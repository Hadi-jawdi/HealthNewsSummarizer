# 🩺 Health News Summarizer

A Python-based desktop application that fetches, summarizes, and reads aloud health news articles from the World Health Organization (WHO) RSS feed. Built with Tkinter and featuring text-to-speech capabilities.

## ✨ Features

- 📰 Fetches latest health news from WHO RSS feed
- 📝 Automatically summarizes articles using LSA (Latent Semantic Analysis)
- 🔊 Text-to-speech functionality with play/pause controls
- 🎯 Shows only important and relevant content
- 📱 Clean and modern user interface
- 🔄 Real-time news updates

## 🛠️ Requirements

- Python 3.x
- Required Python packages:
  - tkinter
  - feedparser
  - beautifulsoup4
  - sumy
  - pyttsx3
  - requests

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd health-news-summarizer
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Run the application:
```bash
python app.py
```

2. Click "🔄 Fetch News" to get the latest health news articles
3. Select an article from the list to view its summary
4. Use the "📄 Show Important Details" button to view the full article content
5. Use the "▶️ Read" button to start reading the content aloud
6. Use the "⏹️ Stop" button to stop the reading

## 🎯 Features in Detail

### News Fetching
- Automatically fetches the latest 10 health news articles from WHO
- Updates in real-time
- Handles connection errors gracefully

### Article Summarization
- Uses LSA (Latent Semantic Analysis) for intelligent summarization
- Extracts the most important sentences
- Maintains context and readability

### Text-to-Speech
- Clear and natural voice output
- Adjustable reading speed
- Play/pause functionality
- Thread-safe implementation

### Content Display
- Clean and organized layout
- Scrollable text areas
- Easy-to-read formatting
- Important content highlighting

## 🛠️ Technical Details

### Dependencies
- `tkinter`: GUI framework
- `feedparser`: RSS feed parsing
- `beautifulsoup4`: HTML parsing and content extraction
- `sumy`: Text summarization
- `pyttsx3`: Text-to-speech conversion
- `requests`: HTTP requests for article fetching

### Architecture
- Modular design with separate functions for:
  - News fetching
  - Content summarization
  - Text-to-speech
  - UI management
- Thread-safe implementation for smooth operation
- Error handling and user feedback


## �� Acknowledgments

- World Health Organization (WHO) for providing the RSS feed
- Python community for the amazing libraries
