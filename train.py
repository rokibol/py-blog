import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig 
from peft import LoraConfig, get_peft_model, TaskType 

print("🧠 [1/4] Loading dataset.jsonl into memory...")
dataset = load_dataset("json", data_files="dataset.jsonl", split="train")

print("🐳 [2/4] Fetching CPU-optimized Base Model weights...")
# 💡 কিলার ট্রিকস: ৪-বিট জ্যাম বাইপাস করতে আমরা মেটা-র অফিশিয়াল পিওর লাইটওয়েট সংস্করণ ব্যবহার করছি
model_id = "Qwen/Qwen2.5-0.5B-Instruct" # ২০২৬ সালের সবচেয়ে কিলার এবং সুপার-ফাস্ট লোকাল সিপিইউ ট্রেইনিং মডেল
tokenizer = AutoTokenizer.from_pretrained(model_id)

# সিপিইউ এর জন্য একদম ক্লিন সিঙ্গেল ডিভাইস ম্যাপ লক করা
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    device_map="cpu", # 🚀 সরাসরি পিওর প্রসেসর গেটওয়ে
    low_cpu_mem_usage=True
)

# ৪-বিট লক না থাকায় এই LoRA লেয়ারটি আপনার প্রসেসরের ভেতর আলোর গতিতে কাজ করবে
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,              
    lora_alpha=16,    
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"] 
)

model = get_peft_model(model, peft_config)
print("✅ [PEFT SUCCESS]: Trainable adapters attached successfully for CPU Training.")

print("🚀 [3/4] Initializing Supervised Fine-Tuning (SFT) Parameters...")
training_args = SFTConfig(
    output_dir="./results",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1, # 💡 কুইক আপডেটের জন্য স্টেপ ১ করা হলো, যাতে সাথে সাথে পার্সেন্টেজ বাড়ে
    learning_rate=2e-4,
    logging_steps=1,
    max_steps=10, # কুইক প্র্যাকটিসের জন্য ১০টি গাণিতিক স্টেপ লকড
    use_cpu=True, 
    report_to="none",
    max_length=512, 
)

def formatting_prompts_func(example):
    return example['text']

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    formatting_func=formatting_prompts_func,
    processing_class=tokenizer,
    args=training_args, 
)

print("🔥 [4/4] STARTING MODEL RETRAINING LOOP... (Optimizing Weights)")
trainer.train()

print("💾 Saving fine-tuned adapters safely to disk...")
model.save_pretrained("./my_fine_tuned_llama3")
print("🎉 [SUCCESS]: Your custom model weights are successfully trained on CPU!")
