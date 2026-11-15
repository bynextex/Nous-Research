# Nous Research Chat App

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](license.md)

A chat interface for models hosted on Nous Research API. Features multi-chat organization, system message templates, light and dark themes, bilingual UI (English / Turkish), and export tools for conversation history.

## Highlights

- Model selection: Hermes-3-Llama-3.1-405B, 70B, DeepHermes-3, and related variants
- Conversation organization: Create, rename, delete, and switch between separate chats
- Preset templates: Pre-configured system prompts for chain-of-thought, technical advisory, and writing
- Export support: Export conversation logs to JSON, PDF (via ReportLab), or CSV
- Token accounting: Shows session token counters and estimated cost calculations
- Bilingual UI: Instant toggle between English and Turkish

## Live Demo

Hosted Streamlit app: [nousresearch.streamlit.app](https://nousresearch.streamlit.app/)

## Local Setup

### Requirements

- Python 3.8+
- [Nous Research API key](https://portal.nousresearch.com/)

### Installation

```bash
git clone https://github.com/bynextex/Nous-Research.git
cd Nous-Research

pip install -r requirements.txt
streamlit run nous_chat_appv2.py
```

Enter your API key in the sidebar input to begin prompting models.

## Repository Structure

```text
Nous-Research/
├── nous_chat_appv2.py   # Main application
├── demo.py              # Minimal demo variant
├── roboto_fonts.py      # Base64 Roboto font definitions for PDF export
├── requirements.txt     # Python dependencies
├── license.md           # MIT License
└── README.md
```

## License

MIT License. See [license.md](license.md) for details.

Developed by [bynextex](https://github.com/bynextex) - [X: @kuntekul](https://x.com/kuntekul)
