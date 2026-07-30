from django.shortcuts import render, redirect
from .models import Post # আমাদের ডাটাবেজ মডেলটি ইম্পোর্ট করলাম

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