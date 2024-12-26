# 📄 Document-Based Chatbot with Cohere 🤖

This project is a **chatbot** designed to answer user queries based on uploaded PDF documents. Powered by **Cohere's NLP capabilities**, it enables semantic search and interactive AI-powered conversations. 🚀

---

## ✨ Features

✅ **Document Upload and Indexing**: Upload PDF documents to create a searchable index.  
🔍 **Semantic Search**: Retrieve relevant snippets from documents using Cohere embeddings.  
💬 **AI-Powered Conversations**: Context-aware responses to your queries.  
🌐 **Interactive Web Interface**: User-friendly interface for uploads and chatting.  

---

## 🏗️ Project Structure

```
├── app.py               # Main Flask application
├── test.py              # Script to test Cohere API models 
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API key) 
├── templates/           
│   └── index.html       # Frontend template 
├── documents/           # Folder for uploaded PDF documents
└── README.md            # Project documentation
```

---

## 🛠️ Prerequisites

🔧 **Python**: Version 3.7 or later.  
🔑 **Cohere API Key**: Get one from [Cohere](https://cohere.ai).  
📦 **Dependencies**: Listed in `requirements.txt`.

---

## 🚀 Installation

1. **Install Dependencies**:  
   Run the following command to install all required libraries:  
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**:  
   Create a `.env` file in the project root with your API key:  
   ```plaintext
   COHERE_API_KEY='Replace with your actual API key'
   ```

---

## 🖥️ Usage

1. **Start the Application**:  
   Run the Flask application:  
   ```bash
   python app.py
   ```

2. **Access the Application**:  
   Open your browser and go to:  
   ```
   http://127.0.0.1:5000
   ```

3. **Upload Documents**:  
   Use the "Upload Your PDF Files" section to upload files.  

4. **Chat with the Bot**:  
   Type your queries in the input field and interact with the chatbot.

---

## 🌐 Frontend Template

The web interface is located in `templates/index.html` and includes:  

- 📤 **File Upload Section**: Drag and drop or select PDF files to upload.  
- 💬 **Chatbox**: A responsive interface for seamless conversations.  
- 📱 **Responsive Design**: Optimized for both desktop and mobile devices using Bootstrap.

---

## 📦 Dependencies

Install the following Python libraries:  
- Flask 🐍  
- pdfplumber 📄  
- Cohere 🤖  
- transformers 🛠️  
- torch 🔥  
- python-dotenv 🌐  

Install them with:  
```bash
pip install -r requirements.txt
```

---

## 🔮 Future Enhancements

✨ **Expand File Support**: Add support for DOCX and TXT files.  
🔒 **User Authentication**: Secure access with login functionality.  
⚡ **Optimization**: Improve embeddings and search for larger datasets.  

---
