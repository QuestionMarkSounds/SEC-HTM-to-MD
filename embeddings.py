from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from prompts import system_prompt
from htm_to_markdown import sec_to_md_file, sec_to_md_from_html
from langchain_text_splitters import RecursiveCharacterTextSplitter
from io import StringIO
from sec_searcher import sec_search

load_dotenv()
embeddings_model = OpenAIEmbeddings()

import streamlit as st

st.set_page_config(page_title='SEC Assistant', layout='centered')

with st.sidebar:
    # st.sidebar.image(image_rhdhv, width=200)
    # PDF upload and processing
    filing = st.file_uploader("Upload a SEC filing", type=["html"])
    ticker_lookup = st.text_input("Search using ticker (example: AAPL)")
    st.sidebar.markdown("***AI may not always produce accurate results. Please confirm with an expert if you are un-sure about a response!")   

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "messages" not in st.session_state:
    # print("AAA")
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

if ticker_lookup is not None:
    filing = sec_search(ticker_lookup)

    md_text = sec_to_md_from_html(filing.html())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7000, chunk_overlap=500, length_function=len)
    chunks = text_splitter.split_text(text=md_text)
    # print(md_text)

    if st.session_state.vector_store is None:
        embeddings = OpenAIEmbeddings()
        st.session_state.vector_store = FAISS.from_texts(chunks, embedding=embeddings)
        st.success("Embeddings Computation Complete")

if filing is not None:
    # stringio = StringIO(filing.getvalue().decode("utf-8"))
    # string_data = filing.read()

    md_text = sec_to_md_file(filing)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7000, chunk_overlap=500, length_function=len)
    chunks = text_splitter.split_text(text=md_text)
    # print(md_text)

    if st.session_state.vector_store is None:
        embeddings = OpenAIEmbeddings()
        st.session_state.vector_store = FAISS.from_texts(chunks, embedding=embeddings)
        st.success("Embeddings Computation Complete")

from groq import Groq
from prompts import system_prompt

def groq_query(system_prompt, context, user_query):

    client = Groq()
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
        temperature=0.2,
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
# if False:
if query:=st.chat_input("Ask me anything about this PDF"):
    st.session_state.messages.append({"role": "user", "content": query})

    # Display user input in the chat format
    with st.chat_message("user"):
        st.markdown(query)

    # Assistant's response using OpenAI GPT-3.5 Turbo
    with st.chat_message("assistant"):
        docs = st.session_state.vector_store.similarity_search(query=query, k=4)

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
