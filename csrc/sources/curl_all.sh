curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/rp.h
curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/rp_acq.h
curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/rp_acq_axi.h
curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/rp_enums.h
curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/rp_gen.h
curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/common/version.h

curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/src/rp.i

curl -L https://api.github.com/repos/RedPitaya/RedPitaya/branches/master | grep -o '"sha": "[^"]*' | grep -o '[^"]*$' | head -1 > sha.txt
