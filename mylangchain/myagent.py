from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from mailbot_functions import db_packages_by_same_user as tool1 , db_total_by_size as tool2

# Define your tools
tool1 = Tool(
    name="PackagesByUser",
    func=tool1,  # your db_packages_by_same_user.run
    description="Get total packages for each user."
)
tool2 = Tool(
    name=" ",
    func=tool2,  # your db_total_by_size.run
    description="Get total packages by size (big, medium, small) for each user."
)

tools = [tool1, tool2]

# Initialize the agent
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # or other agent types
    verbose=True
)

# Now just pass the user request!
user_request = "how many big packages of Sean's does the mailroom contain"
result = agent.run(user_request)
print("MailBot:", result)