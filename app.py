import streamlit as st
from deep_translator import GoogleTranslator
import urllib.parse

# Streamlit UI Setup
st.set_page_config(page_title="Urdu AI Generator", page_icon="🎨")
st.title("🎨 ہمارا AI جنریٹر")
st.write("کوئی بھی تفصیل اردو یا انگریزی میں لکھیں اور مفت تصویر بنائیں!")

# User Input
user_prompt = st.text_input("یہاں اپنی تصویر کی تفصیل لکھیں:", "ایک نہر کی تصویر بناؤ")

if st.button("تصویر بنائیں (Generate Image)"):
    if user_prompt:
        with st.spinner("اردو کا ترجمہ اور تصویر تیار کی جا رہی ہے..."):
            try:
                # 1. Translate Urdu to English
                translated_prompt = GoogleTranslator(source='auto', target='en').translate(user_prompt)
                st.info(f"English Prompt: {translated_prompt}")
                
                # 2. Encode Prompt for Pollinations API (Free & Unlimited)
                encoded_prompt = urllib.parse.quote(translated_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed=42&nologo=true"
                
                # 3. Display Image directly from URL
                st.image(image_url, caption="آپ کی تیار کردہ تصویر", use_container_width=True)
                
            except Exception as e:
                st.error(f"تصویر بنانے میں کوئی مسئلہ پیش آیا: {e}")
    else:
        st.warning("براہِ کرم پہلے کوئی کیپشن لکھیں۔")
