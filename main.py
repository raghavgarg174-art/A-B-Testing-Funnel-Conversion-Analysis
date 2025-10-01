import tkinter as tk
from tkinter import scrolledtext
from tkinter import font as tkFont
import random
import pyttsx3
import os
import subprocess
import re
from nltk.chat.util import Chat, reflections
from datetime import datetime
import time
import math

# Initialize the Text-to-Speech engine
engine = pyttsx3.init()

# Set the voice to female (on most systems, 'female' is available)
voices = engine.getProperty('voices')
female_voice = None

# Find a female voice, if available
for voice in voices:
    if 'female' in voice.name.lower():  # Checks if the voice is female
        female_voice = voice
        break

# Set the engine's voice to the selected female voice, if found
if female_voice:
    engine.setProperty('voice', female_voice.id)
else:
    print("No female voice found. Using default voice.")

# Define pairs of patterns and responses for the NLP chatbot
pairs = [
    (r"hi|hello", ["Hello! How can I assist you today?", "Hi there! What can I do for you today?"]),
    (r"how are you?",
     ["I'm doing well, thank you for asking! How about you?", "I'm great, thanks for asking! How are you?"]),
    (r"my name is (.*)", ["Nice to meet you, %1!", "Hello %1, it's a pleasure to meet you!"]),
    (
    r"(.*) your name?", ["I am a chatbot created to assist you!", "I don't have a name, but you can call me Chatbot!"]),
    (r"(.*) help|assist", ["Sure! I can assist you with general queries like greetings, weather, or even jokes.",
                           "How can I help you today?"]),
    (r"(.*) (joke|funny)", ["Why don’t skeletons fight each other? They don’t have the guts.",
                            "Why did the math book look sad? Because it had too many problems."]),
    (r"(.*) (weather|forecast)",
     ["Sorry, I can't check the weather right now, but I can assist you with other things."]),
    (r"bye", ["Goodbye! Have a wonderful day!", "See you later, take care!"]),
    (r"(.*) calculate (.*)", ["Calculating that now...", "Let me do that math for you..."]),
    (r"(.*) (list|functions|capabilities|do you do)", [
        "Here are the things I can do:\n"
        "1. Answer your greetings.\n"
        "2. Tell jokes and fun facts.\n"
        "3. Perform simple mathematical calculations (e.g., 2+2).\n"
        "4. Open files, folders, or applications on your system.\n"
        "5. Assist with general questions and queries.\n"
        "6. And much more! Just ask away."]),
]

# Global variable for storing user's name and conversation history
user_name = ""
conversation_history = []


# Function for chatbot's text-to-speech response
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Typing effect simulation for chatbot response
def typing_effect(text, delay=0.05):
    for char in text:
        chat_history.insert(tk.END, char)
        chat_history.yview(tk.END)
        chat_history.update()
        time.sleep(delay)
    chat_history.insert(tk.END, "\n")
    chat_history.config(state=tk.DISABLED)


# Create the function for chatbot responses
def chatbot_response(user_input):
    global user_name

    # Check for personalization (if the user has already shared their name)
    if user_input.lower().startswith("my name is"):
        user_name = user_input.split("is")[1].strip()

    # Add user input to conversation history
    conversation_history.append(f"You: {user_input}")

    # Emotion-based responses (simple example: detects positive or negative words)
    if "sad" in user_input.lower() or "unhappy" in user_input.lower():
        return "I'm really sorry to hear that. Is there anything I can do to make you feel better?"

    # Check if the user is asking for a calculation
    if re.search(r"calculate (.*)", user_input.lower()):
        return calculate_expression(user_input)

    # Check if the user is asking to open an app, file, or folder
    if re.search(r"open (.*)", user_input.lower()):
        return open_application(user_input)

    # Find the chatbot response using the defined patterns
    chat = Chat(pairs, reflections)
    response = chat.respond(user_input)

    # If no response is found, return a default response
    if response is None:
        return random.choice(
            ["I'm not sure about that. Could you ask something else?", "I didn't understand that, could you clarify?"])

    # Include the user's name in the response if it's known
    if user_name and "name" not in user_input.lower():
        response = f"{response} (Nice talking to you, {user_name}!)"

    # Add chatbot response to conversation history
    conversation_history.append(f"Chatbot: {response}")

    return response


# Function to calculate mathematical expressions
def calculate_expression(expression):
    try:
        # Removing the "calculate" part and evaluating the expression
        expression = expression.lower().replace("calculate", "").strip()
        result = eval(expression)  # Use eval to evaluate the mathematical expression
        return f"The result of {expression} is: {result}"
    except Exception as e:
        return "Sorry, I couldn't calculate that. Please check your input."


# Function to open an application, file, or folder
def open_application(user_input):
    # Extract the application, file, or folder name from the user's input
    path = user_input.lower().replace("open", "").strip()

    # Try opening common applications or files
    try:
        # If the path is a file or folder
        if os.path.exists(path):
            os.startfile(path)
            return f"Opening {path} now..."

        # If the path is a system command (e.g., 'notepad', 'calc' for Windows)
        if os.name == 'nt':  # Windows
            subprocess.run(path, shell=True)
            return f"Opening {path}..."

        # If not a valid path or app, respond with a default message
        return f"Sorry, I couldn't find {path}. Please check the name."

    except Exception as e:
        return f"Error: {e}. I couldn't open {path}."


# Create a function to handle the user interaction
def send_message():
    user_input = entry_field.get()
    if user_input.lower() == "bye":
        window.quit()  # Exit the app if the user types 'bye'

    # Add the user's message to the chat history
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_input}\n", 'user')

    response = chatbot_response(user_input)

    # Add a typing effect to the chatbot's response
    chat_history.config(state=tk.NORMAL)
    typing_effect(response)

    chat_history.config(state=tk.DISABLED)  # Disable the text box after the message is added
    entry_field.delete(0, tk.END)  # Clear the input field

    # Scroll to the bottom of the chat history
    chat_history.yview(tk.END)

    # Use text-to-speech for the chatbot's response
    speak(response)


# Add a function to clear the chat history
def clear_chat():
    chat_history.config(state=tk.NORMAL)
    chat_history.delete(1.0, tk.END)
    chat_history.config(state=tk.DISABLED)


# Create the GUI window
window = tk.Tk()
window.title("Enhanced Chatbot")
window.geometry("400x550")
window.config(bg='#2e3b4e')  # Dark background color for the window

# Set custom fonts
chat_font = tkFont.Font(family="Helvetica", size=12)
title_font = tkFont.Font(family="Helvetica", size=18, weight="bold")

# Create a scrolled text widget for displaying the chat history
chat_history = scrolledtext.ScrolledText(window, height=20, width=50, state=tk.DISABLED, font=chat_font, bg='#f5f5f5',
                                         wrap=tk.WORD)
chat_history.pack(padx=10, pady=10)

# Tag configuration to differentiate user and bot messages
chat_history.tag_config('user', foreground='blue', font=chat_font)
chat_history.tag_config('bot', foreground='green', font=chat_font)

# Add a label at the top
title_label = tk.Label(window, text="Chat with Chatbot", font=title_font, fg="white", bg='#2e3b4e')
title_label.pack(pady=10)

# Create an input field for user text with placeholder text
entry_field = tk.Entry(window, width=50, font=chat_font, bg='#ffffff', fg='#333333')
entry_field.pack(pady=5)
entry_field.insert(0, "Type here...")  # Placeholder text
entry_field.bind("<FocusIn>", lambda event: entry_field.delete(0, tk.END))  # Clear placeholder text on focus

# Create a Send button to trigger chatbot response
send_button = tk.Button(window, text="Send", command=send_message, width=12, font=("Arial", 12), bg="#4CAF50",
                        fg="white")
send_button.pack(pady=5)

# Create a Clear button to clear the chat history
clear_button = tk.Button(window, text="Clear", command=clear_chat, width=12, font=("Arial", 12), bg="#FF5733",
                         fg="white")
clear_button.pack(pady=5)

# Set focus on the input field when the app starts
entry_field.focus()

# Start the GUI event loop
window.mainloop()
