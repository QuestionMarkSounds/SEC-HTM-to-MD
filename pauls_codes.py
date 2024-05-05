# Import any secret keys here

from dotenv import load_dotenv
import os

load_dotenv()

# Now load the libraries needed for the app
import os
import streamlit as st
import pandas as pd
# from custom_ui_functions import hide_main_menu_streamlit, set_side_bar_width, hide_image_fullscreen, hide_anchor_link, rhdhv_markdown, rhdhv_bullet_points, mandatory_info_caption
from PIL import Image
from PyPDF2 import PdfReader

# Secondary Imports

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS

from prompts import system_prompt

from langchain_groq import ChatGroq

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from langchain_community.document_loaders import PyPDFLoader
st.set_page_config(page_title='Knowledge Assistant', layout='centered')


# hide_main_menu_streamlit()

# set_side_bar_width(550)

rhdhv_blue = "#00567D"
rhdhv_light_blue = "#C7E0F4"

groq_api_key = "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"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

rhdhv_blue = "#00567D"
rhdhv_light_blue = "#C7E0F4"
# load logo image
# image_rhdhv = Image.open('rhdhv.png')

# Set the sidebar header and image here
with st.sidebar:
    # st.sidebar.image(image_rhdhv, width=200)
    # PDF upload and processing
    pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
    st.sidebar.markdown("This app is an LLM-powered RAG ChatBot.")
    st.sidebar.markdown("Built Using Streamlit, Langchain and llama3 via groq")
    st.sidebar.markdown("Vector Embeddings are stored in the st.session_state and similarity search algorithm used is FAISS")
    st.sidebar.markdown("Developed by: Taanis Karigar")
    st.sidebar.markdown("version 180224")
    st.sidebar.markdown("***AI may not always produce accurate results. Please confirm with an expert if you are un-sure about a response!")   

# Add content in the main section here
# rhdhv_markdown("🧠 Knowledge Assistant 💭", rhdhv_blue, "400", tag='h1')

# Initialize session state variables
if "messages" not in st.session_state:
    print("AAA")
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Display chat history
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if pdf is not None:

    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_text(text=text)

    if st.session_state.vector_store is None:
        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        st.session_state.vector_store = FAISS.from_texts(chunks, embedding=embeddings)
        st.success("Embeddings Computation Complete")

GROQ_API_KEY = "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"

from groq import Groq
from prompts import system_prompt

def groq_query(system_prompt, context, user_query):

    client = Groq(api_key=GROQ_API_KEY)
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": system_prompt + context
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response

# groq_query(system_prompt=system_prompt, user_query="Who is the president of madagascar?")

if query:=st.chat_input("Ask me anything about this PDF"):
    st.session_state.messages.append({"role": "user", "content": query})

    # Display user input in the chat format
    with st.chat_message("user"):
        st.markdown(query)

    # Assistant's response using OpenAI GPT-3.5 Turbo
    with st.chat_message("assistant"):
        docs = st.session_state.vector_store.similarity_search(query=query, k=2)

        context = ""

        for doc in docs:
            page_content = doc.page_content
            context += page_content
        

        # # llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0, openai_api_key=OPENAI_API_KEY)
        # llm=ChatGroq(groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
        # chain = load_qa_chain(llm=llm, chain_type="stuff")
        # response = chain.run(input_documents=docs, question=system_prompt+query)

        response = groq_query(system_prompt=system_prompt, context= context, user_query=query)

        print(response)
        if "I don't know" not in response:
            with st.expander("📚 My Source"):
                st.markdown(f"***{context}***")        

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
