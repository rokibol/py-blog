from django.db.models.signals import pre_save
from django.dispatch import receiver
import requests
from .models import Post

# @receiver(pre_save) মানে হলো লারাভেলের saving ইভেন্টের মতো কাজ করবে
@receiver(pre_save, sender=Post)
def analyze_blog_content(sender, instance, **kwargs):
    # instance হলো আপনার সেই পোস্টের অবজেক্ট যা সেভ হতে যাচ্ছে
    # লারাভেলে যেমন আমরা $post->content লিখতাম, এখানে লিখছি instance.content
    
    # যদি আমরা নতুন পোস্ট তৈরি করি বা কন্টেন্ট এডিট করি
    if instance.content:
        # আমাদের ৮০০১ পোর্টের এআই সার্ভারের ঠিকানা
        ai_url = "http://127.0.0.1:8001/analyze-post"

        payload = {"content": instance.content}
        
        try:
            response = requests.post(ai_url, json=payload, timeout=5)
            
            if response.status_code == 200:
                ai_data = response.json()
                instance.ai_summary = ai_data["ai_summary"]
                instance.is_spam = ai_data["is_spam"]
                print("⚡ [AI Success]: Data successfully received from FastAPI!")
            else:
                # যদি সার্ভার রেসপন্স ২০০ না হয়ে অন্য কিছু হয় (যেমন ৪0৪ বা ৫00)
                print(f"❌ [AI Error]: Server responded with status code {response.status_code}")
                instance.ai_summary = f"[AI Server Error Code: {response.status_code}]"
                
        except requests.exceptions.RequestException as error:
            # যদি কানেকশনই হতে না পারে (যেমন পোর্ট ব্লক বা নেটওয়ার্ক ইস্যু)
            print(f"🚨 [AI Connection Failed]: Could not connect to FastAPI. Error: {error}")
            instance.ai_summary = "[AI Service is currently offline]"

