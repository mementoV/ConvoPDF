# Pdf-Q&A with RAG

## Project Description: 
The objective is to create a PDF retrieval system utilizing LangChain, a robust language processing tool, to extract data from PDF documents. Harnessing LangChain's advanced natural language understanding, the system empowers users to execute intricate searches, capturing precise data points from PDF files with efficiency and accuracy. 
Additionally, the system meticulously tracks the number of tokens used and calculates the total cost, ensuring transparency and accountability in resource utilization.

Use a ChatModel to retrieve relevant informations from a PDF file

1. Insert your OpenAI API key and upload a PDF file.
    - First method.
        Insert manually.
        <img width="1439"   src="./assets/pdf_chat screenshot1.png">
        
    - Second method to not insert the the OpenAI API key every session.
        1. Create a .env file and write your OpenAi key : 
            <img width="1400"   src="./assets/pdf_chat screenshot2.png">

        1. The folder will look like this.
            
            ```
            .env
            utils.py
            pdf_chat.py
            ```
2. Upload a PDF file and start chatting.
    1.
    <img width="1400"   src="./assets/pdf_chat screenshot3.png">
    2. 
    <img width="1400"   src="./assets/pdf_chat screenshot4.png">

    
## To Do's

- Add prompt template for better/accurate results.
- Highlight relevant informations inside the Pdf.
- Selection of vector database such as Chroma, FAISS, Pgvector.

