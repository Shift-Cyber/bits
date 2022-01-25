import argparse

def parse_args() -> (str,str):
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log", nargs='?', required=True, help="absolute path to logging target")
    parser.add_argument("-c", "--config", nargs='?', required=True, help="absolute path to config target")
    args = parser.parse_args()

    return args.config.strip(), args.log.strip()