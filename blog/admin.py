from django.contrib import admin
from .models import Post

# blog/admin.py এর একদম নিচে এটি যোগ করুন:
from .models import DocumentAI  # 👈 আপনার নতুন মডেলটি ইমপোর্ট করা হলো

admin.site.register(DocumentAI) # 👈 অ্যাডমিন প্যানেলে এটি রেজিস্টার করা হলো

# আমাদের পোস্ট মডেলটিকে অ্যাডমিন প্যানেলে যুক্ত করে দিলাম
admin.site.register(Post)
