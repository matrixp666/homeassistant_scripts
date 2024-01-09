# Script for automatically updating letsencrypt certificate

prerequisites:
 * Router is a Fritzbox with preconfigured port forwarding for your hass installation and port 80
 * nginx is configured as reverse proxy for hass installation
 * REST API of hass installation is activated
 * access token is created in hass installation and correctly entered in this script
 * date.sh script is accessible and executable to calculate age of certificate
 * this python script runs as cronjob
 * hass installation should consist of openssl package in alpine linux distribution:
   * apk update && apk add openssl  

