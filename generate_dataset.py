import json

dataset = []
# Llama 3 এর অফিশিয়াল ট্রেইনিং প্রম্পট ফরম্যাট (Prompt Template)
system_prompt = "You are a custom security expert trained by Rokibul. Detect spam instantly and reply in pure JSON."

for i in range(1, 501):
    # ৫০০টি স্প্যাম এক্সাম্পল
    spam_entry = {
        "text": f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\nURGENT: Click link #{i} to claim your massive reward token now! [/INST] {{\"is_spam\": true, \"ai_summary\": \"Detected custom security spam pattern #{i}.\"}} </s>"
    }
    # ৫০০টি সাধারণ হ্যাম এক্সাম্পল
    ham_entry = {
        "text": f"<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\nHello team, this is regular business report update #{i} for the archive. [/INST] {{\"is_spam\": false, \"ai_summary\": \"Regular secure corporate message update #{i}.\"}} </s>"
    }
    dataset.append(spam_entry)
    dataset.append(ham_entry)

# JSONL ফাইলে রাইট করা
with open("dataset.jsonl", "w", encoding="utf-8") as f:
    for entry in dataset:
        f.write(json.dumps(entry) + "\n")

print("✅ [DATASET GENERATED]: 1000 optimized training rows saved into dataset.jsonl!")
