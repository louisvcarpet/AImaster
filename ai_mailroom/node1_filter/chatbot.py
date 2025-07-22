from ai_mailroom.myllm import GetLLM
from ai_mailroom.node1_filter.request_prompt import FILTER_PROMPT 
from langchain_core.prompts import ChatPromptTemplate
import asyncio
from state import MailRoomState

class MailRoomChatBot(GetLLM):

    def __init__(self, prompt):
        super().__init__(prompt=prompt)
        self.llm = self.get_llm()

    async def run(self, state: MailRoomState):
        # llm = LlmBase()
        # answer = llm.ainvoke({UserInput})
        # return answer 
        # llm = LlmBase()
        prompt_template = ChatPromptTemplate.from_messages([
    ('system', self.prompt),
    ('human', "{user_request}")
    ])

        chain = prompt_template | self.llm

        user_input = input("Hi I'm your Mailbot, how can I help you today?\n User Query: ")
        # user_input = "give me the total amount of big packages in the mailroom"
        # user_input = "give me the total amount of packages for Frank Lin the mailroom"
        state.user_input = user_input
    
        # formatted_prompt = prompt.format(user_request=UserInput)
    
        answer = await chain.ainvoke({"user_request": user_input})

        #use y/n for condition checking 
        while(answer.content == "Sorry I can only answer questions related to the mailroom information."):
            user_input = input("Sorry I can only answer questions related to the mailroom information. Please ask again.\n User Query: ")
            answer = await chain.ainvoke({"user_request": user_input})
        print(answer.content)
        return state 

    async def __call__(self, state):
        return await self.run(state)
    
    # mailbot("How many big packages does the mailroom have")

