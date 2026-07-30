from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Text Analyzer Service")

class BlogText(BaseModel):
    content: str

@app.post("/analyze-post")
async def analyze_post(data: BlogText):
    text = data.content.lower().strip()
    
    # ১. এআই স্প্যাম ডিটেকশন লজিক (সিম্পল প্যাটার্ন কন্ডিশন)
    bad_words = ["spam", "free money", "click here", "abusive"]
    is_spam = any(word in text for word in bad_words)
    
    # ২. এআই টেক্সট সামারাইজেশন লজিক 
    # বাস্তব জীবনে এখানে বড় AI মডেল থাকে, আমরা টেস্ট করার জন্য প্রথম ১০০ অক্ষর নিয়ে সামারি বানাচ্ছি
    summary = text[:100] + "..." if len(text) > 100 else text
    
    return {
        "is_spam": is_spam,
        "ai_summary": f"[AI Generated Summary]: {summary.capitalize()}"
    }
