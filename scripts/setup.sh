#banner
echo "
█████╗  ██╗████████╗███████╗    ██████╗  ██████╗ ████████╗    ███████╗███████╗████████╗██╗   ██╗██████╗
██╔══██╗██║╚══██╔══╝██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝    ██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
██████╔╝██║   ██║   ███████╗    ██████╔╝██║   ██║   ██║       ███████╗█████╗     ██║   ██║   ██║██████╔╝
██╔══██╗██║   ██║   ╚════██║    ██╔══██╗██║   ██║   ██║       ╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ 
██████╔╝██║   ██║   ███████║    ██████╔╝╚██████╔╝   ██║       ███████║███████╗   ██║   ╚██████╔╝██║
╚═════╝ ╚═╝   ╚═╝   ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝       ╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝

This script exists to initialize the Bits Discord bot in a Linux environment. Your password will be required
 for elevated actions related to dependency install, service account creation and config/source install. Please
 reach-out to contact@scyca.org if you are experiencing bugged code or find missing things. --SCYCA Staff
 "

#ANSI Codes
BLUE_BOLD='\033[1;34m'
RESET='\033[0m'

#Install pip3 and Python3 requirements from file
printf ${BLUE_BOLD}
read -p "Install Python3 requirements? [Y/n] " CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
    sudo apt update
    sudo apt install python3-pip
    pip3 install -r ../requirements.txt
fi

#Setup service account
printf "\n"${BLUE_BOLD}
read -p "Setup service account 'bits'? [Y/n] " CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
    set -x #trace to stdout
    sudo useradd --system --shell /bin/false bits
    set +x #reset tracing
fi

#Create config in /etc and set permissions
printf "\n"${BLUE_BOLD}
read -p "Install configuration at /etc/bits/config.yaml? [Y/n] ${NC}" CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
    set -x #trace to stdout
    sudo mkdir -p /etc/bits
    sudo touch /etc/bits/config.yaml
    sudo chown bits:bits -R /etc/bits
    sudo chmod -R 700 /etc/bits
    set +x #reset tracing
fi

#Setup logs at /var/log/bits
printf "\n"${BLUE_BOLD}
read -p "Setup logging directory at /var/log/bits? [Y/n] " CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
    set -x #trace to stdout
    sudo mkdir -p /var/log/bits
    sudo touch /var/log/bits/bits.log
    sudo chown bits:bits -R /var/log/bits
    sudo chmod -R 700 /var/log/bits
    set +x #reset tracing
fi

#Install into /opt/bits
printf "\n"${BLUE_BOLD}
read -p "Install to /opt/bits? [Y/n] " CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
    SCRIPT_DIR="$(realpath $0 | awk 'BEGIN{FS=OFS="/"} NF--' | awk 'BEGIN{FS=OFS="/"} NF--')"
    set -x #trace to stdout
    sudo mkdir -p /opt/bits
    sudo cp -r $SCRIPT_DIR/* /opt/bits
    sudo chown bits:bits -R /opt/bits
    sudo chmod -R 700 /opt/bits
    set +x #reset tracing
fi

#Setup systemd daemon
printf "\n"${BLUE_BOLD}
read -p "Setup systemd daemon and start the bot? [Y/n] " CONT
printf ${RESET}
if [ "$CONT" = "y" ]; then
     sudo bash -c 'echo "[Unit]
Description=Bits Discord Bot
After=multi-user.target

[Service]
Type=simple
Restart=always
User=bits
Group=bits
ExecStart=/usr/bin/python3 /opt/bits/src/run.py --log /var/log/bits/bits.log --config /etc/bits/config.yaml

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/bits.service'

    set -x #trace to stdout
    sudo systemctl daemon-reload
    sudo systemctl enable bits.service
    sudo systemctl start bits.service
    set +x #reset tracing
fi
