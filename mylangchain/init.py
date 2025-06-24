from langchain_core.runnables import RunnableLambda
from mailbot_functions import db_total_by_size as a
from mailbot_functions import db_loader


def go(size: str) -> str:
    return a.run(size)
test_runnable = RunnableLambda(lambda input: go(input))

result = test_runnable.invoke("big")
print(result)