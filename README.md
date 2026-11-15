# Nous Research Chat App 🧠

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](license.md)

A feature-rich chat application powered by [Nous Research](https://nousresearch.com/) models. Supports multiple conversations, system prompt templates, dark/light themes, bilingual interface (EN/TR), and export to JSON, PDF, and CSV.

---

## ✨ Features

- **Multi-Model Selection** — Choose from Hermes-3-Llama-3.1-405B, 70B, DeepHermes-3, and more
- **Conversation Management** — Create, rename, delete, and switch between multiple chats
- **System Message Templates** — Pre-built templates (Chain of Thought, Expert Advisor, SEO Expert) or custom system prompts
- **Dark/Light Theme** — Toggle between comfortable viewing modes
- **Bilingual Interface** — Full English and Turkish language support
- **Export Options** — Save conversations as JSON, PDF, or CSV
- **Token Usage Tracking** — Monitor token consumption and estimated costs
- **Adjustable Parameters** — Fine-tune temperature (0.0–2.0) and max tokens

## 🌐 Try It Online

👉 [nousresearch.streamlit.app](https://nousresearch.streamlit.app/)

Enter your Nous API key in the sidebar and start chatting immediately.

## 🚀 Local Setup

### Prerequisites

- Python 3.8+
- A [Nous Research API key](https://portal.nousresearch.com/)

### Installation

```bash
# Clone the repository
git clone https://github.com/bynextex/Nous-Research.git
cd Nous-Research

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run nous_chat_appv2.py
```

Open your browser at `http://localhost:8501` and enter your API key in the sidebar.

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Web UI framework |
| **Nous Research API** | LLM inference (Hermes-3 family) |
| **ReportLab** | PDF export with Unicode support |
| **Pandas** | CSV data export |

## 📁 Project Structure

```
Nous-Research/
├── nous_chat_appv2.py   # Main application (full-featured)
├── demo.py              # Simple demo version
├── roboto_fonts.py      # Base64-encoded Roboto fonts for PDF
├── requirements.txt     # Python dependencies
├── license.md           # MIT License
└── .devcontainer/       # Dev container config
```

## 🔒 Privacy & Security

- API keys are **not** stored between sessions
- All data stays local in your browser
- No data sent anywhere except Nous Research API endpoints

## 📸 Screenshots

> Coming soon — contributions welcome!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License — see [license.md](license.md) for details.

## 👨‍💻 Author

Built by [@bynextex](https://github.com/bynextex) | [X/Twitter](https://x.com/muma_gaga)
