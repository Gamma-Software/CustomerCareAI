from langchain import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain, SQLDatabaseSequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain import (
    LLMMathChain,
    OpenAI,
    SQLDatabase,
    SQLDatabaseChain
)
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

from careai.core.memory import load_long_term_memory
from careai.utils.configuration import Config
from careai.core.prompts import load_character_info, adapt_prompt


class CareaiBot:

    # Initialize the prompt and llm chain
    def __init__(self, conf: Config):
        self.agent = self.test2(conf)

    def test1(self, conf):

        memory = ConversationBufferMemory(memory_key="chat_history")

        llm=OpenAI(temperature=0, verbose=True, openai_api_key=conf.open_ai_api_key)

        llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

        _DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Use the following format:

        Question: "Question here"
        SQLQuery: "SQL Query to run"
        SQLResult: "Result of the SQLQuery"
        Answer: "Final answer here"

        Only use the following tables:

        {table_info}

        If someone asks for the table foobar, they really mean the employee table.

        Question: {input}"""
        PROMPT = PromptTemplate(
            input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
        )
        db = SQLDatabase.from_uri("postgresql://valentin:margera@localhost:5433/postgres", include_tables=['patients', 'dentists', 'appointments'], sample_rows_in_table_info=2)

        query_response_limit = 3
        db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True, top_k=query_response_limit)

        tools = [
            Tool(
                name="Calculator",
                func=llm_math_chain.run,
                description="useful for when you need to answer questions about math",
            ),
            Tool(
                name="Dentist-DB",
                func=db_chain.run,
                description="useful for when you need add an appointment, modify it or remove it or add dentist, modify it or remove it, or add a patient, modify it or remove it or seeing the relation between the patient the doctor and the appoitments. Input should be in the form of a question containing full context",
            ),
        ]


        return initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

    def test2(self, conf):
        llm = OpenAI(temperature=0, verbose=True, openai_api_key=conf.open_ai_api_key)
        llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
        db = SQLDatabase.from_uri("postgresql://valentin:margera@localhost:5433/postgres", include_tables=['patients', 'dentists', 'appointments'], sample_rows_in_table_info=2)

        query_response_limit = 1
        db_chain = SQLDatabaseSequentialChain.from_llm(llm, db, verbose=True, top_k=query_response_limit, use_query_checker=True)

        tools = [
            Tool(
                name="Calculator",
                func=llm_math_chain.run,
                description="useful for when you need to answer questions about math",
            ),
            Tool(
                name="Dentist-DB",
                func=db_chain.run,
                description="useful for when you need add an appointment, modify it or remove it or add dentist, modify it or remove it, or add a patient, modify it or remove it or seeing the relation between the patient the doctor and the appoitments. Input should be in the form of a question containing full context",
            ),
        ]

        model = ChatOpenAI(temperature=0, verbose=True, openai_api_key=conf.open_ai_api_key)
        SYSTEM_PROMPT = (
            "Let's first understand the problem and devise a plan to solve the problem."
            " Please output the plan starting with the header 'Plan:' "
            "and then followed by a numbered list of steps. "
            "Please make the plan the minimum number of steps required "
            "to accurately complete the task. If the task is a question, "
            "the final step should almost always be 'Given the above steps taken, "
            "please respond to the users original question'. "
            "At the end of your plan, say '<END_OF_PLAN>'"
        )
        planner = load_chat_planner(model, SYSTEM_PROMPT)
        executor = load_agent_executor(model, tools, verbose=True)
        return PlanAndExecute(planner=planner, executor=executor, verbose=True)

    def process_input(self, user_input):
        """Process user input and display response or error message

        Args:
            chatgpt_chain (_type_): _description_
            user_input (_type_): _description_

        Returns:
            Bool: True if the process ended correctly
            Str:  AI message (Could be an error message)
        """
        try:
            response = self.agent.run(user_input)
            return True, response
        except Exception as e:
            print(e)
            error_message = "AI Assistant encountered an error. Please try again later."
            print(error_message)
            return False, error_message
