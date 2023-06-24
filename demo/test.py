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


llm = OpenAI(temperature=0, openai_api_key="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")
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
tools = [
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    )
]

db = SQLDatabase.from_uri("postgresql://valentin:margera@localhost:5433/postgres", include_tables=['patients', 'dentists', 'appointments'], sample_rows_in_table_info=2)

query_response_limit = 1
db_chain = SQLDatabaseSequentialChain.from_llm(llm, db, verbose=True, top_k=query_response_limit, use_query_checker=True)

tools.append(
    Tool(
        name="Dentist-DB",
        func=db_chain.run,
        description="useful for when you need add an appointment, modify it or remove it or add dentist, modify it or remove it, or add a patient, modify it or remove it or seeing the relation between the patient the doctor and the appoitments. Input should be in the form of a question containing full context",
    )
)

model = ChatOpenAI(temperature=0, openai_api_key="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")
planner = load_chat_planner(model)
executor = load_agent_executor(model, tools, verbose=True)
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

agent.run("Give me an appointment with Dr. Anderson for tomorrow at 10am.")