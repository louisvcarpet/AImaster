from state import MailRoomState
from langchain_core.runnables import Runnable
import asyncio

class testDisplay:

    async def __call__(self, state: MailRoomState):
        """The only job here is to display the state result. It will be called by the fronend and return the result."""
        print("State in display:", state)
        return state
        # Here you can add more logic to format or present the result as needed

if __name__ == "__main__":

    # Example usage
    state = MailRoomState(user_input="How many big packages does the mailroom have?")
    state.result = "There are 5 big packages in the mailroom."
    tester = testDisplay()
    asyncio.run(tester(state))
    
    

    
   