
def import_memory(filename):
    pass

# Export the chat history into a text file
def export_chat_history(memory, filename):
    formatted_history = ""
    for message in memory['history']:
        if isinstance(message, HumanMessage):
            formatted_history += f"Human: {message.content}\n"
        elif isinstance(message, AIMessage):
            formatted_history += f"Assistant: {message.content}\n\n"

    # Create a new file to store the conversation history
    file_path = os.path.join(os.getcwd(), filename)
    with open(file_path, 'w') as f:
        f.write(formatted_history)
    print("Conversation history exported successfully to human_assistant_messages.txt!")
