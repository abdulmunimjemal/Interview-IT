import time
import asyncio
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.output_parser import StrOutputParser 
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

load_dotenv()


# Prompt Engineering

system_template = (
    "You are an interviewer for a technical position, conducting a Data Structures and Algorithms (DSA) interview."
    "The candidate has been given the following problem to solve: \n{challenge}\n"
    "Your responsibilities include presenting the problem, tracking the time allotted ({total_time} minutes), assessing the candidate's approach, and evaluating their solution."
    "The candidate is actively working on the problem and may request hints or clarifications. They will notify you when they are ready to submit their solution."
    "Please remind the candidate to manage their time effectively within the allotted time."
    "REMINDER: Use Interview Conversational Tone and provide constructive feedback to the candidate."
)

candidate_template = (
    "Current Time: {current_time} minutes\n"
    "Current User's Attempted Code: \n```{current_attempt}```\n"
    "If the user is ready to submit their solution, they should type 'submit'. Otherwise, they can request hints or clarifications as long as they have time remaining."
    "If the user runs out of time, the interviewer will assess their current solution and provide feedback."
    "If the user submits their solution before time runs out, the interviewer will evaluate their solution and provide feedback."
    "Consider the following dimensions when evaluating their solution: Problem-Solving Approach Algorithmic Efficiency, Code Quality, Efficiency in Implementation, Communication, Time Management, Adaptability, Overall Performance"
)

# Variables of the template:
# {challenge} - the problem statement
# {total_time} - the total time allotted for the interview
# {current_time} - the current time elapsed in the interview
# {current_attempt} - the current code attempt by the candidate
# {chat_history} - the chat history between the interviewer and the candidate

interviewer_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        MessagesPlaceholder("chat_history"),
        ("human", candidate_template),
    ]
)

llm = ChatOpenAI(model="gpt-4o-mini")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
interview_chain = interviewer_template | llm | StrOutputParser()

problem = """
27. Remove Element (Easy)

Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The order of the elements may be changed. Then return the number of elements in nums which are not equal to val.

Consider the number of elements in nums which are not equal to val be k, to get accepted, you need to do the following things:

Change the array nums such that the first k elements of nums contain the elements which are not equal to val. The remaining elements of nums are not important as well as the size of nums.
Return k.

You can use any programming language to solve this problem.
"""

total_time = 45


async def main():
    start_time = time.time()
    round = 0
    print("Welcome to the DSA Interview Simulator!")
    print(f"Hello, You have to solve the following problem in {total_time} minutes: \n{problem}\n\n")

    while True:
        elapsed_time = int(time.time() - start_time)
        user_input = input(f"[{round}] Current Time (You enter for now): {elapsed_time}/{total_time} minutes\n"
                           f"[{round}] Your Attempt: \n")

        if user_input == "submit":
            user_input = "The candidate has submitted their solution. Please check the history and evaluate their final submission."

        variables = {"challenge": problem, "total_time": total_time, "current_time": elapsed_time,
                     "current_attempt": user_input, "chat_history": memory.buffer_as_messages}

        ai_response = await interview_chain.ainvoke(variables)
        print("AI: ", ai_response)
        input("Press Enter to continue...")

        memory.chat_memory.add_user_message(f"Time: {elapsed_time}/{total_time} minutes \n\n Attempt: \n ```{user_input}```")
        memory.chat_memory.add_ai_message(ai_response)

        round += 1

if __name__ == "__main__":
    asyncio.run(main())