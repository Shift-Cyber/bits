import yaml


class Configuration:
    def __init__(self, logging:object, config_file_abspath:str="/etc/bits/config.yaml") -> None:
        self.config_file_abspath = config_file_abspath
        self.log = logging
    
    def __get_config(self) -> None:

        #assert that the file exists and is readable, exit on failure

        #read yaml into class attributes if exists
        pass

    def __set_config(self) -> None:

        #assert that the file exists and is readable, exit on failure

        #write yaml into class attributes if exists


        with open(self.config_file_abspath, 'tw') as fio:
            documents = yaml.dump(dict_file, fio)
        #write current class attributes to config file
        pass