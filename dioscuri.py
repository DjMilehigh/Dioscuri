import streamlit as st
from gemini_chat import GeminiChat
from appendages import get_appended_prompt

def main():
    st.title("Dioscuri")

    # Initialize GeminiChat
    gemini_chat = GeminiChat()

    # Chat history
    chat_history_container = st.container()

    # Function to display chat messages
    def display_chat_history(messages):
        for role, message in messages:
            with st.chat_message(role):
                st.markdown(message)

    # Initialize or retrieve chat history from session state
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    messages = st.session_state["chat_history"]

    # State variable for user input
    user_input_state = st.session_state.get("user_input_state", "")

    # User input
    user_input = st.text_input("Enter your message:", key="user_input", value=user_input_state)

    # Sidebar for settings
    with st.sidebar:
        st.title("Settings")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.9, 0.01)
        append_encoded_string = st.checkbox("Enable Jailbreak", value=True)
        if st.button("Clear Chat"):
            st.session_state["chat_history"] = []

    if user_input:
        prompt = user_input

        if append_encoded_string:
            # Append encoded string to the user input
            prompt = user_input + " " + get_appended_prompt()

        max_retries = 5
        retry_count = 0
        response = None

        while retry_count < max_retries:
            # Send the prompt to GeminiChat
            response = gemini_chat.send_message(prompt, temperature=temperature)

            if response is not None:
                break

            retry_count += 1
            print(f"Retrying query ({retry_count}/{max_retries})...")

        if response is None:
            st.error("Failed to generate a response after multiple retries.")

        # Update chat history
        messages.append(("user", user_input))
        messages.append(("assistant", response))
        st.session_state["chat_history"] = messages

        # Clear user input state
        st.session_state["user_input_state"] = ""

    # Display chat history
    display_chat_history(messages)

if __name__ == "__main__":
    main()
