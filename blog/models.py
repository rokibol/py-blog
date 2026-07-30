from django.db import models

class Post(models.Model):
    # ১. পোস্টের টাইটেল (লারাভেলের $table->string('title') এর মতো)
    title = models.CharField(max_length=200)
    
    # ২. ব্লগ পোস্টের মূল বডি বা কন্টেন্ট ($table->text('content') এর মতো)
    content = models.TextField()
    
    # ৩. এআই থেকে জেনারেট হওয়া সারাংশ বা সামারি সেভ রাখার কলাম
    ai_summary = models.TextField(blank=True, null=True)
    
    # ৪. পোস্টটি স্প্যাম বা খারাপ ভাষার কিনা তার ফ্ল্যাগ
    is_spam = models.BooleanField(default=False)
    
    # ৫. পোস্ট তৈরির সময় (自动 $table->timestamps() এর মতো)
    created_at = models.DateTimeField(auto_now_add=True)

    # ডান্ডার মেথড: আমরা ফেজ-২ ওওপি-তে শিখেছিলাম! 
    # এটি দিলে জ্যাঙ্গো অ্যাডমিন প্যানেলে অবজেক্টের বদলে পোস্টের টাইটেল সরাসরি দেখাবে
    def __str__(self):
        return self.title
