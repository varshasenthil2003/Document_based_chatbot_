import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import cohere
import pdfplumber
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Path to store uploaded documents
DOCUMENTS_FOLDER = './documents'
os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)

cohere_client = cohere.Client(os.getenv('COHERE_API_KEY'))

# Utility function to extract text from PDF files
def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF document."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return ''.join(page.extract_text() or '' for page in pdf.pages)
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ''


# Index uploaded documents for semantic search
def index_documents():
    """Indexes all uploaded documents."""
    document_texts = []
    document_metadata = []

    for filename in os.listdir(DOCUMENTS_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(DOCUMENTS_FOLDER, filename)
            text = extract_text_from_pdf(pdf_path)
            if text:
                document_texts.append(text)
                document_metadata.append({"filename": filename, "path": pdf_path})

    return document_texts, document_metadata


def get_embeddings(texts):
    """Generate embeddings for a list of texts using Cohere."""
    embeddings = cohere_client.embed(
        model="embed-english-v2.0",  #Cohere's embedding model
        texts=texts
    ).embeddings
    return np.array(embeddings)

def search_documents(query):
    """Search documents semantically for the best matches."""
    global document_texts, document_metadata
    if not document_texts:
        return []

    # Generate embeddings for the query and documents
    query_embedding = get_embeddings([query])[0]
    document_embeddings = get_embeddings(document_texts)

    similarities = cosine_similarity([query_embedding], document_embeddings)[0]

    # Retrieve the top documents based on similarity
    ranked_indices = np.argsort(similarities)[::-1] 
    top_documents = []
    
    for idx in ranked_indices:
        if similarities[idx] > 0.3: 
            text_snippet = document_texts[idx][:500]  
            top_documents.append({
                "filename": document_metadata[idx]["filename"],
                "snippet": text_snippet,
                "similarity": similarities[idx],
            })

    return top_documents

def generate_response(prompt):
    """Generates a response using the Cohere API."""
    response = cohere_client.generate(
        model="command",
        prompt=prompt,
        max_tokens=300, 
        temperature=0.5,  
    )
    return response.generations[0].text.strip()

def conversational_chat(user_input):
    """Handles conversational chat with document context."""
    print("into convo chat")
    documents = search_documents(user_input)

    document_context = '\n\n'.join(
        [f"Document: {doc['filename']}\nSnippet: {doc['snippet']}" for doc in documents]
    )
    print("CONTEXT : ", document_context)
    
    if not documents:
        document_context = "No relevant documents found."

    # AI prompt
    prompt = f"""
        You are an advanced AI assistant tasked with answering user questions based on a set of PDF documents. 
        Your response should only use the relevant document content provided below and avoid unrelated information.

        Relevant Document Context:
        {document_context}

        User Input:
        {user_input}

        Your Task:
        Provide a clear, concise, and accurate response based on the relevant document context.
        """
    response = generate_response(prompt)
    return response

@app.route('/')
def index():
    """Renders the homepage."""
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handles user queries."""
    user_input = request.json.get('user_input', '').strip()
    if not user_input:
        return jsonify({'error': 'User input is required'}), 400

    print("Processing query:", user_input)
    
    # Generate response based on the current input and document context
    output = conversational_chat(user_input)

    return jsonify({
        'response': output,
        'speech_enabled': True,
        'message_id': str(hash(output))
    })


@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clears the conversation history."""
    session.pop('conversation_history', None)
    return jsonify({'message': 'Conversation history cleared'})


@app.route('/upload', methods=['POST'])
def upload():
    """Handles file uploads."""
    if 'files' not in request.files:
        return jsonify({'error': 'No files part'}), 400

    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No files selected'}), 400

    for file in files:
        if file.filename.endswith('.pdf'):
            file_path = os.path.join(DOCUMENTS_FOLDER, file.filename)
            file.save(file_path)

    # Reindex documents after upload
    global document_texts, document_metadata
    document_texts, document_metadata = index_documents()

    return jsonify({'message': 'Files uploaded and indexed successfully!'})


if __name__ == '__main__':
    # Index documents on startup
    document_texts, document_metadata = index_documents()
    app.run(debug=True)