from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableLambda
from mailbot_functions.db_packages_by_same_user import run as t1
from mailbot_functions.db_total_by_size import run as t2
from mailbot_functions.mailbot_prompt import User_Prompt,  TEST_PROMPT
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Define the model as a Runnable
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0,
    api_key=os.environ.get("OPENAI_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ('system', TEST_PROMPT),
    ('human', "{context}\n{user_request}")
])

tool2 = RunnableLambda(t2)

chain =  prompt | model

def ask(chain, request):
    # Wrap the question as a SystemMessage (or HumanMessage if you prefer)
    # messages = [SystemMessage(content=question)]
    result = chain.invoke(request)
    return result.content

if __name__ == "__main__":
    user_request = "how many small packages of Sean's does the mailroom contain and print me the relavant dataset"
   # how many big packages do the mailroom contain 
   # I am Micheal Jordan
    answer = ask(chain, {"user_request": user_request, "context":t2(user_request)})
    print("MailBot:", answer)

