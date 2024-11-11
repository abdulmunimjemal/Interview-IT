from groq import AsyncGroq
import asyncio
from app.templates import load_prompt_template

# client = AsyncGroq()


async def generate_response(transcription: str) -> str:

    prompt_template = load_prompt_template("prompt.txt")
    prompt = prompt_template.format(transcription=transcription)

    # Fake LLM response generation
    await asyncio.sleep(1)  # Simulating async call

    # chat_completion = await client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": "Explain the importance of low latency LLMs",
    #         }
    #     ],
    #     model="llama3-8b-8192",
    # )
    # print(chat_completion.choices[0].message.content)

    return f"LLM Response to: {transcription}"