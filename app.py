import io
import random
import urllib.parse
from PIL import Image
import requests
import streamlit as st

# Function to translate Urdu to English using a public API
def translate_urdu_to_english(text):
    if not text:
        return ""
    # Try a free translation API (this is a basic method, for heavy use a paid API is better)
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=ur&tl=en&dt=t&q={urllib.parse.quote(text)}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            result = response.json()
            return result[0][0][0]  # The translated text
        else:
            return text # Fallback to original text if API fails
    except Exception as e:
        return text # Fallback to original text if there's an error

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
    '<p class="sub-text">اپنی پسندیدہ چیزیں اب اردو میں لکھیں، ہم بنائیں گے HD تصاویر!</p>',
    unsafe_allow_html=True,
)

user_prompt_urdu = st.text_input(
    "تصویر کی تفصیل (اردو میں لکھیں):",
    placeholder="مثال: ایک برفانی ریچھ بناؤ",
)

# Composition Selector
composition = st.radio(
    "تصویر کی ساخت منتخب کریں:",
    [
        "Portrait (پورٹریٹ شاٹ)",
        "Wide Shot (وائڈ سین، مکمل منظر)",
    ],
)

if st.button("✨ HD تصویر تیار کریں (Generate Image)"):
    if user_prompt_urdu:
        with st.spinner("تصویر تیار کی جا رہی ہے..."):
            try:
                # 1. Translate Urdu to English Automatically
                translated_prompt = translate_urdu_to_english(user_prompt_urdu)
                st.info(f"🔍 **AI سمجھا:** {translated_prompt}")

                # 2. Composition Enhancer
                if composition == "Portrait (پورٹریٹ شاٹ)":
                    scene_details = "portrait shot, large head and shoulders, close-up shot, shallow depth of field, focused on face"
                else:
                    scene_details = "wide shot, medium shot, environmental scene, fully showing subject clearly"

                # Style Enhancer
                style_enhancer = "realistic photograph, highly detailed, crisp focus, 8k resolution, sharp subject"

                # 3. Construct Final optimized prompt
                enhanced_prompt = f"{scene_details}, {style_enhancer}, {translated_prompt}"
                encoded_prompt = urllib.parse.quote(enhanced_prompt)

                # Fetch Image from Pollinations
                random_seed = random.randint(1, 99999)
                # Ensure width and height are appropriate for composition
                if composition == "Portrait (پورٹریٹ شاٹ)":
                     image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true&seed={random_seed}"
                else:
                     image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&model=flux&nologo=true&seed={random_seed}"

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
