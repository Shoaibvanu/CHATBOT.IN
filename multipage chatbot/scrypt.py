import streamlit as st
from dotenv import load_dotenv
import openai
from htmlTemplates import css, bot_template, user_template

# Set your OpenAI API key here
openai.api_key = "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"

def is_legal_response(response):
    # Add your logic to check if the response is relevant to law-related content
    # For example, you can check for specific keywords, phrases, or patterns
    return "legal" in response.lower() or "law" in response.lower()

def includes_sections(response):
    # Add your logic to check if the response includes sections and subsections
    # For example, you can check for specific keywords related to sections and subsections
    return all(keyword in response.lower() for keyword in ["Act", "sub-section", "clause", " sub-clause"])

def get_openai_response(question, model="gpt-3.5-turbo-1106"):
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Legal question: {question}"}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=200
    )

    if is_legal_response(response['choices'][0]['message']['content']) and includes_sections(response['choices'][0]['message']['content']):
        return response['choices'][0]['message']['content'].strip()
    else:
        return "I don't know the answer to the question."

def handle_userinput(user_question):
    response = get_openai_response(user_question)
    st.write(bot_template.replace("{{MSG}}", response), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Legal Chatbot", page_icon="icon.png")
    st.write(css, unsafe_allow_html=True)
    st.header("HOW MAY I ASSIST YOU")
    user_question = st.text_input("WRITE YOUR LEGAL QUERIES")
    if user_question:
        handle_userinput(user_question)

if __name__ == '__main__':
    main()
