# NotionWizard

This is a simple Notion Page Assistant that uses OpenAI's functions to create a Notion page. 

It  provides a chat-based interface where you can interact with the assistant. Simply enter your message in the chat input and press Enter. The assistant will respond with appropriate actions.

## Prerequisites

- You need to have Python installed on your machine. You can download it from [here](https://www.python.org/downloads/).
- You also need to install the `openai` and `requests` Python libraries. You can install them using pip:

```bash
pip install -r requirements.txt
```

- You need to have an OpenAI API key. You can get it from [here](https://beta.openai.com/signup/).
- You also need a Notion API token and a Page ID. You can get them by following the instructions [here](https://developers.notion.com/docs).
- Please also check [here](https://developers.notion.com/docs/create-a-notion-integration) for more information on how to create a Notion integration.
- To get the page ID, click on Share  at the top right of your Notion page and copy the link. The page ID is the last part of the link. For example, if the link is `https://www.notion.so/Getting-Started-c51d744605e94cf9b2a74a9692338072`, the page ID is `c51d744605e94cf9b2a74a9692338072`.


## Usage

1. Clone this repository:

2. Navigate to the project directory:

```bash
cd openai-notion-page-creator
```

4. Run the script:

```bash
streamlit run main.py
```
Enter your OpenAI API key, Notion API token, and Page ID in the appropriate fields and click on the `Submit` button.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

