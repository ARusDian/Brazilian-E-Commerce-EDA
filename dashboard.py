import streamlit as st

def main():
    st.title("Chatbot Streamlit App")

    user_input = st.text_input("Enter your message:")

    if st.button("Send"):
        chatbot_response = get_chatbot_response(user_input)
        st.text_area("Chatbot Response:", chatbot_response, height=100)

def get_chatbot_response(user_input):
    return "Chatbot: Hello! I’m a simple chatbot. You said: " + user_input

if __name__ == "main":
    main()
