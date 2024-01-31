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


class MissingType:
    pass


MISSING = MissingType()


@dataclass
class Parameter:
    name: str
    is_pointer: bool
    ctype: str
    default_value: Any = MISSING
    call_value: Any = MISSING
    use_in_def: bool = True
    use_in_call: bool = True

    @classmethod
    def from_cxx_obj(cls, obj: Any) -> "Parameter":
        return cls.from_cxx_name_and_type(obj.name, obj.type)

    @classmethod
    def from_cxx_name_and_type(cls, name: str, param_type: Any) -> "Parameter":
        if isinstance(param_type, cxxtypes.Pointer):
            return Parameter(
                name,
                True,
                param_type.ptr_to.typename.segments[0].name,
            )
        else:
            return Parameter(name, False, param_type.typename.segments[0].name)

    @property
    def pyname(self) -> str:
        return camel_to_snake_case(self.name)

    @property
    def cout_pyname(self) -> str:
        return "__" + self.pyname

    @property
    def arr_pyname(self) -> str:
        return "__arr_" + self.pyname

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

    def as_def_return_var(self) -> str:
        if self.ctype in ENUMS:
            return "constants." + ENUMS[self.ctype] + f"({self.cout_pyname})"
        else:
            return self.cout_pyname

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

    def pairs(self):
        if len(self) == 0:
            yield None, None
            return
        if len(self) == 1:
            yield self[0], None
            return
        for ndx in range(len(self) - 1):
            yield self[ndx], self[ndx + 1]
        yield self[-1], None


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
                py_doc += (
                    textwrap.fill(pdoc, initial_indent=INDENT, subsequent_indent=INDENT)
                    + "\n"
                )
                use_pydoc = True

        c_doc = "\n\n"
        c_doc += "C Parameters\n"
        c_doc += "------------\n"
        use_cdoc = False
        for name, pdoc in self.parameters.items():
            if name not in include:
                c_doc += camel_to_snake_case(name) + "\n"
                c_doc += (
                    textwrap.fill(pdoc, initial_indent=INDENT, subsequent_indent=INDENT)
                    + "\n"
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
shutil.copy(PATH / "error.py", CONVERTED_PATH / "error.py")

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


def build_buffer_string(varname: str, ctype: str, buffer_size: str | int) -> str:
    return varname + " = " + get_buffer_string(ctype, buffer_size)


def buffer_to_numpy_array(
    numpy_type: str, buffer_name: str, buffer_size: str | int
) -> str:
    return f"np.fromiter({buffer_name}, dtype={numpy_type}, count={buffer_size})"


def build_numpy_array(
    varname: str, numpy_type: str, buffer_name: str, buffer_size: str | int
) -> str:
    return varname + " = " + buffer_to_numpy_array(numpy_type, buffer_name, buffer_size)


WITHOUT_ERROR_CODE = """
def {func_pyname}({def_parameters}) -> {def_return_type}:
{doc}

{pre}

    {call_return_vars} = rp.{func_cname}({call_arguments})

{post}

    return {def_return_vars}
"""

WITH_ERROR_CODE = """
def {func_pyname}({def_parameters}) -> {def_return_type}:
{doc}

{pre}

    {call_return_vars} = rp.{func_cname}({call_arguments})

    if __status_code != StatusCode.OK.value:
        raise RPPError(
            "{func_cname}",
            {debug_call_arguments},
              __status_code
              )

{post}

    return {def_return_vars}
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
            parameters[name.strip()] = doc.strip()
        elif base == "@return":
            ret = rest.strip()
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
        pthis, pnext = parameters[ndx], parameters[ndx + 1]
        if pthis.name == "size" and pnext.name == "buffer":
            return "*size_*buffer", (pthis, pnext)
        if pthis.name == "buffer" and pnext.name == "buffer_size":
            return "*buffer_*buffer_size", (pthis, pnext)

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
        func_cname: str = func.name.segments[0].name  # type: ignore

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

        parameters = Parameters(map(Parameter.from_cxx_obj, func.parameters))
        ret = Parameter.from_cxx_name_and_type("return", func.return_type)

        has_buffer = any(param.name == "buffer" for param in parameters)
        count_pointers = sum(param.is_pointer for param in parameters)

        pre_call: list[str] = []
        post_call: list[str] = []

        #############################
        # Call to rp c function
        #############################
        call_arguments: list[str] = []
        # return arguments from c function
        call_return_vars: list[str] = []

        if cfunc_has_status_code:
            call_return_vars.append("__status_code")

        #############################
        # Python Function Definition
        #############################
        def_parameters: list[str] = []
        def_return_type: list[str] = []
        def_return_vars: list[str] = []

        codepath = ""

        it = iter(parameters.pairs())
        for p, pnext in it:
            if p is None:
                continue
            if pnext and p.is_pointer and pnext.is_pointer:
                if (p.name, pnext.name) == ("size", "buffer"):
                    szpar, bufpar = p, pnext
                    pre_call = [
                        build_buffer_string(bufpar.pyname, bufpar.ctype, szpar.pyname)
                    ]
                    szpar.default_value = "constants.ADC_BUFFER_SIZE"
                    def_parameters.append(szpar.as_def_parameter())
                    call_arguments.append(szpar.pyname)
                    call_arguments.append(bufpar.pyname)
                    call_return_vars.append(szpar.cout_pyname)
                    call_return_vars.append(bufpar.cout_pyname)
                    post_call = [
                        build_numpy_array(
                            bufpar.arr_pyname,
                            bufpar.numpy_type,
                            bufpar.pyname,
                            szpar.cout_pyname,
                        )
                    ]
                    def_return_vars.append(bufpar.arr_pyname)
                    def_return_type.append(f"npt.NDArray[{bufpar.numpy_type}]")
                    next(it)  # consume pnext
                    continue
                elif (p.name, pnext.name) == ("buffer", "buffer_size"):
                    bufpar, szpar = p, pnext
                    pre_call = [
                        build_buffer_string(bufpar.pyname, bufpar.ctype, szpar.pyname)
                    ]
                    szpar.default_value = "constants.ADC_BUFFER_SIZE"
                    def_parameters.append(szpar.as_def_parameter())
                    call_arguments.append(bufpar.pyname)
                    call_arguments.append(szpar.pyname)
                    call_return_vars.append(bufpar.cout_pyname)
                    call_return_vars.append(szpar.cout_pyname)
                    post_call = [
                        build_numpy_array(
                            bufpar.arr_pyname,
                            bufpar.numpy_type,
                            bufpar.pyname,
                            szpar.cout_pyname,
                        )
                    ]
                    def_return_vars.append(bufpar.arr_pyname)
                    def_return_type.append(f"npt.NDArray[{bufpar.numpy_type}]")
                    next(it)  # consume pnext
                    continue

            if p.is_pointer:
                if count_pointers == 1:
                    # unique pointer parameter, likely converted to output
                    # call_arguments.append(p.as_call_argument())
                    call_return_vars.append(p.cout_pyname)
                    # def_parameters.append(p.as_def_parameter())
                    def_return_vars.append(p.as_def_return_var())
                    def_return_type.append(p.pytype)
                else:
                    call_arguments.append(p.as_call_argument())
                    call_return_vars.append(p.cout_pyname)
                    def_parameters.append(p.as_def_parameter())
                    def_return_vars.append(p.as_def_return_var())
                    def_return_type.append(p.pytype)
            else:
                call_arguments.append(p.as_call_argument())
                # call_return_vars.append(p.cout_pyname)
                def_parameters.append(p.as_def_parameter())
                # def_return_vars.append(p.as_def_return_var())
                # def_return_type.append(p.pytype)

        if ret.is_pointer:
            if ret.ctype == "char":
                call_return_vars.append("__value")
                def_return_vars.append("__value")
                def_return_type.append("str")
            else:
                raise ValueError(ret.ctype)
        if not call_return_vars and not cfunc_has_status_code:
            # likely a math call
            call_return_vars.append("__value")
            def_return_vars.append("__value")
            def_return_type.append(ret.pytype)

        pre = INDENT + ("\n" + INDENT).join(pre_call)
        post = INDENT + ("\n" + INDENT).join(post_call)

        if not def_return_type:
            def_return_type = ["None"]

        kwargs = dict(
            func_pyname=func_pyname,
            func_cname=func_cname,
            doc=parse_doc(func.doxygen).as_docstring(parameters.names()),
            def_parameters=", ".join(map(str, def_parameters)),
            def_return_type=", ".join(def_return_type)
            if len(def_return_type) == 1
            else ("tuple[%s]" % (", ".join(def_return_type))),
            def_return_vars=", ".join(def_return_vars),
            call_return_vars=", ".join(call_return_vars),
            call_arguments=", ".join(call_arguments),
            debug_call_arguments="_to_debug(%s)" % (", ".join(call_arguments)),
            pre=pre,
            post=post,
        )

        if cfunc_has_status_code:
            o_print(WITH_ERROR_CODE.format(**kwargs))
        else:
            o_print(WITHOUT_ERROR_CODE.format(**kwargs))

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
