import json
import re
import time
from datetime import datetime

pending_question = None


# -------------------------
# KNOWLEDGE BASE FUNCTIONS
# -------------------------

def load_knowledge():
    try:
        with open("knowledge.json", "r") as file:
            return json.load(file)
    except:
        return {}


def save_knowledge(data):
    with open("knowledge.json", "w") as file:
        json.dump(data, file, indent=4)


# -------------------------
# CHAT HISTORY FUNCTION
# -------------------------

def save_chat(user_message, bot_response):
    with open("chat_history.txt", "a") as file:
        file.write(f"User: {user_message}\n")
        file.write(f"Bot: {bot_response}\n")
        file.write("-" * 40 + "\n")


# -------------------------
# CHATBOT RESPONSE FUNCTION
# -------------------------

def calculate_expression(expression):
    try:
        expression = expression.replace(" ", "")

        if re.match(r'^[0-9+\-*/().]+$', expression):
            result = eval(expression)
            return f"Result = {result}"

    except:
        pass

    return None

def get_response(user_input, knowledge, start_time):
    global pending_question
    user_input = user_input.lower().strip()
    
    # Learning Mode

    if pending_question is not None:

        knowledge[pending_question] = user_input

        save_knowledge(knowledge)

        stats["learned_answers"] += 1

        learned_question = pending_question

        pending_question = None

        return f"Thank you! I learned the answer for '{learned_question}'."

    if user_input == "/stats":
        return show_stats(start_time)

    calculation = calculate_expression(user_input)

    if calculation:
        return calculation

    # Greetings
    if user_input in ["hello", "hi", "hey"]:
        return "Hello! How can I help you today?"

    elif user_input == "how are you":
        return "I'm doing great. Thanks for asking!"

    elif user_input == "bye":
        return "Goodbye! Have a great day."

    # Date
    elif user_input == "date":
        return datetime.now().strftime("Today's date is %d-%m-%Y")

    # Time
    elif user_input == "time":
        return datetime.now().strftime("Current time is %I:%M %p")

    # Check learned knowledge
    elif user_input in knowledge:
        return knowledge[user_input]

    # Unknown question
    else:
        pending_question = user_input

    return "I don't know the answer. Please teach me."


# -------------------------
# MAIN PROGRAM
# -------------------------

stats = {
    "messages": 0,
    "learned_answers": 0
}

def show_stats(start_time):

    session_time = int(time.time() - start_time)

    minutes = session_time // 60
    seconds = session_time % 60

    return (
        f"\nMessages Sent: {stats['messages']}"
        f"\nLearned Answers: {stats['learned_answers']}"
        f"\nSession Duration: {minutes} min {seconds} sec"
    )

def main():

    print("=" * 50)
    print("      SMART AI CHATBOT ASSISTANT")
    print("=" * 50)
    print("Type 'bye' to exit.\n")

    knowledge = load_knowledge()
    start_time = time.time()

    while True:

        user_input = input("You: ")
        stats["messages"] += 1

        response = get_response(user_input, knowledge, start_time)

        print("Bot:", response)

        save_chat(user_input, response)

        if user_input.lower() == "bye":
            break


if __name__ == "__main__":
    print("Run gui.py to start the chatbot.")

def process_message(user_input, knowledge, start_time):
    return get_response(user_input, knowledge, start_time)