# Antaraa - Therapeutic Companion

Antaraa (अन्तरा) is an AI-powered therapeutic companion designed to provide emotional support through conversational interactions. Meaning "Inner Space" in Sanskrit, Antaraa creates a safe sanctuary for self-reflection and emotional exploration.

![Antaraa Interface](https://github.com/user-attachments/assets/09765606-01d4-478e-989f-970e7dc9df73)

## Features

- **Compassionate AI Conversations**: Engage in therapeutic dialogue with a supportive companion
- **Privacy-First Design**: Conversations are never stored or recorded
- **Crisis Support**: Automatic detection of distress signals with immediate resource provision
- **Session Management**: Start new conversations or export session transcripts
- **Reflection Tools**: Built-in prompts for self-exploration
- **Minimalist Interface**: Clean design for distraction-free interaction

## Getting Started

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/antaraa.git
cd antaraa
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenRouter API key:

```bash
OPENROUTER_API_KEY="your_api_key_here"
```

### Usage

Run the application:

```bash
streamlit run app.py
```

The application will open in your default browser at http://localhost:8501

## How It Works

Antaraa uses AI models through OpenRouter's API to power therapeutic conversations, any openai compatiable api can be used. The application:

- Creates a safe space for emotional expression
- Provides thoughtful responses using therapeutic principles
- Detects crisis keywords to offer immediate support resources
- Maintains complete privacy with no data storage

## Configuration
Customize your experience by modifying:

AI model selection in MODEL
Conversation starter messages
Crisis detection keywords and resources
Interface branding elements
