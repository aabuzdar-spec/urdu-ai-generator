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

# Custom CSS Styles (Improved layout)
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
    '<p class="sub-text">بغیر کسی ایرر کے 100% پرفیکٹ، مکمل منظر یا پورٹریٹ، آپ کی مرضی کی تصاویر بنائیں!</p>',
    unsafe_allow_html=True,
)


# Robust Urdu Translation Function
def safe_translate(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={urllib.parse.quote(text)}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            result = res.json()
            translated = result[0][0][0]
            if "error" not in translated.lower():
                return translated
    except Exception:
        pass
    return text


user_prompt = st.text_input(
    "تصویر کی تفصیل (Urdu / English):",
    placeholder="مثال: ایک آدمی ہوا میں اڑ رہا ہے",
)

# New Feature: Let user choose the composition (Full Scene or Portrait)
composition = st.radio(
    "تصویر کی ساخت (Composition) منتخب کریں:",
    [
        "Full Scene (مکمل منظر، وائڈ شارٹ)",
        "Portrait (قریبی شاٹ، پورٹریٹ)",
    ],
)

style = st.selectbox(
    "تصویر کا آرٹ سٹائل منتخب کریں:",
    [
        "Photorealistic (بالکل اصلی اور شفاف)",
        "3D Animation (کارٹون سٹائل)",
        "Digital Painting (ڈیجیٹل آرٹ)",
        "Oil Painting (روایتی پینٹنگ)",
    ],
)

if st.button("✨ HD تصویر تیار کریں (Generate Image)"):
    if user_prompt:
        with st.spinner("تیزی سے تصویر پروسیس کی جا رہی ہے..."):
            try:
                translated_prompt = safe_translate(user_prompt)

                unwanted_words = [
                    "picture of", "image of", "draw a", "make a",
                    "photo of", "ki tasveer", "tasveer banao", "banao",
                ]
                clean_prompt = translated_prompt.lower()
                for word in unwanted_words:
                    clean_prompt = clean_prompt.replace(word, "")

                # 1. Base style prompts
                style_enhancers = {
                    "Photorealistic (بالکل اصلی اور شفاف)": "realistic photograph, highly detailed, crisp focus, 8k resolution, sharp subject",
                    "3D Animation (کارٹون سٹائل)": "3d animated style, vibrant colorful scene, clear rendering, highly detailed",
                    "Digital Painting (ڈیجیٹل آرٹ)": "clean digital art painting, crisp lines, clean colors, high resolution",
                    "Oil Painting (روایتی پینٹنگ)": "oil painting masterpiece, classical art style, deep texture, rich colors, fully focused composition",
                }

                # 2. Add composition words
                # These words are used to guide AI, not block words
                if composition == "Full Scene (مکمل منظر، وائڈ شارٹ)":
                    scene_prompt = f"environmental portrait, wide angle shot, full shot showing whole scene and surroundings, {style_enhancers[style]}"
                else:
                    scene_prompt = f"portrait shot, large head and shoulders, close-up shot, shallow depth of field, focused on face, {style_enhancers[style]}"

                # Final prompt composition, prioritizing user prompt
                final_prompt = (
                    f"{clean_prompt.strip()}, {scene_prompt}"
                )
                st.info(f"🔍 **Optimized AI Prompt:** {final_prompt}")

                # 3. Direct Image Generation
                random_seed = random.randint(1, 999999)
                encoded = urllib.parse.quote(final_prompt)

                # Adjusted width and height for a more standard aspect ratio
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
