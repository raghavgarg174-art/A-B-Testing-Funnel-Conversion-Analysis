# Chatbot

An interactive chatbot application built using Python. This chatbot features a user-friendly GUI built with Tkinter, and it supports advanced functionalities like text-to-speech (TTS), file handling, mathematical computations, and basic natural language processing (NLP) for conversation handling.

---

## Features

1. **Basic Conversations**: Handles greetings, general queries, and personalized interactions.
2. **Text-to-Speech (TTS)**: Speaks responses using a default voice (male/female dependson availability).
3. **Mathematical Computations**: Perform simple calculations (e.g., `calculate 2+2`).
4. **Open Files or Applications**: Opens specified files or applications on your system (e.g., `open notepad`).
5. **Jokes**: Shares random jokes to entertain users.
6. **Typing Effect**: Simulates a typing effect for chatbot responses.
7. **Personalization**: Remembers the user's name during the session.
8. **GUI-Based Interaction**: Easy-to-use graphical interface with a scrolled text area for chat history.

---

## Tech Stack

- **Programming Language**: Python
- **GUI Library**: Tkinter
- **Speech Engine**: pyttsx3 (for text-to-speech)
- **Natural Language Processing**: NLTK Chat module
- **File & Process Handling**: os, subprocess modules
- **Other Utilities**: re (for regex), datetime, and math libraries

---

## Usage
- **Launch the Chatbot:** Run the application using the command python src/main.py.
- **Chat:** Type your query or message in the input box and press Send to interact with the chatbot.
- **Perform Calculations:** Use the calculate command, followed by the expression, e.g., calculate 10 * 5.
- **Open Applications/Files:** Use the open command, followed by the name of the application or file path, e.g., open notepad.
- **Clear Chat History:** Press the Clear button to reset the conversation.
- **Exit the Chatbot:** Type bye or close the application window.

---

## Prerequisites

1. Python 3.7 or later.
2. Required Python libraries listed in `requirements.txt`.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/heatblaze/Chatbot.git
   
