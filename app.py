import io
import random
import urllib.parse
from PIL import Image
import requests
import streamlit as st
from googletrans import Translator # We now use this reliable library

st.set_page_config(
    page_title="Urdu AI Studio Pro", page_icon="🎨", layout="centered"
)

# Custom CSS Styles (Enhanced UI with all options)
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #1e1e2f 0%, #0f172a 100%); color: #ffffff; }
    .main-header {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 50%, #3b82f6 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; font-weight: 800; font-size: 3.2rem; margin-bottom: 5px;
    }
    .sub-text { text-align: center; color: #cbd5e1; font-size: 1.3rem; margin-bottom: 30px; }
    .stTextInput > div > div > input { border-radius: 12px; border: 2px solid #6366f1; background-color: #1e293b; color: #ffffff; font-size: 1.1rem; }
    .stButton > button {
        width: 100%; background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        color: white; border: none; padding: 14px 28px; font-size: 1.3rem; font-weight: bold; border-radius: 12px;
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
    '<p class="sub-text">اپنی پسندیدہ چیزیں اردو میں لکھیں، ہم بنائیں گے الٹرا HD تصاویر!</p>',
    unsafe_allow_html=True,
)

user_prompt_urdu = st.text_input(
    "تصویر کی تفصیل (اردو میں لکھیں):",
    placeholder="مثال: ایک برفانی ریچھ بناؤ",
)

# Composition Selector
composition = st.radio(
    "تصویر کی ساخت (Composition) منتخب کریں:",
    [
        "Portrait (قریبی شاٹ، پورٹریٹ)",
        "Wide Shot (مکمل منظر، وائڈ سین)",
    ],
)

# restored all style options
style = st.selectbox(
    "تصویر کا آرٹ سٹائل منتخب کریں:",
    [
        "Photorealistic (بالکل اصلی اور شفاف)",
        "3D Pixar Animation (کارٹون سٹائل)",
        "Pixel Art (پکسل آرٹ)",
        "Oil Painting (روایتی پینٹنگ)",
        "Watercolor (واٹر کلر آرٹ)",
        "Vaporwave (ویپر ویو سٹائل)",
        "Comic Book (کامک بک سٹائل)",
    ],
)

if st.button("✨ HD تصویر تیار کریں (Generate Image)"):
    if user_prompt_urdu:
        with st.spinner("تصویر تیار کی جا رہی ہے..."):
            try:
                # 1. New, more robust translation logic
                translator = Translator()
                translated = translator.translate(user_prompt_urdu, src='ur', dest='en')
                translated_prompt = translated.text
                
                if translated_prompt.strip() == user_prompt_urdu.strip():
                     # Fallback logic if googletrans fails: use the original text with a warning
                     # but in practice, googletrans is much more reliable than our manual function.
                     translated_prompt = f"error translating Urdu prompt: {user_prompt_urdu}"
                
                st.info(f"🔍 **AI سمجھا:** {translated_prompt}")

                # 2. Add style and composition enhancers
                style_enhancers = {
                    "Photorealistic (بالکل اصلی اور شفاف)": "realistic photograph, highly detailed, crisp focus, 8k resolution, sharp subject",
                    "3D Pixar Animation (کارٹون سٹائل)": "3d animated style, vibrant colorful scene, clear rendering",
                    "Pixel Art (پکسل آرٹ)": "pixel art illustration, retro game style, defined pixels, clean composition",
                    "Oil Painting (روایتی پینٹنگ)": "oil painting style, classical art, deep texture, classical lighting",
                    "Watercolor (واٹر کلر آرٹ)": "watercolor painting, soft colors, transparent layers, artistic style",
                    "Vaporwave (ویپر ویو سٹائل)": "vaporwave aesthetic, pastel colors, retro 80s feel, neon lighting",
                    "Comic Book (کامک بک سٹائل)": "comic book illustration, bold lines, dramatic lighting, vivid colors",
                }

                if composition == "Portrait (قریبی شاٹ، پورٹریٹ)":
                    scene_details = "portrait shot, close-up shot, shallow depth of field, focused on face"
                    width, height = 1024, 1024
                else:
                    scene_details = "wide angle shot, medium shot, fully showing subject and environment clearly"
                    width, height = 1280, 720

                # 3. Construct Final optimized prompt
                enhanced_prompt = f"{scene_details}, {style_enhancers[style]}, {translated_prompt}"
                encoded_prompt = urllib.parse.quote(enhanced_prompt)

                # Fetch Image from Pollinations
                random_seed = random.randint(1, 999999)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true&seed={random_seed}"

                response = requests.get(image_url)
                img = Image.open(io.BytesIO(response.content))

                st.image(
                    img,
                    caption=f"آپ کی تیار کردہ HD تصویر",
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
