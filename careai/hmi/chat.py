from PIL import Image

class CLI:
    def __init__(self, title, description, prompt):
        print("Bot name: ", title)
        print("Bot description: ", description)

    # Get user input and process it
    def get_user_input(self) -> str:
        user_input = input("Your message: ")
        return user_input

class Streamlit:

    def __init__(self, title, description, prompt):
        # Initialize streamlit
        import streamlit as st
        self.st = st
        self.title = title
        self.description = description
        self.prompt = prompt

    def setup(self, process_input):
        image = Image.open('conf/bots/anne_frank.jpg')
        self.st.set_page_config(page_title=self.title, page_icon=image)
        self.st.header(self.title)

        self.st.image(image, caption=self.description)

        with self.st.expander("Prompt"):
            self.st.write(self.prompt.template)

        if "generated" not in self.st.session_state:
            self.st.session_state["generated"] = []

        if "past" not in self.st.session_state:
            self.st.session_state["past"] = []

        user_input = self.st.text_input("You: ", "Hi, how are you ?", key="input")

        if user_input:
            output = process_input(user_input)
            self.st.session_state.past.append(user_input)
            self.st.session_state.generated.append(output)

        if self.st.session_state["generated"]:
            from streamlit_chat import message
            for i in range(len(self.st.session_state["generated"]) - 1, -1, -1):
                message(self.st.session_state["generated"][i], key=str(i))
                message(self.st.session_state["past"][i], is_user=True, key=str(i) + "_user")