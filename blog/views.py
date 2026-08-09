from django.shortcuts import render, redirect
from .models import Post # আমাদের ডাটাবেজ মডেলটি ইম্পোর্ট করলাম
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import DocumentAI

# এটি লারাভেলের public function customerPage() এর মতো একটি কন্ট্রোলার মেথড
def customer_post_list(request):
    # ডাটাবেজ থেকে সব ব্লগ পোস্ট নিয়ে আসলাম (Laravel: $posts = Post::all())
    posts = Post.objects.all()
    
    # ডাটাগুলোকে একটি অ্যাসোসিয়েটিভ অ্যারে বা ডিকশনারিতে সাজালাম
    context = {'posts': posts}
    
    # লারাভেলের return view('posts', compact('posts')) এর মতো এখানে render করা হয়
    return render(request, 'blog/customer_page.html', context)
# --- এটি হলো আমাদের নতুন পোস্ট তৈরি করার কন্ট্রোলার (Create & Store) ---
def post_create(name_or_request):
    request = name_or_request
    
    # ১. ইউজার যখন ফর্মে 'Submit' বাটনে চাপবে (Laravel: $request->isMethod('post'))
    if request.method == "POST":
        # লারাভেলের $request->input('title') এর মতো ডাটা ধরা
        title_data = request.POST.get('title')
        content_data = request.POST.get('content')
        
        # ডাটাবেজ মডেলের অবজেক্ট তৈরি করে সেভ করা
        new_post = Post(title=title_data, content=content_data)
        
        # ম্যাজিক: .save() দেওয়ার সাথে সাথে আমাদের সিগন্যাল (Observer) ফায়ার হবে এবং FastAPI-কে কল করবে!
        new_post.save() 
        
        # সফলভাবে সেভ হওয়ার পর কাস্টমার পেজে রিডাইরেক্ট করা (Laravel: redirect()->route(...))
        return redirect('customer_posts')
        
    # ২. ইউজার যখন সাধারণ লিংকে ঢুকবে, তখন শুধু খালি ফর্ম পেজটি দেখাও (GET Request)
    return render(request, 'blog/create_post.html')

def ai_pdf_chat(request):
    # ডাটাবেজে থাকা শেষ আপলোড হওয়া পিডিএফ-টি নেওয়া
    latest_doc = DocumentAI.objects.order_by('-uploaded_at').first()
    
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_question = request.POST.get('question')
        
        # ফাস্টএপিআই আরএগে (RAG) রিকোয়েস্ট পাঠানো
        try:
            api_url = "http://fastapi_ai:8003/ask-pdf"
            response = requests.post(api_url, json={"question": user_question}, timeout=45)
            if response.status_code == 200:
                return JsonResponse({"answer": response.json().get("answer")})
            return JsonResponse({"answer": "Error: AI engine failed to respond."}, status=500)
        except Exception as e:
            return JsonResponse({"answer": f"Connection Error: {str(e)}"}, status=500)

    return render(request, 'blog/pdf_chat.html', {'doc': latest_doc})