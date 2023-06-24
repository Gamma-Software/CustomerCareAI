import os
import datetime

import careai.utils.configuration as configuration
from careai.core.bot import CareaiBot
from careai.hmi.chat import CLI, Streamlit
from careai.core.io import export_chat_history

class Core:

    def __init__(self, interface):
        """Get the configuration and init the bot, its memory and its chains"""
        self.conf = configuration.load("conf/config.ini")

        self.bot = CareaiBot(self.conf)

        if interface == "cli":
            self.hmi = CLI("Doctor assistant", "Dentist assistant", "")
        else:
            self.hmi = Streamlit("Anne Frank", "This is Anne Frank", "")
            self.hmi.setup(self.bot.process_input)

    def check_for_exit(self, user_input: str) -> bool:
        if user_input.lower() == 'exit':
                export_input = input("\nNice talking to you. Do you want to export our conversation? (Y/N): ")
                if export_input.lower() == 'y':
                    # Access the memory
                    memory = self.chatgpt_chain.memory.load_memory_variables({})
                    # Save chat history in memory
                    export_chat_history(memory, os.path.join(
                        self.conf.chat_history_path,
                        self.conf.chatbot_name,
                        datetime.datetime.now()))
                return True
        return False

    def run(self):
        """Get user input and process it"""
        if isinstance(self.hmi, Streamlit):
            return # Streamlit HMI does not need to run this

        end_chat = False
        while not end_chat:
            try:
                user_input = self.hmi.get_user_input()
            except KeyboardInterrupt:
                user_input = "exit"
            end_chat = self.check_for_exit(user_input)
            if not end_chat:
                no_error, message = self.bot.process_input(user_input)
                if no_error:
                    print("AI: " + message)
                else:
                    end_chat = True

