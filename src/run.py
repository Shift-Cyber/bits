# Entrypoint for all bot code
# should be run like:
#    ./run --log /var/log/bits/bits.log --config /etc/bits/config.yaml
import os

from stubs.parse_args import parse_args
from stubs.logging import bits_logger
from stubs.configure import Configuration

def main():
    #Save command line arguments for instantiation
    config_file_abspath, log_file_abspath = parse_args()

    #Build logger from provided path
    logger = bits_logger(log_file_abspath)

    #Initialize configuration handler
    config = Configuration(logger, config_file_abspath)




    

    logger.info(f"Initialized daemon with config from '{config_file_abspath},' logging to '{log_file_abspath}'")
    while True:
        pass


if __name__ == '__main__':
    main()