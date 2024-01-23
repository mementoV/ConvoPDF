import streamlit as st
import base64
import os
from streamlit_chat import message
from streamlit_javascript import st_javascript
from langchain.callbacks import get_openai_callback # Check number of token use per request
import openai
from utils import process,load_chain,similarity
from dotenv import load_dotenv
import requests

def check_openai_api_key(api_key):
    if api_key =='':
        return False
    client = openai.OpenAI(api_key=api_key)
    try:
        client.models.list()
    except openai.AuthenticationError:
        return False
    else:
        return True


def clear_submit():
    st.session_state["submit"] = False

def displayPDFpage(upl_file, page_nr):
    # Read file as bytes:
    bytes_data = upl_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8")

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="770" type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)

#clear chat history
def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]


if __name__ == '__main__':
    with st.sidebar:
        st.title("Pdf Q&A with RAG")

    #Check if there is a given key in the .env file and if it's a valid one
    
    load_dotenv()
    get_key = os.getenv('OPENAI_API_KEY')
    
    if get_key : 

        OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
        if not check_openai_api_key(OPENAI_API_KEY):
            with st.sidebar:
                st.write("Please insert a valid key")
    else:
        with st.sidebar:
            OPENAI_API_KEY = st.text_input("OPENAI API KEY",type="password")


    with st.sidebar:
        
        #Check if given key is valid
        try:
            if not check_openai_api_key(OPENAI_API_KEY):
                OPENAI_API_KEY = st.text_input("OPENAI API KEY",type="password")
                
            else : 
                st.write("Valid key")
        except:
            with st.sidebar:
                st.write("Please insert a valid key")

        uploaded_file = st.file_uploader("Upload file",type=["pdf"],help="Only PDF file are supported")

    #Create 2 collumns for chat, pdf visualisation
    side1,side2 = st.columns(spec=[0.7, 0.3], gap="large")
    
    if uploaded_file and check_openai_api_key(OPENAI_API_KEY):
        #Track chat history,tokens,cost
        if "generated" not in st.session_state:
            st.session_state['generated'] = []

        if "past" not in st.session_state:
            st.session_state["past"] = []
        
        if "tokens" not in st.session_state:
            st.session_state['tokens'] = []

        if "cost" not in st.session_state:
            st.session_state['cost'] = []
        db = process(uploaded_file)

        #Display the pdf
        with side2:
            ui_witdh = st_javascript("window.innerWidth")
            displayPDFpage(uploaded_file,ui_witdh)

        #Chatbox
        with side1:
            st.button("Clear history", on_click=on_btn_click)
            with st.container():
                
                query = st.text_input("Say something",placeholder="Can you give me a short summary?",
                                    disabled= not uploaded_file,on_change=clear_submit) 
                
                chat_history = [(st.session_state["past"][i], st.session_state["generated"][i])
                                for i in range(len(st.session_state['generated']))]

                #Load the OpenAI model
                qa_chain = load_chain(OPENAI_API_KEY=OPENAI_API_KEY)

                #Track the number of tokens used and the cost
                with get_openai_callback() as cb:
                    docs = similarity(db,query)
                    answer = qa_chain.run(input_documents = docs,question = query)

                st.session_state.past.append(query)
                st.session_state.generated.append(answer)

                st.session_state.tokens.append(cb.total_tokens)
                st.session_state.cost.append(cb.total_cost)
                
                #Display the messages
                if st.session_state['generated']:
                    
                    for i in range(len(st.session_state['generated'])-1,-1,-1):
                        if st.session_state['generated'][i]!='' and st.session_state['past'][i]!='':
                            message(
                            st.session_state["past"][i],
                            is_user=True,
                            
                            seed="A",
                            key=str(i) + "_user",
                            )
                            st.write("Tokens used : ",cb.total_tokens)
                            st.write("Prompt tokens : ",cb.prompt_tokens," | ","Completions tokens : ",cb.completion_tokens)
                            message(
                                st.session_state["generated"][i],
                                
                                seed="B",
                                key=str(i),
                            )
                        

        with st.sidebar:
            st.subheader("Tokens and cost tracking",divider="rainbow")
            st.write("Total tokens used : ",sum(st.session_state.tokens))
            st.write(f'Cost : {sum(st.session_state.cost)} $')



