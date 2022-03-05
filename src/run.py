# Entrypoint for the bot service
# ...should be started like:
#    > python3 run.py --log /var/log/bits/bits.log --config /etc/bits/config.yaml
import os
import logging

from stubs.parse_args import parse_args
from stubs.logging import bits_logger
from stubs.file_verification import FileVerification
from configure import Configuration
from bot import Bot

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

        #Apply logging verbosity from configuration
        if (config.data['log_level'].upper() == "DEBUG"): _ = logging.DEBUG
        elif (config.data['log_level'].upper() == "INFO"): _ = logging.INFO
        elif (config.data['log_level'].upper() == "WARNING"): _ = logging.WARNING
        elif (config.data['log_level'].upper() == "ERROR"): _ = logging.ERROR
        elif (config.data['log_level'].upper() == "CRITICAL"): _ = logging.CRITICAL
        else:
            log.warning(f"Could not interpret log verbosity from config: {config.data['bot_settings']}")
            _ = logging.DEBUG
        log.setLevel(_)
        log.info(f"Applied log level {_} from configuration file")

        #Initialize bot
        log.info(f"Initialized bot with config from '{config_file_abspath}' logging to '{log_file_abspath}'")
        Bot(log, config)
    
    except KeyboardInterrupt:
        log.info(f"Daemon terminated via keyboard interrupt")
        exit()


if __name__ == '__main__':
    main()
