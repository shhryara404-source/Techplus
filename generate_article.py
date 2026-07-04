import json
import os
from datetime import datetime
from huggingface_hub import InferenceClient

HF_TOKEN = os.environ["HF_TOKEN"]
client = InferenceClient(token=HF_TOKEN)

topic = "پیشرفت‌های جدید در هوش مصنوعی و فناوری"

def generate_english(prompt):
    try:
        response = client.text_generation(
            model="gpt2",          # بسیار پایدار، انگلیسی
            prompt=prompt,
            max_new_tokens=600,
            temperature=0.7,
            stream=False
        )
        return response.strip()
    except Exception as e:
        print(f"خطای انگلیسی: {e}")
        return "English content not available at this moment."

def generate_persian(prompt):
    try:
        # مدل فارسی رایگان و پایدار
        response = client.text_generation(
            model="persiannlp/parsi-gpt2",
            prompt=prompt,
            max_new_tokens=600,
            temperature=0.7,
            stream=False
        )
        return response.strip()
    except Exception as e:
        print(f"خطای فارسی: {e}")
        return "محتوای فارسی در این لحظه در دسترس نیست."

prompt_en = f"Write a detailed article in English about: {topic}. Minimum 4 paragraphs."
prompt_fa = f"یک مقاله جامع به زبان فارسی درباره این موضوع بنویس: {topic}. حداقل ۴ پاراگراف."

article_en = generate_english(prompt_en)
article_fa = generate_persian(prompt_fa)

# ذخیره در فایل
with open("articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

new_id = len(articles) + 1
today = datetime.now().strftime("%Y/%m/%d")

articles.append({
    "id": new_id,
    "category": "Technology",
    "date": today,
    "title": {"fa": topic, "en": topic},
    "excerpt": {"fa": article_fa[:200] + "...", "en": article_en[:200] + "..."},
    "body": {
        "fa": f"<p>{article_fa.replace(chr(10), '</p><p>')}</p>",
        "en": f"<p>{article_en.replace(chr(10), '</p><p>')}</p>"
    }
})

with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("✅ مقاله جدید ذخیره شد.")
