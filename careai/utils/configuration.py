import json
import configparser

class Config:

    def __init__(self, parser: configparser.ConfigParser, config_file: str):
        parser.read(config_file)

        self.__open_ai_api_key = parser.get('API_KEYS', 'OPENAI-API_KEY')

        self.__logging_log_path = parser.get('LOGGING', 'LOG_PATH')
        self.__logging_log_level = parser.get('LOGGING', 'LOG_LEVEL')
        self.__logging_chat_history_path = parser.get('LOGGING', 'CHAT_HISTORY_PATH')

        self.__chatbot_debug = parser.get('CHATBOT', 'CHATBOT_DEBUG')
        self.__chatbot_info_path = parser.get('CHATBOT', 'CHAT_INFO_PATH')
        self.__chatbot_temperature = parser.get('CHATBOT', 'TEMPERATURE')
        self.__chatbot_max_token = parser.get('CHATBOT', 'MAX_TOKENS')

        with open(self.__chatbot_info_path,'r') as f:
            self.__chatbot_setup = json.load(f)

    @property
    def open_ai_api_key(self):
        return self.__open_ai_api_key

    @property
    def log_path(self):
        return self.__logging_log_path

    @property
    def log_level(self):
        return self.__logging_log_level

    @property
    def chat_history_path(self):
        return self.__logging_chat_history_path

    @property
    def chat_debug(self):
        return self.__chatbot_debug

    @property
    def chatbot_info_path(self):
        return self.__chatbot_info_path

    @property
    def chatbot_temperature(self):
        return self.__chatbot_temperature

    @property
    def chatbot_max_token(self):
        return self.__chatbot_max_token

    @property
    def chatbot_setup(self):
        return self.__chatbot_setup


def load(config_file="config.ini") -> Config:
    return Config(configparser.ConfigParser(), config_file)