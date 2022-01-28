# Entrypoint for the bot service
# ...should be started like:
#    > python3 run.py --log /var/log/bits/bits.log --config /etc/bits/config.yaml
import os

from stubs.parse_args import parse_args
from stubs.logging import bits_logger
from stubs.configure import Configuration
from stubs.file_verification import FileVerification

def main():
    try:
        #Save command line arguments for instantiation
        config_file_abspath, log_file_abspath = parse_args()

        #Build logger from provided path
        verify_log_file = FileVerification(log_file_abspath)
        if not verify_log_file.is_readable(): exit()
        if not verify_log_file.is_writeable(): exit()
        log = bits_logger(log_file_abspath)

        #Initialize configuration handler
        verify_config_file = FileVerification(config_file_abspath, log)
        if not verify_config_file.is_readable(): exit()
        if not verify_config_file.is_writeable(): exit()
        config = Configuration(log, config_file_abspath)


        print(config.data['bot_settings']['discord_token'])

        
        log.info(f"Daemon initialized with config from '{config_file_abspath}' and logging to '{log_file_abspath}'")
        while True:
            pass
    
    except KeyboardInterrupt:
        log.info(f"Daemon terminated via keyboard interrupt")
        exit()


if __name__ == '__main__':
    main()