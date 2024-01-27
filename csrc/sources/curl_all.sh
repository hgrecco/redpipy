curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/redpitaya/rp.h
curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/redpitaya/rp_acq.h
curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/redpitaya/rp_acq_axi.h
curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/redpitaya/rp_enums.h
curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/redpitaya/rp_gen.h
curl -O https://raw.githubusercontent.com/RedPitaya/RedPitaya/master/rp-api/api/include/redpitaya/version.h

curl -L https://api.github.com/repos/RedPitaya/RedPitaya/branches/master | grep -o '"sha": "[^"]*' | grep -o '[^"]*$' | head -1 > sha.txt
