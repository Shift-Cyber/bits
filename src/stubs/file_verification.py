import os.path
import logging
import errno

class FileVerification:
    def __init__(self, file_abspath:str, logging:object=None) -> None:
        #Save absolute path to file
        self.file_abspath = file_abspath

        #Initialize handle to logger else log to stdout
        self.log = logging


    def is_writeable(self) -> bool:
        try:
            with open(self.file_abspath, 'ta') as fio:
                self.__log(f"File '{self.file_abspath}' is writeable", logging.DEBUG)
            
            #File is writeable
            return True

        except IOError as e:
            if e.errno == errno.ENOENT:
                self.__log(f"File '{self.file_abspath}' is not writeable: does not exist", logging.WARNING)
            elif e.errno == errno.EACCES:
                self.__log(f"File '{self.file_abspath}' is not writeable: no write permission", logging.WARNING)
            elif e.errno == errno.EISDIR:
                self.__log(f"File '{self.file_abspath}' is not writeable: path is a directory", logging.WARNING)
            else:
                self.__log(f"File '{self.file_abspath}' is not writeable: {e.errno}", logging.WARNING)

            #File is not writeable
            return False


    def is_readable(self) -> bool:
        try:
            with open(self.file_abspath) as fio:
                _ = fio.read()
                self.__log(f"File '{self.file_abspath}' is readable", logging.DEBUG)
            
            #File is readable
            return True

        except IOError as e:
            if e.errno == errno.ENOENT:
                self.__log(f"File '{self.file_abspath}' is not readable: does not exist", logging.WARNING)
            elif e.errno == errno.EACCES:
                self.__log(f"File '{self.file_abspath}' is not readable: no read permission", logging.WARNING)
            elif e.errno == errno.EISDIR:
                self.__log(f"File '{self.file_abspath}' is not readable: path is a directory", logging.WARNING)
            else:
                self.__log(f"File '{self.file_abspath}' is not readable: {e.errno}", logging.WARNING)

            #File is not readable
            return False
    

    def is_directory(self) -> bool:
        if os.path.isdir(self.file_abspath):
            #File is a directory
            self._log(f"'{file_abspath}' is a directory", logging.DEBUG)
            return True

        else:
            #File is not a directory is inaccessible
            self.__log(f"'{file_abspath}' is not a directory or is inaccessible", logging.DEBUG)
            return False

    def __log(self, message:str, level:object=None) -> None:
        if self.log == None:
            if (level==logging.WARNING or level==logging.ERROR or level==logging.CRITICAL):
                print(message)
        elif level==logging.DEBUG:
            self.log.debug(message)
        elif level==logging.INFO:
            self.log.info(message)
        elif level==logging.WARNING:
            self.log.warning(message)
        elif level==logging.ERROR:
            self.log.error(message)
        elif level==logging.CRITICAL:
            self.log.critical(message)
        else:
            print('[!] Unknown error, this should never happen!')
            exit()