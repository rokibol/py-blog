from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
import json
import re
import traceback  # 🧠 পাইথনের আসল এরর লাইন ট্র্যাক করার অফিশিয়াল মডিউল
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from pydantic import BaseModel

# পিডিএফ আপলোড ও ডাটাবেজ সেভ করার ফোল্ডার পাথ ডিফাইন করা
UPLOAD_DIR = "/app/uploaded_pdfs"
CHROMA_DB_DIR = "/app/chroma_db"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Local LLM-Powered Advanced Text Analyzer Service with Live Debugging")

class BlogText(BaseModel):
    content: str

def analyze_content_locally(text: str):
    print("\n🔍 [DEBUG START]: Initiating Local LLM Analysis...")
    
    # ১. ওলামা ক্লায়েন্ট তৈরি করার ধাপ ডিবাগ
    try:
        client = ollama.Client(host='http://192.168.0.101:11434')
        print("✅ [DEBUG]: Ollama Client successfully created on host gateway.")
    except Exception as e:
        print("❌ [CRITICAL]: Failed to initialize Ollama Client!")
        traceback.print_exc()  # সার্ভার লগে হুবহু লাইনের এরর প্রিন্ট করবে
        raise e
    
    system_prompt = (
        "You are an expert AI content moderator. Analyze the input text. "
        "You must output ONLY a valid JSON object. No conversational text. "
        "The JSON schema must be exactly: {\"is_spam\": boolean, \"ai_summary\": \"string\"}"
    )
    
    # ২. ওলামা চ্যাট বা মডেল লোডিং এর ধাপ ডিবাগ
    try:
        print("🧠 [DEBUG]: Sending content payload to Llama3 model... (Waiting for response)")
        response = client.chat(model='llama3', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': text},
        ])
        print("✅ [DEBUG]: Successfully received raw response from Llama3.")
    except Exception as e:
        print("❌ [CRITICAL]: Error occurred during Ollama client.chat execution!")
        print("💡 TIP: Is your local Ollama running? Is Llama3 model downloaded?")
        traceback.print_exc()  # ওলামা কানেক্ট না হলে এখানে এরর প্রিন্ট হবে
        raise e

    # ৩. জেসন পার্সিং এবং এক্সট্রাকশন এর ধাপ ডিবাগ
    try:
        ai_response_text = response['message']['content'].strip()
        print(f"🤖 [DEBUG] Raw AI Content: {ai_response_text}")
        
        json_match = re.search(r'\{.*\}', ai_response_text, re.DOTALL)
        if json_match:
            ai_response_text = json_match.group(0)
            
        parsed_json = json.loads(ai_response_text)
        print("✅ [DEBUG]: JSON parsing successful. Returning metadata back to Django.")
        return parsed_json
    except Exception as e:
        print("❌ [CRITICAL]: Failed to parse AI output into valid JSON object!")
        traceback.print_exc()
        raise e

@app.post("/analyze-post")
async def analyze_post(data: BlogText):
    if not data.content.strip():
        raise HTTPException(status_code=400, detail="Content field cannot be empty.")
        
    try:
        result = analyze_content_locally(data.content)
        return {
            "is_spam": result.get("is_spam", False),
            "ai_summary": result.get("ai_summary", "[Summary parsed]")
        }
    except Exception as e:
        # ৫০০ এরর স্ক্রিনে দেওয়ার ঠিক আগে আসল এরর মেসেজটি ফাস্টএপিআই লগে পুশ করা
        print(f"🚨 [API ENDPOINT EXCEPTION HANDLER]: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal LLM Error: {str(e)}")

# জ্যাঙ্গো থেকে পিডিএফ প্রসেস করার রিকোয়েস্ট স্কিমা
class PDFProcessRequest(BaseModel):
    file_name: str

# ১. পিডিএফ ফাইল রিড করে ভেক্টর ডাটাবেজে রূপান্তর করার কোর ফাংশন
def embed_and_store_pdf(file_name: str):
    pdf_path = os.path.join(UPLOAD_DIR, file_name)
    if not os.path.exists(pdf_path):
        return {"status": "error", "message": "PDF file not found on server."}

    try:
        # ক) পিডিএফ লোড করা
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        # খ) বড় টেক্সটকে এআই প্রসেসিংয়ের সুবিধার জন্য ছোট ১০০০ ক্যারেক্টারের টুকরো করা
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        # গ) ওপেন-সোর্স HuggingFace মডেল দিয়ে টেক্সটকে গাণিতিক ভেক্টরে (Embeddings) রূপান্তর করা
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # ঘ) লোকাল ChromaDB ভেক্টর ডাটাবেজে ডাটা চিরতরে সেভ করে ফেলা
        vector_db = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings, 
            persist_directory=CHROMA_DB_DIR
        )
        return {"status": "success", "message": f"Successfully processed {len(chunks)} text chunks."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ২. ফাস্টএপিআই-তে নতুন এন্ডপয়েন্ট তৈরি করা যা জ্যাঙ্গো কল করবে
@app.post("/process-pdf")
async def process_pdf(data: PDFProcessRequest):
    result = embed_and_store_pdf(data.file_name)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result


# api.py এর একদম নিচে এই চ্যাট এন্ডপয়েন্টটি যুক্ত করুন:

class ChatRequest(BaseModel):
    question: str

@app.post("/ask-pdf")
async def ask_pdf(data: ChatRequest):
    if not data.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
        
    try:
        # ক) লোকাল ChromaDB এবং HuggingFace এম্বেডিং লোড করা
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)
        
        # খ) ইউজার যে প্রশ্নটি করেছে, তার সাথে মিল থাকা সবচেয়ে কাছাকাছি ৩টি টেক্সট টুকরো (Chunks) খুঁজে বের করা
        search_results = vector_db.similarity_search(data.question, k=3)
        
        # খুঁজে পাওয়া টুকরোগুলোকে একটি টেক্সট ব্লকে সাজানো
        context_text = "\n\n".join([doc.page_content for doc in search_results])
        print(f"🎯 [RAG DEBUG]: Retrieved Context from PDF:\n{context_text[:200]}...")
        
        # গ) ওলামা Llama 3 কে কড়া প্রম্পট দেওয়া যেন সে শুধুমাত্র এই পিডিএফ-এর ডাটা দেখেই উত্তর দেয়
        client = ollama.Client(host='http://192.168.0.101:11434')
        system_prompt = (
            "You are a strict AI assistant that answers questions based ONLY on the provided context extracted from a PDF. "
            "If the answer cannot be found in the context, politely say 'I cannot find the answer in the provided document.' "
            "Do not make up facts or use external knowledge. Keep your answer precise and professional."
        )
        
        user_prompt = f"Context from PDF:\n{context_text}\n\nQuestion: {data.question}"
        
        response = client.chat(model='llama3', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ])
        
        return {"answer": response['message']['content'].strip()}
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
