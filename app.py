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
    '<p class="sub-text">واضح اور سادہ طریقہ کار کے ساتھ AI تصاویر بنائیں!</p>',
    unsafe_allow_html=True,
)

user_prompt = st.text_input(
    "تصویر کی تفصیل (Urdu / English):",
    placeholder="مثال: ایک عورت اور ایک بلی ایک ساتھ بیٹھے ہیں",
)

style = st.selectbox(
    "تصویر کا آرٹ سٹائل منتخب کریں:",
    [
        "Photorealistic (قدرتی منظر)",
        "Digital Art (ڈیجیٹل آرٹ)",
        "3D Pixar Animation (کارٹون سٹائل)",
        "Oil Painting (روایتی پینٹنگ)",
    ],
)

if st.button("✨ HD تصویر تیار کریں (Generate Image)"):
    if user_prompt:
        with st.spinner("تصویر تیار کی جا رہی ہے..."):
            try:
                # 1. Translate Urdu to English directly
                translated_prompt = GoogleTranslator(
                    source="auto", target="en"
                ).translate(user_prompt)

                # Clean unwanted phrase words
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

                # 2. Minimal, clean enhancers to avoid ignoring the main subject
                style_enhancers = {
                    "Photorealistic (قدرتی منظر)": "realistic photo, high quality, clear details",
                    "Digital Art (ڈیجیٹل آرٹ)": "clean digital art, vivid colors, high resolution",
                    "3D Pixar Animation (کارٹون سٹائل)": "3d animated style, colorful, clear characters",
                    "Oil Painting (روایتی پینٹنگ)": "oil painting style, artistic composition",
                }

                # Subject goes FIRST, style goes LAST
                enhanced_prompt = (
                    f"{clean_prompt.strip()}, {style_enhancers[style]}"
                )
                st.info(f"🔍 **Prompt:** {enhanced_prompt}")

                random_seed = random.randint(1, 99999)
                encoded_prompt = urllib.parse.quote(enhanced_prompt)

                # Using Flux model directly
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
