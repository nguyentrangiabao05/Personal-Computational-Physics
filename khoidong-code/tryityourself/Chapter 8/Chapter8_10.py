def send_messages(messages, sent_messages):
    while messages:
        current_message = messages.pop(0)
        print(f"Sending message: {current_message}")
        sent_messages.append(current_message)

text_messages = ["Hello there!", "How are you?", "See you later."]
sent_messages = []

send_messages(text_messages, sent_messages)

print("\nFinal lists:")
print(f"text_messages: {text_messages}")
print(f"sent_messages: {sent_messages}")