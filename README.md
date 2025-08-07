# Voice Agent SDK: Multi-Agent Voice Assistant (OpenAI Agents SDK)

A comprehensive project for building a multi-agent voice assistant system using the OpenAI Agents SDK, featuring both a Command-Line Interface (CLI) and a professional Streamlit web application. This project demonstrates how to create, configure, and extend multiple AI agents with tool integrations, handoff logic, and advanced voice features.

---

## 🚀 Project Overview

- **Multi-Agent System**: Build and manage several AI agents (e.g., Weather, Spanish, Urdu) using the OpenAI Agents SDK.
- **Tools Integration**: Extend agent capabilities with custom tools (e.g., weather info, translation).
- **Agent Handoffs**: Seamlessly transfer conversations between agents based on context or user intent.
- **Voice Features**: Record, transcribe, and synthesize voice for natural, interactive experiences.
- **Two Versions**: Use either a CLI or a Streamlit-based UI for interaction.

---

## 🛠️ Features

- **Voice Input/Output**: Record your voice, transcribe it, and get AI responses as both text and audio.
- **Multi-Language Agents**: Includes agents for weather, Spanish, and Urdu conversations.
- **Secure API Key Handling**: Enter and manage your OpenAI API key securely (session state only).
- **Agent Handoffs**: Agents can hand off tasks to each other (e.g., from general to weather agent).
- **Custom Tools**: Integrate external APIs (like weather) as agent tools.
- **CLI & Streamlit UI**: Choose between a terminal-based or web-based experience.
- **Modern UI**: Streamlit app features a responsive, professional design.

---

## 📂 File Structure

```
voice-agent-sdk/
├── agents_setup.py      # Agent definitions, handoff logic, and setup
├── cli.py               # CLI version: interact with agents via terminal
├── config.py            # Configuration and environment variable handling
├── streamlit_app.py     # Streamlit web application (main UI)
├── tools.py             # Custom tools (e.g., weather API integration)
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project metadata
├── README.md            # Project documentation
└── ...                  # __pycache__, lock files, etc.
```

---

## 🖥️ CLI Version

Interact with your agents directly from the terminal.

### Run the CLI
```bash
python cli.py
```

- Enter your OpenAI API key when prompted.
- Select an agent and start a conversation.
- Use voice or text input (if supported).
- Agents can hand off tasks to each other automatically.

---

## 🌐 Streamlit Web App

A modern, interactive web UI for your multi-agent system.

### Run the Streamlit App
```bash
streamlit run streamlit_app.py
```

- Enter your OpenAI API key in the sidebar.
- Select an agent from the dropdown.
- Click "Start Recording" and speak into your microphone.
- View and listen to AI responses in real time.
- Enjoy a professional, customizable UI.

---

## 🧩 How It Works

1. **Agent Setup**: Agents are defined in `agents_setup.py` using the OpenAI Agents SDK. Each agent can have unique instructions, tools, and handoff logic.
2. **Tools Integration**: Tools (e.g., weather API) are implemented in `tools.py` and registered with agents.
3. **Voice Pipeline**: The app records your voice, transcribes it (using OpenAI or other ASR), and sends it to the selected agent. The agent's response is synthesized back to audio.
4. **Agent Handoffs**: Agents can transfer control to each other based on conversation context (e.g., language switch, weather request).
5. **UI Layer**: Choose between CLI (`cli.py`) or Streamlit (`streamlit_app.py`) for interaction.

---

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd voice-agent-sdk
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **(Optional) Set Environment Variables**
   - Create a `.env` file for API keys (e.g., `WEATHER_API_KEY=...`).

---

## ⚙️ Customization & Extensibility

### Adding New Agents
- Edit `agents_setup.py` and add a new agent definition using the OpenAI Agents SDK.
- Register new tools in `tools.py` and link them to agents.
- Update handoff logic as needed for new agent types.

### Extending Tools
- Implement new tool classes/functions in `tools.py`.
- Register them with agents in `agents_setup.py`.

### UI Customization
- For CLI: Edit `cli.py` for new commands or flows.
- For Streamlit: Edit `streamlit_app.py` for UI/UX changes, styling, or new features.

---

## 🔒 Security Notes

- API keys are never stored permanently; only in session or environment variables.
- All voice and text data is processed locally or via secure OpenAI APIs.
- The app runs locally by default.

---

## ❓ Troubleshooting

- **Microphone Issues**: Check permissions and device selection.
- **Audio Playback**: Ensure speakers/headphones are connected and browser allows playback.
- **API Errors**: Verify API keys and internet connection.
- **Recording Issues**: Adjust recording duration/settings in the UI.

---

## 📄 License

This project is licensed under the same terms as your original voice agent project.

---

## 🙋‍♂️ Support

- Check browser console or terminal for errors.
- Verify API keys and credits.
- Test microphone and audio in other apps.
- Ensure all dependencies are installed.

---

## References
- [OpenAI Agents SDK Documentation](https://platform.openai.com/docs/assistants/agents)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python SpeechRecognition](https://pypi.org/project/SpeechRecognition/)

---