from django.urls import path
from . import views # আমাদের কন্ট্রোলার ফাইলটি ইম্পোর্ট করলাম

urlpatterns = [
    # লারাভেলের Route::get('/customer/posts', [PostController::class, 'customerPage']) এর মতো
    path('customer/posts/', views.customer_post_list, name='customer_posts'),

    # --- নতুন পোস্ট তৈরি করার ফর্মের রাস্তা ---
    path('customer/posts/create/', views.post_create, name='create_post'),

    path('ai-chat/', views.ai_pdf_chat, name='ai_pdf_chat'),

]
