import io
import json
import random
import urllib.parse
from PIL import Image
import requests
import streamlit as st

st.set_page_config(
    page_title="Urdu AI Studio Pro", page_icon="🎨", layout="centered"
)

# Custom CSS Styles
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #0f172a 100%); color: #ffffff; }
    .main-header {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 50%, #3b82f6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; font-weight: 800; font-size: 2.8rem; margin-bottom: 5px;
    }
    .sub-text { text-align: center; color: #cbd5e1; font-size: 1.1rem; margin-bottom: 25px; }
    .stTextInput > div > div > input { border-radius: 12px; border: 2px solid #6366f1; background-color: #1e293b; color: #ffffff; font-size: 1.1rem; }
    .stButton > button {
        width: 100%; background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        color: white; border: none; padding: 12px 24px; font-size: 1.2rem; font-weight: bold; border-radius: 12px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="main-header">🎨 اردو AI امیج سٹوڈیو پرو</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-text">بغیر کسی ایرر کے 100% پرفیکٹ اور الٹرا ایچ ڈی تصاویر بنائیں!</p>',
    unsafe_allow_html=True,
)


# Robust Urdu Translation Function (Bypasses Deep Translator Errors)
def safe_translate(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={urllib.parse.quote(text)}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            result = res.json()
            translated = result[0][0][0]
            # Verify if translation isn't an error message
            if "error" not in translated.lower():
                return translated
    except Exception:
        pass
    return text  # Fallback to original input if translation fails


user_prompt = st.text_input(
    "تصویر کی تفصیل (Urdu / English):",
    placeholder="مثال: ایک آدمی ہوا میں اڑ رہا ہے",
)

style = st.selectbox(
    "تصویر کا آرٹ سٹائل منتخب کریں:",
    [
        "Photorealistic (بالکل اصلی اور شفاف)",
        "3D Pixar Animation (کارٹون سٹائل)",
        "Digital Art (ڈیجیٹل آرٹ)",
    ],
)

if st.button("✨ HD تصویر تیار کریں (Generate Image)"):
    if user_prompt:
        with st.spinner("تیزی سے تصویر پروسیس کی جا رہی ہے..."):
            try:
                # 1. Clean and Safe Translation
                translated_prompt = safe_translate(user_prompt)

                # Remove filler noise
                unwanted_words = [
                    "picture of",
                    "image of",
                    "draw a",
                    "make a",
                    "photo of",
                    "ki tasveer",
                    "tasveer banao",
                    "banao",
                ]
                clean_prompt = translated_prompt.lower()
                for word in unwanted_words:
                    clean_prompt = clean_prompt.replace(word, "")

                # 2. Optimized Prompt Architecture
                style_enhancers = {
                    "Photorealistic (بالکل اصلی اور شفاف)": "photograph, highly detailed, sharp focus, 8k resolution, crisp subject",
                    "3D Pixar Animation (کارٹون سٹائل)": "3d pixar style animation, vibrant colors, clear rendering",
                    "Digital Art (ڈیجیٹل آرٹ)": "clean digital art illustration, sharp edges, high resolution",
                }

                final_prompt = (
                    f"{clean_prompt.strip()}, {style_enhancers[style]}"
                )
                st.info(f"🔍 **Optimized AI Prompt:** {final_prompt}")

                # 3. Direct Image Generation
                random_seed = random.randint(1, 999999)
                encoded = urllib.parse.quote(final_prompt)

                # Using stable Pollinations Flux without broken parameters
                img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&model=flux&nologo=true&seed={random_seed}"

                response = requests.get(img_url, timeout=45)

                if response.status_code == 200:
                    img = Image.open(io.BytesIO(response.content))
                    st.image(
                        img,
                        caption="آپ کی تیار کردہ HD تصویر",
                        use_container_width=True,
                    )

                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    byte_im = buf.getvalue()

                    st.download_button(
                        label="📥 تصویر ڈاؤن لوڈ کریں (Download Image)",
                        data=byte_im,
                        file_name="ai_image.png",
                        mime="image/png",
                    )
                else:
                    st.error(
                        "سرور اس وقت مصروف ہے، براہ کرم 5 سیکنڈ بعد دوبارہ کوشش کریں۔"
                    )

            except Exception as e:
                st.error(f"پروسیسنگ میں مسئلہ آیا: {e}")
    else:
        st.warning("براہِ کرم پہلے تصویر کی کوئی تفصیل درج کریں۔")
