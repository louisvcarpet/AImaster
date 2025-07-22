from ai_mailroom.myllm import GetLLM
from ai_mailroom.node3_verify.oc_prompt import CHECKER_PROMPT 
from langchain_core.prompts import ChatPromptTemplate
import asyncio
from state import MailRoomState

class OutputChecker(GetLLM):

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
    ('human', "User_query: {user_request}\nResult: {result}")
])      

        chain = prompt_template | self.llm

       
        # formatted_prompt = prompt.format(user_request=UserInput)
    
        answer = await chain.ainvoke({"user_request": state.user_input , "result": state.result})


        #use y/n for condition checking 
        # if state.tryout >= 3 : 
        #     state.output_checker = "yes"
        #     return state.output_checker
        if answer.content.lower() == "yes":
            state.output_checker = "yes"
        elif answer.content.lower() == "no":
            state.output_checker = "no"
        
        return state

    async def __call__(self, state: MailRoomState):
        print("Running Output Checker...")
        return  await self.run(state)
    
    # mailbot("How many big packages does the mailroom have")

if __name__ == "__main__":
    # Example usage
    state = MailRoomState(user_input="How many big packages does the mailroom have?", result="There are 5 big packages in the mailroom.")
    output_checker = OutputChecker(prompt=CHECKER_PROMPT)
    asyncio.run(output_checker(state))
    print(state.output_checker)  # Should print "yes" or "no" based on the result verification
