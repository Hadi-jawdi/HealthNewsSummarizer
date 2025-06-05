import tkinter as tk
from tkinter import ttk, messagebox
import feedparser
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import pyttsx3
import webbrowser
import requests
import re
import threading

# --- TTS ENGINE ---
def init_tts_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Slower speech rate for better comprehension
    return engine

engine = init_tts_engine()
current_summary = ""  # Global variable to store current summary text
current_article_url = ""  # Store current article URL
current_full_content = ""  # Store full article content
is_reading = False  # Flag to track reading state
reading_thread = None  # Thread for reading

def stop_reading():
    global is_reading, engine
    is_reading = False
    engine.stop()
    # Reinitialize the engine after stopping
    engine = init_tts_engine()

def read_current_content():
    global is_reading, reading_thread, engine
    
    if is_reading:
        stop_reading()
        return
    
    content = summary_box.get("1.0", tk.END).strip()
    if not content:
        messagebox.showinfo("Info", "No content to read.")
        return
    
    is_reading = True
    
    def reading_task():
        global engine
        try:
            engine.say(content)
            engine.runAndWait()
        except Exception as e:
            print(f"Reading error: {e}")
            # Reinitialize engine if there's an error
            engine = init_tts_engine()
        finally:
            is_reading = False
    
    reading_thread = threading.Thread(target=reading_task)
    reading_thread.start()

def clean_text(text):
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters and symbols
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()

def extract_important_content(soup):
    # Find the main content container
    main_content = None
    
    # Common content container classes/ids
    content_selectors = [
        'article', 'main', 'content', 'post', 'entry',
        '[class*="content"]', '[class*="article"]', '[class*="post"]',
        '[id*="content"]', '[id*="article"]', '[id*="post"]'
    ]
    
    for selector in content_selectors:
        main_content = soup.select_one(selector)
        if main_content:
            break
    
    if not main_content:
        main_content = soup.body
    
    # Remove unwanted elements
    for element in main_content.select('script, style, nav, header, footer, .ad, .advertisement, .sidebar, .comment, .share, .social, .menu, .navigation, .footer, .header'):
        element.decompose()
    
    # Get paragraphs
    paragraphs = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    # Extract and clean text
    content_parts = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if text and len(text) > 20:  # Only include substantial paragraphs
            content_parts.append(text)
    
    return '\n\n'.join(content_parts)

def fetch_full_article(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract important content
        important_content = extract_important_content(soup)
        
        # Clean and format the content
        cleaned_content = clean_text(important_content)
        
        # Create a structured format
        formatted_content = f"📰 Important Details:\n\n{cleaned_content}"
        
        return formatted_content
    except Exception as e:
        print(f"Error fetching article: {e}")
        return "Could not fetch the article content."

def show_full_article():
    if current_article_url:
        full_content = fetch_full_article(current_article_url)
        current_full_content = full_content
        
        summary_box.delete("1.0", tk.END)
        summary_box.insert(tk.END, full_content)
    else:
        messagebox.showinfo("Info", "No article URL available.")

# --- FETCH & SUMMARIZE NEWS ---

def get_news():
    url = "https://www.who.int/rss-feeds/news-english.xml"  # WHO health news RSS
    feed = feedparser.parse(url)

    if feed.bozo:
        print("Feedparser error:", feed.bozo_exception)
        messagebox.showerror("Error", "Couldn't fetch news. Please check your internet connection.")
        return

    if not feed.entries:
        messagebox.showinfo("Info", "No news found.")
        return

    news_list.delete(0, tk.END)
    articles.clear()

    for entry in feed.entries[:10]:
        title = entry.title
        content = entry.summary if hasattr(entry, 'summary') else entry.description
        link = entry.link if hasattr(entry, 'link') else ""
        soup = BeautifulSoup(content, "html.parser")
        clean_text = soup.get_text()
        articles.append((title, clean_text, link))
        news_list.insert(tk.END, title)

def summarize_article(event):
    global current_summary, current_article_url
    index = news_list.curselection()
    if not index:
        return
    index = index[0]
    title, content, url = articles[index]
    current_article_url = url

    parser = PlaintextParser.from_string(content, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, 3)

    summary_text = "\n".join(str(sentence) for sentence in summary_sentences)
    current_summary = summary_text  # store for TTS

    summary_box.delete("1.0", tk.END)
    summary_box.insert(tk.END, f"📰 {title}\n\n{summary_text}")

# --- UI SETUP ---

root = tk.Tk()
root.title("🩺 Health News Summarizer + TTS")
root.geometry("1000x800")  # Increased window size
root.configure(bg="#f2f8fc")

# Configure style
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TLabel", font=("Segoe UI", 12))
style.configure("TFrame", background="#f2f8fc")

# Main container
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill="both", expand=True)

# Title
title_label = ttk.Label(main_frame, text="📰 Health News Summarizer", font=("Segoe UI", 24, "bold"))
title_label.pack(pady=(0, 20))

# Button frame
btn_frame = ttk.Frame(main_frame)
btn_frame.pack(pady=(0, 20))

ttk.Button(btn_frame, text="🔄 Fetch News", command=get_news).grid(row=0, column=0, padx=10)
ttk.Button(btn_frame, text="📄 Show Important Details", command=show_full_article).grid(row=0, column=1, padx=10)
ttk.Button(btn_frame, text="▶️ Read", command=read_current_content).grid(row=0, column=2, padx=10)
ttk.Button(btn_frame, text="⏹️ Stop", command=stop_reading).grid(row=0, column=3, padx=10)

# News list frame with scrollbar
news_frame = ttk.Frame(main_frame)
news_frame.pack(fill="both", expand=True, pady=(0, 20))

news_scrollbar = ttk.Scrollbar(news_frame)
news_scrollbar.pack(side="right", fill="y")

news_list = tk.Listbox(news_frame, 
                      height=12,
                      font=("Segoe UI", 11),
                      selectmode=tk.SINGLE,
                      yscrollcommand=news_scrollbar.set,
                      width=80,
                      bg="white",
                      selectbackground="#0078D7",
                      selectforeground="white")
news_list.pack(side="left", fill="both", expand=True)
news_scrollbar.config(command=news_list.yview)
news_list.bind("<<ListboxSelect>>", summarize_article)

# Summary frame with scrollbar
summary_frame = ttk.Frame(main_frame)
summary_frame.pack(fill="both", expand=True)

summary_scrollbar = ttk.Scrollbar(summary_frame)
summary_scrollbar.pack(side="right", fill="y")

summary_box = tk.Text(summary_frame,
                     wrap="word",
                     font=("Segoe UI", 12),
                     height=15,
                     yscrollcommand=summary_scrollbar.set,
                     bg="white",
                     padx=10,
                     pady=10)
summary_box.pack(side="left", fill="both", expand=True)
summary_scrollbar.config(command=summary_box.yview)

# Footer
footer_label = ttk.Label(main_frame, 
                        text="Made with ❤️ by Hadi for Code in Place",
                        font=("Segoe UI", 10, "italic"))
footer_label.pack(pady=(20, 0))

articles = []

root.mainloop()
