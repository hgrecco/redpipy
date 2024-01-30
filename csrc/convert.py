import io
import pathlib
import shutil
import subprocess
import textwrap
from dataclasses import dataclass
from typing import Any, Literal, overload
from warnings import warn

import stringcase
from cxxheaderparser import types as cxxtypes
from cxxheaderparser.simple import ParsedData, parse_string

FUNCTIONS_TO_SKIP = [
    "rp_createBuffer",
    "rp_deleteBuffer",
]


def camel_to_snake_case(name: str) -> str:
    name = (
        name.replace("GPIOn", "gpio_n")
        .replace("GPIOp", "gpio_p")
        .replace("AOpin", "ao_pin")
        .replace("AIpin", "ai_pin")
        .replace("DOpin", "do_pin")
        .replace("DIpin", "di_pin")
        .replace("AC_DC", "Ac_dc")
    )
    snake_case = name[0]
    for idx in range(1, len(name) - 1):
        is_upper = name[idx].isupper()
        followed_by_lower = not name[idx + 1].isupper()
        preceded_by_lower = not name[idx - 1].isupper()
        if (is_upper and followed_by_lower) or (is_upper and preceded_by_lower):
            snake_case += "_"
        snake_case += name[idx]
    snake_case += name[len(name) - 1]  # append last letter
    return snake_case.lower()


def format_func_name(name: str, prefix: str) -> str:
    s = camel_to_snake_case(name)
    s = s.replace("__", "_")
    if s.startswith(prefix):
        return s[len(prefix) :]
    return s


MISSING = object()


@dataclass
class Parameter:
    name: str
    is_pointer: bool
    ctype: str
    default_value: Any = MISSING
    call_value: Any = MISSING
    use_in_def: bool = True
    use_in_call: bool = True

    @property
    def pyname(self) -> str:
        return camel_to_snake_case(self.name)

    @property
    def pytype(self) -> str:
        return to_python_type(self.ctype)

    @property
    def numpy_type(self):
        if self.ctype.startswith("uint"):
            return f"np.uint{self.ctype[4:-2]}"
        elif self.ctype.startswith("int"):
            return f"np.int{self.ctype[3:-2]}"
        elif self.ctype == "float":
            return "np.float32"
        elif self.ctype == "double":
            return "np.float64"
        else:
            raise ValueError(self.ctype)

    def as_def_parameter(self) -> str:
        if self.default_value is MISSING:
            return f"{self.pyname}: {self.pytype}"
        else:
            return f"{self.pyname}: {self.pytype} = {self.default_value}"

    def as_call_argument(self) -> str:
        if self.ctype in ENUMS:
            return (
                self.pyname + ".value"
                if self.call_value is MISSING
                else str(self.call_value)
            )
        else:
            return self.pyname if self.call_value is MISSING else str(self.call_value)

    def as_debug_call_argument(self) -> str:
        if self.call_value is MISSING:
            if self.is_pointer:
                return f"'<{self.pyname}>'"
            return self.pyname
        return str(self.call_value)


class Parameters(list[Parameter]):
    def names(self) -> tuple[str, ...]:
        return tuple(p.name for p in self)

    def as_def_parameters(self) -> str:
        return ", ".join(p.as_def_parameter() for p in self if p.use_in_def)

    def as_call_arguments(self) -> str:
        return ", ".join(p.as_call_argument() for p in self if p.use_in_call)

    def as_debug_call_arguments(self) -> str:
        tmp = tuple(p.as_debug_call_argument() for p in self if p.use_in_call)
        if len(tmp) == 0:
            return ""
        elif len(tmp) == 1:
            return tmp[0] + ", "
        return ", ".join(tmp)


@dataclass(frozen=True)
class Doc:
    main: str
    parameters: dict[str, str]
    ret: str

    def as_docstring(self, include: tuple[str, ...]) -> str:
        doc = textwrap.fill(self.main)

        py_doc = "\n\n"
        py_doc += "Parameters\n"
        py_doc += "----------\n"
        use_pydoc = False
        for name, pdoc in self.parameters.items():
            if name in include:
                py_doc += camel_to_snake_case(name) + "\n"
                py_doc += textwrap.fill(
                    pdoc, initial_indent=INDENT, subsequent_indent=INDENT
                )
                use_pydoc = True

        c_doc = "\n\n"
        c_doc += "C Parameters\n"
        c_doc += "------------\n"
        use_cdoc = False
        for name, pdoc in self.parameters.items():
            if name not in include:
                c_doc += camel_to_snake_case(name) + "\n"
                c_doc += textwrap.fill(
                    pdoc, initial_indent=INDENT, subsequent_indent=INDENT
                )
                use_cdoc = True

        if use_pydoc:
            doc += py_doc
        if use_cdoc:
            doc += c_doc

        doc = f'''"""{doc}\n"""'''
        return textwrap.indent(doc, INDENT)


PATH = pathlib.Path(__file__).parent
SOURCE_PATH = PATH / "sources"
CONVERTED_PATH = PATH / "converted"

shutil.copy(PATH / "constants.py", CONVERTED_PATH / "constants.py")

commit_id = (SOURCE_PATH / "sha.txt").read_text().strip("\n")


MODULE_TEMPLATE = (PATH / "_template.tmpl").read_text()

INDENT = " " * 4

ENUMS = dict(
    rp_dpin_t="Pin",
    rp_pinState_t="PinState",
    rp_outTiggerMode_t="OutTriggerMode",
    rp_pinDirection_t="PinDirection",
    rp_apin_t="AnalogPin",
    rp_waveform_t="Waveform",
    rp_gen_mode_t="GenMode",
    rp_gen_sweep_dir_t="GenSweepDirection",
    rp_gen_sweep_mode_t="GenSweepMode",
    rp_trig_src_t="TriggerSource",
    rp_gen_gain_t="GenGain",
    rp_channel_t="Channel",
    rp_channel_trigger_t="TriggerChannel",
    rp_eq_filter_cof_t="EqFilterCoefficient",
    rp_acq_decimation_t="Decimation",
    rp_acq_ac_dc_mode_t="AcqMode",
    rp_acq_trig_src_t="AcqTriggerSource",
    rp_acq_trig_state_t="AcqTriggerState",
)


def my_parse_file(path: pathlib.Path) -> ParsedData:
    content = path.read_text()
    out: list[str] = []
    for line in content.split("\n"):
        if line.startswith("#ifdef"):
            continue
        if line.startswith("#ifndef"):
            continue
        if line.startswith("#endif"):
            continue
        if line.startswith("#define"):
            continue
        if line.startswith("#include"):
            continue
        out.append(line)
    return parse_string("\n".join(out))


def to_python_type(s: str) -> str:
    if s.startswith("uint"):
        return "int"
    elif s.startswith("int"):
        return "int"
    elif s == "float":
        return "float"
    elif s == "double":
        return "float"
    elif s == "bool":
        return "bool"
    elif s == "buffers_t":
        return "np.ndarray"
    elif s in ENUMS:
        return "constants." + ENUMS[s]
    elif s.startswith("rp_"):
        return "constants." + stringcase.pascalcase(s[3:].strip("_t"))  # type: ignore
    raise ValueError(s)


def get_buffer_string(ctype: str, buffer_size: str | int) -> str:
    if ctype in ("float", "double"):
        return f"rp.fBuffer({buffer_size})"
    elif ctype.startswith("uint"):
        return f"rp.uBuffer({buffer_size})"
    elif ctype.startswith("int"):
        return f"rp.iBuffer({buffer_size})"
    raise ValueError(ctype)


def buffer_to_numpy_array(
    numpy_type: str, buffer_name: str, buffer_size: str | int
) -> str:
    return f"np.fromiter({buffer_name}, dtype={numpy_type}, count={buffer_size})"


GETTER_TEMPLATE_NO_ERROR_CODE = """
def {func_pyname}({as_def_parameters}) -> {pyout_type}:
{doc}

{pre}

    __value = rp.{func_cname}({as_call_arguments})

{post}


"""

GETTER_TEMPLATE_WITH_ERROR_CODE = """
def {func_pyname}({as_def_parameters}) -> {pyout_type}:
{doc}

{pre}

    __status_code, __value = rp.{func_cname}({as_call_arguments})

    if __status_code != StatusCode.OK.value:
        raise constants.RPPError(
            "{func_cname}",
            ({as_debug_call_arguments}),
              __status_code
              )

{post}
"""

SETTER_TEMPLATE_NO_ERROR_CODE = """
def {func_pyname}({as_def_parameters}) -> {pyout_type}:
{doc}

{pre}

    rp.{func_cname}({as_call_arguments})

{post}


"""

SETTER_TEMPLATE_WITH_ERROR_CODE = """
def {func_pyname}({as_def_parameters}) -> {pyout_type}:
{doc}

{pre}

    __status_code = rp.{func_cname}({as_call_arguments})

    if __status_code != StatusCode.OK.value:
        raise constants.RPPError(
            "{func_cname}",
            ({as_debug_call_arguments}),
              __status_code
              )

{post}
"""


def parse_doc(doc: str | None) -> Doc:
    if doc is None:
        return Doc("", {}, "")
    doc = doc.replace("/**", "").replace("*/", "").replace("*", "")

    main = ""

    pending = list(reversed(doc.split("\n")))
    parameters: dict[str, str] = {}

    if not pending:
        return Doc(main.strip(), parameters, "")

    ret: str | None = None

    line = ""
    while pending:
        line = pending.pop().strip()
        if line.startswith("@"):
            break
        main += " " + line.strip()

    tmp: list[str] = [line]
    while pending:
        line = pending.pop().strip()
        if line.startswith("@"):
            tmp.append(line.strip())
        else:
            tmp[-1] += " " + line.strip()

    for el in tmp:
        if not el.strip():
            continue
        base, rest = el.split(" ", 1)
        if base == "@param":
            name, doc = rest.split(" ", 1)
            parameters[name] = doc
        elif base == "@return":
            ret = rest
        else:
            raise Exception("Why here!")

    if ret is None:
        ret = ""

    return Doc(main.strip(), parameters, ret)


@overload
def get_guess(
    parameters: list[Parameter]
) -> tuple[Literal["*size_*buffer"], tuple[Parameter, Parameter]]:
    ...


def get_guess(parameters: list[Parameter]) -> tuple[str, tuple[Parameter, ...]]:
    for ndx in range(len(parameters) - 1):
        if parameters[ndx].name == "size" and parameters[ndx + 1].name == "buffer":
            return "*size_*buffer", (parameters[ndx], parameters[ndx + 1])
        if (
            parameters[ndx].name == "buffer"
            and parameters[ndx + 1].name == "buffer_size"
        ):
            return "*size_*buffer", (parameters[ndx + 1], parameters[ndx])
    return "unknown", ()


log = print
for filename in ("acq", "acq_axi", "gen", "rp"):
    if filename == "rp":
        cfilename = "rp.h"
    else:
        cfilename = f"rp_{filename}.h"

    pymodule_name = f"{filename}.py"

    log(f"Converting {filename} -> {pymodule_name}")

    content = io.StringIO()

    def o_print(s: str) -> int:
        return content.write(s)

    skipped_functions: list[str] = []

    for func in my_parse_file(SOURCE_PATH / cfilename).namespace.functions:
        msg = ""
        func_cname: str = func.name.segments[0].name

        if func_cname in FUNCTIONS_TO_SKIP:
            log(f"- Skipping {func_cname}")
            skipped_functions.append(func_cname)
            continue

        func_pyname = format_func_name(func_cname[3:], filename + "_")

        log(f"- Converting {func_cname} -> {func_pyname}")

        is_getter = "Get" in func_cname
        is_setter = "Set" in func_cname
        is_call = False

        # If the return type is int, it might return a status code.
        # If the return type is not int, it does not return a status code.
        cfunc_has_status_code_by_rtype = (
            not isinstance(func.return_type, cxxtypes.Pointer)
            and func.return_type.typename.segments[0].name == "int"
        )

        # If the docstring says RP_OK, it returns a status code.
        # If the docstring does not say RP_OK, it migh return a status code.
        cfunc_has_status_code_by_doc = "RP_OK" in (func.doxygen or "")

        if cfunc_has_status_code_by_rtype and cfunc_has_status_code_by_doc:
            cfunc_has_status_code = True
        elif not cfunc_has_status_code_by_rtype and not cfunc_has_status_code_by_doc:
            cfunc_has_status_code = False
        else:
            # guesses do not agree
            if not cfunc_has_status_code_by_doc and cfunc_has_status_code_by_rtype:
                # it might be missing in the docs.
                cfunc_has_status_code = True
                log("  guessing status code: True")
            else:
                cfunc_has_status_code = None
                log("  Inconsistent guess status code")

        if is_getter and is_setter:
            warn(f"In {filename}, {func_cname} is both getter and setter")
        elif not (is_getter or is_setter):
            is_call = True

        parameters: Parameters = Parameters()

        for func_param in func.parameters:
            if isinstance(func_param.type, cxxtypes.Pointer):
                param = Parameter(
                    func_param.name,
                    True,
                    func_param.type.ptr_to.typename.segments[0].name,
                )
            else:
                param = Parameter(
                    func_param.name, False, func_param.type.typename.segments[0].name
                )

            parameters.append(param)

            del param

        pre_call = []
        post_call = []

        has_buffer = any(param.name == "buffer" for param in parameters)
        count_pointers = sum(param.is_pointer for param in parameters)

        pyout_type = "None"
        if is_getter:
            if has_buffer:
                if len(parameters) == 1:
                    out = parameters.pop()
                    pyout_type = to_python_type(out.ctype)
                    pre_call = [
                        out.name
                        + " = "
                        + get_buffer_string(out.ctype, "constants.ADC_BUFFER_SIZE")
                    ]
                    post_call = [
                        "return "
                        + buffer_to_numpy_array(
                            out.numpy_type, out.name, "constants.ADC_BUFFER_SIZE"
                        )
                    ]
                else:
                    org, pars = get_guess(parameters)

                    if org == "*size_*buffer":
                        szpar, bufpar = pars
                        pre_call = [
                            bufpar.pyname
                            + " = "
                            + get_buffer_string(
                                bufpar.ctype, "constants.ADC_BUFFER_SIZE"
                            ),
                        ]

                        post_call = [
                            "return "
                            + buffer_to_numpy_array(
                                bufpar.numpy_type,
                                bufpar.name,
                                "constants.ADC_BUFFER_SIZE",
                            )
                        ]

                        szpar.use_in_def = False
                        szpar.call_value = "constants.ADC_BUFFER_SIZE"
                        bufpar.use_in_def = False
                        bufpar.call_value = bufpar.pyname

                        pyout_type = f"npt.NDArray[{bufpar.numpy_type}]"

                    else:
                        print("!!!", func_cname)

            else:
                if count_pointers == 1:
                    for ndx, out in enumerate(parameters):
                        if out.is_pointer:
                            break
                    parameters.pop(ndx)
                    pyout_type = out.pytype
                    post_call = ["return __value"]

                elif count_pointers == 0:
                    # This function does not return an error code
                    # i.e. math functinos
                    if isinstance(func.return_type, cxxtypes.Pointer):
                        if func.return_type.ptr_to.typename.segments[0].name == "char":
                            pyout_type = "str"
                        else:
                            raise ValueError("")
                    else:
                        pyout_type = to_python_type(
                            func.return_type.typename.segments[0].name
                        )
                    post_call = ["return __value"]
                else:
                    # return all values
                    pyout_type = "tuple[{}]".format(
                        ", ".join((p.pytype for p in parameters))
                    )
                    post_call = ["return __value"]

        pre = INDENT + ("\n" + INDENT).join(pre_call)
        post = INDENT + ("\n" + INDENT).join(post_call)

        kwargs = dict(
            func_pyname=func_pyname,
            func_cname=func_cname,
            doc=parse_doc(func.doxygen).as_docstring(parameters.names()),
            as_def_parameters=parameters.as_def_parameters(),
            as_call_arguments=parameters.as_call_arguments(),
            as_debug_call_arguments=parameters.as_debug_call_arguments(),
            pyout_type=pyout_type,
            pre=pre,
            post=post,
        )

        if is_getter:
            if cfunc_has_status_code:
                o_print(GETTER_TEMPLATE_WITH_ERROR_CODE.format(**kwargs))
            else:
                o_print(GETTER_TEMPLATE_NO_ERROR_CODE.format(**kwargs))
        elif is_setter:
            if cfunc_has_status_code:
                o_print(SETTER_TEMPLATE_WITH_ERROR_CODE.format(**kwargs))
            else:
                o_print(SETTER_TEMPLATE_NO_ERROR_CODE.format(**kwargs))
        elif is_call:
            if cfunc_has_status_code:
                o_print(SETTER_TEMPLATE_WITH_ERROR_CODE.format(**kwargs))
            else:
                o_print(SETTER_TEMPLATE_NO_ERROR_CODE.format(**kwargs))

    if skipped_functions:
        msg = "Skipped functions\n"
        msg += "-----------------\n"
        msg += "\n".join(("- " + s) for s in skipped_functions)
        msg = "\n" + textwrap.indent(msg, INDENT) + "\n"
    else:
        msg = ""

    with (CONVERTED_PATH / pymodule_name).open("w", encoding="UTF-8") as fo:
        qualname = "redpipy." + pymodule_name[:-3]
        fo.write(
            MODULE_TEMPLATE.format(
                qualname=qualname,
                underline=len(qualname) * "~",
                content=content.getvalue(),
                original_file=cfilename,
                commit_id=commit_id,
                msg=msg,
            )
        )

    subprocess.run(["ruff", "format", str(CONVERTED_PATH / pymodule_name)])
    subprocess.run(["ruff", "--fix", str(CONVERTED_PATH / pymodule_name)])
