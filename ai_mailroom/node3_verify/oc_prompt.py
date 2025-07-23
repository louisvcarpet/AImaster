CHECKER_PROMPT = """ Your only job is to verify whethe state variable 'result'
 and correctly answer the  state variable 'user_input' according to my mailroom service. 

 *** if the 'user_query' is related to any form of package creation such as help me to add/create/register a package, you must return "yes" if the 'result' has "Package created successfully".

Case A: 
for example, if the 'User_query' is "How many big packages does the mailroom have?" and the 'Result' is "There are 5 big packages in the mailroom.", then you should return "yes" because the result correctly answers the user input query.
If the 'result' is "There are 5 packages in the mailroom.", then you should return "yes" because the result fully answer the user input based on the mailroom situation. ASSUME the result is always related to the mailroom information.

Case B:
You must handle queries about recipients and date ranges, such as:
- "How many packages does this recipient have within XXX days?"
- "How many packages does [recipient] have since [specific date]?"
- "How many packages does [recipient] have after [date]?"

**Guidelines:**
- If the 'result' provides a count, a list, or a table of packages for the specified recipient and date range, return "yes".
- If the 'result' says "No packages found for [recipient] after [date].", return "yes".
- If the 'result' lists packages (with type, size, delivery_date, etc.) for the recipient after the specified date, return "yes".
- If the 'result' gives a summary like "[Recipient] has X packages delivered after [date].", return "yes".
- Assume the result is always related to the mailroom information.

**Examples:**

Example A:
User_query: "How many big packages does the mailroom have?"
Result: "There are 5 big packages in the mailroom."
→ Return "yes"

Example B:
User_query: "How many packages does Frank Lin have within 2 months?"
Result: "Frank Lin has 3 packages delivered after 2025-05-19:\n  type  size delivery_date\n   box   big    2025-06-17\nwooden crate   big    2025-06-17\nenvelope small    2025-06-17"
→ Return "yes"

Example C:
User_query: "How many packages does Rachel Chang have after 2025-07-23?"
Result: "No packages found for Rachel Chang after 2025-07-23."
→ Return "yes"

Example D:
User_query: "How many packages does Frank Lin have after 2025-05-19?"
Result: "Frank Lin has 3 packages delivered after 2025-05-19."
→ Return "yes"

******
If the 'result' correctly answered the 'user_input'(User Query), return "yes". If it is incorrectly answered or not satisfactory, return "no".
You must only return "yes" or "no" and nothing else.*****


User_query: {user_request}
Resut: {result}
"""
