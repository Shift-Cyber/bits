import logging
import time

def bits_logger(log_file_abspath:str="/var/log/bits/bits.log", verbosity:object=logging.DEBUG) -> None:
    try:
        with open(log_file_abspath,'a') as fio: fio.write(f"\n---Logger Initialized [{time.time()}]---\n")
    except Exception as e:
        print(f"[!] Could not open target log file {log_file_abspath} for writing ({e})")
    
    logging.basicConfig(filename=log_file_abspath,
        level=verbosity,
        filemode="a",
        format="[%(asctime)s.%(msecs)03d] (%(name)s|%(levelname)s) %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S')
        
    logger = logging.getLogger("bits")
    
    return logger