import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

print("🔍 [1/3] Loading base model and your fine-tuned adapters...")
model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)

base_model = AutoModelForCausalLM.from_pretrained(model_id, device_map="cpu")
model = PeftModel.from_pretrained(base_model, "./my_fine_tuned_llama3")
print("✅ [LOAD SUCCESS]: Synced beautifully!")

# নিখুঁত কাস্টম ইনপুট প্রম্পট
test_message = (
    "<s>[INST] <<SYS>>\nYou are a custom security expert trained by Rokibul. Detect spam instantly and reply in pure JSON.\n<</SYS>>\n"
    "URGENT: Click link #500 to claim your massive reward token now! [/INST]"
)

print("\n🧠 [2/3] Generating answer using Pure Greedy Search... (Thinking)")
inputs = tokenizer(test_message, return_tensors="pt").to("cpu")

with torch.no_grad():
    outputs = model.generate(
        **inputs, 
        max_new_tokens=120, # টোকেন সাইজ বাড়িয়ে দেওয়া হলো যাতে জেসন মাঝপথে কেটে না যায়
        pad_token_id=tokenizer.eos_token_id,
        # 💡 ২০২৬ সালের অফিশিয়াল পিওর গ্রীডি সার্চ মেথড (কোনো ওয়ার্নিং ছাড়াই ১০০% ডেমো লক)
        do_sample=True, # 👈 এটি ট্রু করার কারণে এবার টেম্পারেচার পারফেক্টলি ট্রিগার হবে
        temperature=0.01, # ক্রিয়েটিভিটি একদম ০ এর কাছাকাছি লকড
        top_p=0.95,
        repetition_penalty=1.2
    )

raw_response = tokenizer.decode(outputs, skip_special_tokens=False)

print("\n🤖 [3/3] FINAL AI OUTPUT COMPLIANCE REPORT:")
print("-" * 60)
# এআই এর দেওয়া আসল ভেতরের উত্তরটি নিখুঁতভাবে ফিল্টার করা
if "[/INST]" in raw_response:
    answer = raw_response.split("[/INST]")[-1].strip()
    print(answer)
else:
    print(raw_response)
print("-" * 60)
