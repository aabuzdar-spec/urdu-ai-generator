import io
import random
import urllib.parse
from PIL import Image
import requests
import streamlit as st
from deep_translator import GoogleTranslator  # Robust translator library

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


# Reliable Urdu to English translation
def safe_translate_urdu(text):
    try:
        translated = GoogleTranslator(source="ur", target="en").translate(text)
        if translated and translated.strip():
            return translated
    except Exception:
        pass
    return text


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

# Style Selector
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
                # 1. Translate Urdu Prompt to English
                translated_prompt = safe_translate_urdu(user_prompt_urdu)

                # Remove extra noise words
                unwanted_words = [
                    "make a",
                    "draw a",
                    "create a",
                    "picture of",
                    "image of",
                    "banao",
                ]
                clean_prompt = translated_prompt.lower()
                for w in unwanted_words:
                    clean_prompt = clean_prompt.replace(w, "")

                st.info(f"🔍 **AI سمجھا:** {clean_prompt.strip()}")

                # 2. Add style and composition enhancers
                style_enhancers = {
                    "Photorealistic (بالکل اصلی اور شفاف)": "realistic photograph, highly detailed, 8k resolution, crisp focus",
                    "3D Pixar Animation (کارٹون سٹائل)": "3d pixar style animation, vibrant colors, clean render",
                    "Pixel Art (پکسل آرٹ)": "pixel art illustration, retro game style, defined pixels",
                    "Oil Painting (روایتی پینٹنگ)": "oil painting masterpiece, classical canvas texture, rich colors",
                    "Watercolor (واٹر کلر آرٹ)": "watercolor painting, soft artistic color palette",
                    "Vaporwave (ویپر ویو سٹائل)": "vaporwave aesthetic, 80s neon style, pastel tones",
                    "Comic Book (کامک بک سٹائل)": "comic book art, bold outlines, vivid colors",
                }

                if composition == "Portrait (قریبی شاٹ، پورٹریٹ)":
                    scene_details = "portrait shot, close-up shot, detailed focus"
                    width, height = 1024, 1024
                else:
                    scene_details = "wide angle shot, medium shot, full environmental view"
                    width, height = 1280, 720

                # 3. Final Prompt
                final_prompt = f"{clean_prompt.strip()}, {scene_details}, {style_enhancers[style]}"
                encoded_prompt = urllib.parse.quote(final_prompt)

                # Fetch Image from Pollinations API
                random_seed = random.randint(1, 999999)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true&seed={random_seed}"

                response = requests.get(image_url, timeout=45)

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
                    st.error("تصویر بنانے میں سرور کا مسئلہ آیا، دوبارہ کوشش کریں۔")

            except Exception as e:
                st.error(f"پروسیسنگ میں مسئلہ آیا: {e}")
    else:
        st.warning("براہِ کرم پہلے تصویر کی کوئی تفصیل درج کریں۔")
