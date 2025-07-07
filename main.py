import os
import asyncio
from dotenv import load_dotenv
import chainlit as cl
from typing import cast
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load environment variables
load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
# print("api key loaded", openrouter_api_key)

if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

@cl.on_chat_start
async def start():
    # Setup client and model
    client = AsyncOpenAI(
        api_key=openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
        "Authorization": f"Bearer {openrouter_api_key}"
    }
    )

    model = OpenAIChatCompletionsModel(
        model="meta-llama/llama-3.3-8b-instruct:free",
        openai_client=client
    )

    config = RunConfig(
        model=model,
        model_provider=client,
        tracing_disabled=True
    )

    agent = Agent(
        name="Smart Student Assistant",
        instructions="""
You are a smart and friendly student assistant created by **Danish Abbasi**.

You help students by:
- Answering academic questions clearly.
- Giving motivational and practical study tips.
- Summarizing text in simple words with bullet points.

Always be supportive, clear, and concise. If you don't know something, politely admit it.
""",
        model=model
    )

    # Save to session
    cl.user_session.set("agent", agent)
    cl.user_session.set("config", config)
    cl.user_session.set("chat_history", [])

    # Your custom welcome message
    await cl.Message(
        content="""
# 🎓 **Smart Student Assistant**  
📚 Your friendly academic AI buddy — powered by **OpenRouter AI**

💡 **What I can help you with:**  
- 🧠 Answer your **academic questions** in simple terms  
- ✍️ Give **motivational & practical study tips**  
- 📑 **Summarize text** into easy bullet points  
- 🤝 Be your 24/7 study companion

✨ Designed to explain complex topics clearly, with a positive tone — always focused, supportive, and student-friendly.

---

👨‍💻 **Created by: _Danish Abbasi_**  
🔗 Powered by **meta-llama/llama-3.3-8b-instruct:free**

🎯 Ask anything now to get started!
"""
    ).send()


@cl.on_message
async def main(message: cl.Message):
    thinking_msg = cl.Message(content="🧠 Thinking...")
    await thinking_msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
    history = cl.user_session.get("chat_history") or []

    # Append user input
    history.append({"role": "user", "content": message.content})

    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=history,
            run_config=config
        )
      
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, 'delta'):
                token = event.data.delta
                await thinking_msg.stream_token(token)  
        cl.user_session.set("chat_history", result.to_input_list())

    except Exception as e:
        thinking_msg.content = f"❌ Error: {str(e)}"
        await thinking_msg.update()
        print(f"[ERROR] {e}")