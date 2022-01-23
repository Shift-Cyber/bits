#banner
echo "
██████╗ ██╗████████╗███████╗    ██████╗  ██████╗ ████████╗     ██████╗██╗     ███████╗ █████╗ ███╗   ██╗██╗   ██╗██████╗ 
██╔══██╗██║╚══██╔══╝██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝    ██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║██║   ██║██╔══██╗
██████╔╝██║   ██║   ███████╗    ██████╔╝██║   ██║   ██║       ██║     ██║     █████╗  ███████║██╔██╗ ██║██║   ██║██████╔╝
██╔══██╗██║   ██║   ╚════██║    ██╔══██╗██║   ██║   ██║       ██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║██╔═══╝ 
██████╔╝██║   ██║   ███████║    ██████╔╝╚██████╔╝   ██║       ╚██████╗███████╗███████╗██║  ██║██║ ╚████║╚██████╔╝██║     
╚═════╝ ╚═╝   ╚═╝   ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝        ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     

This script exists to purge the Bits Discord bot from a Linux environment. Your password will be required
 for elevated actions related to stoping services and cleaning up files with elevated permissions. Please
 reach-out to contact@scyca.org if you are experiencing bugged code or find missing things. --SCYCA Staff"

#ANSI Codes
RED_BOLD='\033[1;31m'
RESET='\033[0m'

#Remove config from /etc
printf "\n"${RED_BOLD}
read -p "Remove configuration /etc/bits/config.yaml? [Y/n] ${NC}" CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
    set -x #trace to stdout
    sudo rm -f /etc/bits/config.yaml
    set +x #reset tracing
fi

#Setup service account
printf "\n"${RED_BOLD}
read -p "Remove service account 'bits'? [Y/n] " CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
    set -x #trace to stdout
    sudo userdel bits
    set +x #reset tracing
fi

#Setup logs at /var/log/bits
printf "\n"${RED_BOLD}
read -p "Remove logging directory at /var/log/bits? [Y/n] " CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
    set -x #trace to stdout
    sudo rm -rf /var/log/bits
    set +x #reset tracing
fi

#Purge install from /opt/bits
printf "\n"${RED_BOLD}
read -p "Purge install from /opt/bits? [Y/n] " CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
    set -x #trace to stdout
    sudo rm -rf /opt/bits
    set +x #reset tracing
fi

#Setup systemd daemon
printf "\n"${RED_BOLD}
read -p "Stop daemon and purge? [Y/n] " CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
    set -x #trace to stdout
    sudo systemctl stop bits.service
    sudo systemctl disable bits.service
    sudo rm -f /etc/systemd/system/bits.service
    sudo systemctl daemon-reload
    sudo systemctl reset-failed
    set +x #reset tracing
fi