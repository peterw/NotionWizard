import json
import time
import openai
import streamlit as st
import api_calls
import requests
import os 
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
notion_api_key = os.getenv('NOTION_API_KEY')
page_id = os.getenv('PAGE_ID')

def setup_st_interface():
    """Set up the Streamlit interface and handle API key form submission."""
    st.title("Notion Page Assistant")
    # Initialize message history
    st.session_state.messages = st.session_state.get('messages', [{"role": "assistant", "content": "Welcome! How can I assist you today?"}])

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def process_input():
    """Process user input and display assistant response."""
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        assistant_response = get_assistant_response(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            if assistant_response:
                response_chunk = ""
                for chunk in assistant_response.split():
                    response_chunk += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(response_chunk + "▌")

            message_placeholder.markdown(assistant_response)

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})


def get_assistant_response(input_text):
    functions = [
        {
            "name": "get_response_for_chat",
            "description": "Gets a reply from the GPT-3 model to display in the chat",
            "parameters": {
                "type": "object",
                "properties": {
                    "Reply": {
                        "type": "string",
                        "description": "The reply to display in the chat so as to make it look like a real conversation"
                    }
                },
                "required": ["Reply"]
            }
        },
        {
            "name": "create_notion_page_with_content",
            "description": "Creates a new Notion page with the input text as the content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Title": {
                        "type": "string",
                        "description": "The Title of the page"
                    },
                    "Content": {
                        "type": "string",
                        "description": "The content of the page.You can generate this based on a user's input or take a user's input as content.Format this content accordingly"
                    }
                },
                "required": ["Title", "Content"]
            }
        },
    ]
    model = "gpt-3.5-turbo-0613"
    messages = [{"role": "user", "content": input_text}]


    # Define the API endpoint
    api_endpoint = "https://api.openai.com/v1/chat/completions"

    # Set up the request payload
    payload = {
        "model": model,
        "messages": messages,
        "functions": functions
    }

    # Set up the request headers
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    # Make the POST request
    response = requests.post(api_endpoint, json=payload, headers=headers)

    # Handle the response
    if response.status_code == 200:
        completion = response.json()
    else:
        # Handle error response
        return "Authentication Error, please check your APi keys and try again"

    try:
        function_arguments = json.loads(completion['choices'][0]['message']['function_call']['arguments'])
        print(function_arguments["Title"])

        if 'Reply' in function_arguments:
            return function_arguments['Reply']
        elif 'Content' in function_arguments:
            try:
                page_details = api_calls.create_notion_page_with_content(
                    function_arguments['Title'],
                    function_arguments['Content'],
                    page_id
                )
            except Exception as e:
                print(e)
                return "Error creating page. Please check your Notion integration/API keys and try again."
            return f"Page Title: {page_details['page_title']}\nURL: {page_details['page_url']}"
    except KeyError:
        return completion['choices'][0]['message']['content']


if __name__ == "__main__":
    setup_st_interface()
    process_input()
