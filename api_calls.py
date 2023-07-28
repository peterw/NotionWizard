import json
import os
import requests
import streamlit as st
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

notion_token = os.getenv('NOTION_API_KEY')

url = "https://api.notion.com/v1/pages"
headers = {
    "Authorization": f"Bearer {notion_token}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_notion_page_with_content(page_title, content, page_id):

    url = "https://api.notion.com/v1/pages/"

    payload = json.dumps({
    "parent": {
    "page_id": page_id
    },
    "properties": {
        "title": {
            "title": [{"type": "text", "text": {"content": page_title}}]
        }
    },
    "children": [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {
                    "content": content }}]
            }
        }
    ]

    })
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        response = response.json()
        st.balloons()
        st.success("Page created successfully")
        page_title = response['properties']['title']['title'][0]['text']['content']
        page_url = response['url']
        st.session_state['page_title'] = page_title
        st.session_state['page_url'] = page_url

        return {'status': 'success', 'page_title': page_title, 'page_url': page_url}
    else:
        st.error(f"Failed to create page.{response.json()['message']}")
        return {'status': 'error', 'error': response}

