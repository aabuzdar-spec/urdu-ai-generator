import io
import urllib.parse
from deep_translator import GoogleTranslator
from PIL import Image
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Urdu AI Studio Pro", page_icon="🎨", layout="centered"
)

# Custom CSS for Colorful UI
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #0f172a 100%);
        color: #ffffff;
    }
    .main-header {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 5px;
    }
    .sub-text {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #6366f1;
        background-color: #1e293b;
        color: #ffffff;
        font-size: 1.1rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    '<h1 class="main-header">🎨 اردو AI امیج سٹوڈیو پرو</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-text">مفت اور پرفیکٹ فوکس کے ساتھ HD تصاویر بنائیں!</p>',
    unsafe_allow_html=True,
)

# User Input Box
user_prompt = st.text_input(
    "تصویر کی تفصیل (Urdu / English):",
    placeholder="مثال: ایک آدمی اور ایک کتا اکٹھے بیٹھے ہیں",
)

# Style Selection Dropdown
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
                # 1. Translate Urdu to English
                translated_prompt = GoogleTranslator(
                    source="auto", target="en"
                ).translate(user_prompt)

                # Clean instruction words
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

                # 2. Balanced & Precision Quality Boosters
                style_enhancers = {
                    "Photorealistic (بالکل اصلی اور وائڈ فوکس)": "wide shot, full scene composition, photograph, 8k resolution, sharp focus, natural lighting",
                    "Ultra Detailed Portrait (تفصیلی پورٹریٹ)": "detailed portrait, sharp focus, professional lighting, 8k resolution",
                    "3D Pixar / Animation (کارٹون سٹائل)": "3D pixar character style, bright lighting, high quality render",
                    "Oil Painting (روایتی پینٹنگ)": "masterpiece oil painting, clear brush strokes, detailed composition",
                }

                enhanced_prompt = (
                    f"{clean_prompt.strip()}, {style_enhancers[style]}"
                )
                st.info(f"🔍 **Auto-Enhanced Prompt:** {enhanced_prompt}")

                # 3. Request Image using Turbo model for exact prompt matching
                encoded_prompt = urllib.parse.quote(enhanced_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=turbo&nologo=true"

                response = requests.get(image_url)
                img = Image.open(io.BytesIO(response.content))

                # 4. Display Final Image
                st.image(
                    img,
                    caption="آپ کی تیار کردہ HD تصویر",
                    use_container_width=True,
                )

                # 5. Direct Download Button
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
