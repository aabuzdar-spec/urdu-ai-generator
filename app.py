import io
import random
import urllib.parse
from deep_translator import GoogleTranslator
from PIL import Image
import requests
import streamlit as st

st.set_page_config(
    page_title="Urdu AI Studio Pro", page_icon="🎨", layout="centered"
)

# Custom CSS
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
    '<p class="sub-text">مفت اور پرفیکٹ فوکس کے ساتھ HD تصاویر بنائیں!</p>',
    unsafe_allow_html=True,
)

user_prompt = st.text_input(
    "تصویر کی تفصیل (Urdu / English):",
    placeholder="مثال: ایک آدمی اور ایک کتا اکٹھے بیٹھے ہیں",
)

style = st.selectbox(
    "تصویر کا آرٹ سٹائل منتخب کریں:",
    [
        "Photorealistic (بالکل اصلی اور وائڈ فوکس)",
        "Ultra Detailed Portrait (تفصیلی پورٹریٹ)",
        "3D Pixar / Animation (کارٹون سٹائل)",
        "Oil Painting (روایتی پینٹنگ)",
    ],
)

if st.button("✨ HD تصویر تیار کریں (Generate Image)"):
    if user_prompt:
        with st.spinner("تصویر پروسیس اور فوکس کی جا رہی ہے..."):
            try:
                translated_prompt = GoogleTranslator(
                    source="auto", target="en"
                ).translate(user_prompt)

                unwanted_words = [
                    "picture of",
                    "image of",
                    "draw a",
                    "make a",
                    "photo of",
                    "ki tasveer",
                    "tasveer banao",
                ]
                clean_prompt = translated_prompt.lower()
                for word in unwanted_words:
                    clean_prompt = clean_prompt.replace(word, "")

                # Strict multi-subject composition keywords added at the front
                style_enhancers = {
                    "Photorealistic (بالکل اصلی اور وائڈ فوکس)": "wide shot, full body shot, both subjects visible together in frame, sharp focus, 8k resolution, clear details, professional photography",
                    "Ultra Detailed Portrait (تفصیلی پورٹریٹ)": "medium shot showing both subjects, sharp focus, crisp details, 8k resolution",
                    "3D Pixar / Animation (کارٹون سٹائل)": "wide shot 3d render, pixar character style, vibrant lighting, sharp focus",
                    "Oil Painting (روایتی پینٹنگ)": "masterpiece oil painting, clear composition showing all elements, sharp focus",
                }

                # Force framing setup before the translated prompt
                enhanced_prompt = f"{style_enhancers[style]}, {clean_prompt.strip()}, high clarity, fully in focus"
                st.info(f"🔍 **Auto-Enhanced Prompt:** {enhanced_prompt}")

                # Random seed generation for dynamic render
                random_seed = random.randint(1, 99999)
                encoded_prompt = urllib.parse.quote(enhanced_prompt)

                # Using Flux model with enhanced framing logic
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true&seed={random_seed}"

                response = requests.get(image_url)
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

            except Exception as e:
                st.error(f"تصویر بنانے میں کوئی مسئلہ پیش آیا: {e}")
    else:
        st.warning("براہِ کرم پہلے تصویر کی کوئی تفصیل درج کریں۔")
