# Smart Student Assistant

A friendly academic AI chatbot built with [Chainlit](https://www.chainlit.io/) and powered by OpenRouter's Llama-3 model. Designed to help students with academic questions, study tips, and text summarization in a supportive, easy-to-understand way.

---

## Features

- **Academic Q&A:** Answers student questions in simple, clear language.
- **Study Tips:** Provides motivational and practical advice for effective studying.
- **Text Summarization:** Summarizes complex text into easy bullet points.
- **Positive Tone:** Always supportive, concise, and student-friendly.
- **Session Memory:** Remembers chat history for context-aware responses.

---

## How It Works

- On chat start, the app:
  - Loads your OpenRouter API key from the `.env` file.
  - Initializes the Llama-3 model via OpenRouter.
  - Sets up a custom agent with helpful instructions.
  - Greets the user with a welcome message.

- On each user message:
  - Appends the message to the chat history.
  - Runs the agent with the full conversation context.
  - Streams the response back to the user with a typewriter effect.
  - Updates the chat history for continuity.

---

## Setup & Usage

1. **Clone the repository**
2. **Install dependencies** (see `pyproject.toml`)
3. **Create a `.env` file** with your OpenRouter API key:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```
4. **Run the app** (typically with `chainlit run main.py`)
5. **Chat with your AI assistant!**

---

## Customization
- Edit the agent's instructions in `main.py` to change its personality or expertise.
- Change the model or provider as needed.

---

## Credits
- **Created by:** Danish Abbasi
- **Powered by:** meta-llama/llama-3.3-8b-instruct:free via OpenRouter
- **Framework:** [Chainlit](https://www.chainlit.io/)

---

## License
MIT (or specify your license here)
