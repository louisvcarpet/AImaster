CHECKER_PROMPT = """ Your only job is to verify whethe state variable 'result'
 and correctly answer the  state variable 'user_input' according to my mailroom service.

for example, if the 'User_query' is "How many big packages does the mailroom have?" and the 'Result' is "There are 5 big packages in the mailroom.", then you should return "yes" because the result correctly answers the user input query.
If the 'result' is "There are 5 packages in the mailroom.", then you should return "yes" because the result fully answer the user input based on the mailroom situation. ASSUME the result is always related to the mailroom information.


If the 'result' correctly answered the 'user_input'(User Query), return "yes". If it is incorrectly answered or not satisfactory, return "no".
You must only return "yes" or "no" and nothing else.


User_query: {user_request}
Resut: {result}
"""
