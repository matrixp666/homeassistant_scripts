#!/usr/bin/env bash
DOMAIN_NAME=matrixp.selfhost.co
DOMAIN_PORT=8124
now_epoch=$( date +%s )
expiry_date=$( echo | openssl s_client -showcerts -servername ${DOMAIN_NAME} -connect ${DOMAIN_NAME}:${DOMAIN_PORT} 2>/dev/null | openssl x509 -inform pem -noout -enddate | cut -d "=" -f 2 )
#echo -n " $expiry_date";
expiry_epoch=$( date -d "${expiry_date::-4}" +%s )
expiry_days="$(( ($expiry_epoch - $now_epoch) / (3600 * 24) ))"
echo "$expiry_days"