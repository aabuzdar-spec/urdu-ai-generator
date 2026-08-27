import streamlit as st
from deep_translator import GoogleTranslator
import requests
import io
from PIL import Image

# Streamlit UI Setup
st.set_page_config(page_title="Urdu AI Generator", page_icon="🎨")
st.title("🎨 ہمارا AI جنریٹر")
st.write("کوئی بھی تفصیل اردو یا انگریزی میں لکھیں اور مفت تصویر بنائیں!")

# User Input
user_prompt = st.text_input("یہاں اپنی تصویر کی تفصیل لکھیں:", "ایک خوبصورت وادی میں سورج غروب ہو رہا ہے")

# Hugging Face Free API Endpoint
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

def generate_image(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, json=payload)
    return response.content

if st.button("تصویر بنائیں (Generate Image)"):
    if user_prompt:
        with st.spinner("اردو کا ترجمہ اور تصویر تیار کی جا رہی ہے..."):
            try:
                # 1. Translate Urdu to English
                translated_prompt = GoogleTranslator(source='auto', target='en').translate(user_prompt)
                st.info(f"English Prompt: {translated_prompt}")
                
                # 2. Call Hugging Face API
                image_bytes = generate_image(translated_prompt)
                image = Image.open(io.BytesIO(image_bytes))
                
                # 3. Display Image
                st.image(image, caption="آپ کی تیار کردہ تصویر", use_container_width=True)
            except Exception as e:
                st.error("تصویر بنانے میں کوئی مسئلہ پیش آیا ہے۔ براہِ کرم دوبارہ کوشش کریں۔")
    else:
        st.warning("براہِ کرم پہلے کوئی کیپشن لکھیں۔")
