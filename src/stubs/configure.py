import yaml


class Configuration:
    def __init__(self, logging:object=None, config_file_abspath:str="/etc/bits/config.yaml") -> None:
        #Save absolute path to log file
        self.config_file_abspath = config_file_abspath

        #Initialize handle to logger
        self.log = logging

        #Initialize configuration, will set/load in reverse order
        self.data = {
            "log_level": None,
            "bot_settings": {
                "discord_token": None,
                "a_new_key": None
            }
        }

        #Pull configuration and ensure consistency with self.data
        self.__get_config()
        self.__set_config()
    

    def __get_config(self) -> None:
        with open(self.config_file_abspath, "tr") as fio:
            try:
                temp_config = yaml.safe_load(fio)

                for attribute_key in temp_config.keys():
                    if attribute_key in self.data:
                        self.data[attribute_key] = temp_config[attribute_key]

                self.log.info(f"Parsed log file '{self.config_file_abspath}'")
            except Exception as e:
                self.log.critical(f"Couln't parse configuration from '{self.config_file_abspath}': {e}")
                exit()
    
        
    def __set_config(self) -> None:
        with open(self.config_file_abspath, "tw") as fio:
            try:
                yaml.dump(self.data, fio)
                self.log.info(f"Updated log file '{self.config_file_abspath}'")
            except Exception as e:
                self.log.critical(f"Couln't write configuration to '{self.config_file_abspath}': {e}")
                exit()
