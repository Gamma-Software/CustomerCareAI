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

        max_num_turns = 10
        print('='*10)
        cnt = 0
        while cnt !=max_num_turns:
            cnt+=1
            if cnt==max_num_turns:
                print('Maximum number of turns reached - ending the conversation.')
                break
            self.bot.agent.step()

            # end conversation
            if '<END_OF_CALL>' in self.bot.conversation_history[-1]:
                print('Agent determined it is time to end the conversation.')
                break
            try:
                user_input = self.hmi.get_user_input()
            except KeyboardInterrupt:
                user_input = "exit"

            if not self.check_for_exit(user_input):
                no_error, message = self.bot.process_input(user_input)
                if not no_error:
                    break
            print('='*10)
