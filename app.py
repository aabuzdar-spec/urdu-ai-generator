import io
import urllib.parse
from deep_translator import GoogleTranslator
from PIL import Image
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Urdu AI Studio - Studio Quality Images",
    page_icon="🎨",
    layout="centered",
)

# Custom CSS for Colorful UI
st.markdown(
    """
    <style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #0f172a 100%);
        color: #ffffff;
    }
    
    /* Header Container Styling */
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

    /* Input Field Styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #6366f1;
        background-color: #1e293b;
        color: #ffffff;
        font-size: 1.1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ec4899;
        box-shadow: 0 0 10px rgba(236, 72, 153, 0.5);
    }

    /* Button Styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(236, 72, 153, 0.6);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    '<h1 class="main-header">🎨 اردو AI امیج سٹوڈیو</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-text">اپنی سوچ کو اردو میں لکھیں اور FLUX.1 / Midjourney کوالٹی کی شاندار تصاویر حاصل کریں!</p>',
    unsafe_allow_html=True,
)

# User Input Box
user_prompt = st.text_input(
    "تصویر کی تفصیل (Urdu / English):",
    placeholder="مثال: ایک قدیم حویلی، اینٹوں کی دیواریں، پرانے درخت",
)

# Style Selection Dropdown
style = st.selectbox(
    "تصویر کا آرٹ سٹائل منتخب کریں:",
    [
        "Midjourney v6 Photorealistic (بالکل اصلی)",
        "FLUX.1 Dev Ultra Detail (انتہائی تفصیلی)",
        "Cyberpunk / Futuristic (جدید سائنسی)",
        "3D Pixar / Anime Animation (کارٹون سٹائل)",
        "Oil Painting / Classical Art (روایتی پینٹنگ)",
    ],
)

if st.button("✨ HD تصویر تیار کریں (Generate HD Image)"):
    if user_prompt:
        with st.spinner("کوئری کی پروسیسنگ اور HD تصویر رینڈر کی جا رہی ہے..."):
            try:
                # 1. Automatic Urdu to English Translation
                translated_prompt = GoogleTranslator(
                    source="auto", target="en"
                ).translate(user_prompt)

                # Clean unnecessary instruction words that confuse the AI
                unwanted_words = [
                    "picture of",
                    "image of",
                    "draw a",
                    "make a",
                    "photo of",
                    "a picture of",
                    "ki tasveer",
                    "tasveer banao",
                ]
                clean_prompt = translated_prompt.lower()
                for word in unwanted_words:
                    clean_prompt = clean_prompt.replace(word, "")

                # 2. Advanced Midjourney & FLUX.1 Automatic Prompt Enhancer
                style_enhancers = {
                    "Midjourney v6 Photorealistic (بالکل اصلی)": "shot on 35mm lens, photorealistic, 8k resolution, volumetric lighting, depth of field, masterpiece, trending on ArtStation",
                    "FLUX.1 Dev Ultra Detail (انتہائی تفصیلی)": "FLUX.1-dev style, ultra detailed, octane render, unreal engine 5, hyperrealistic, sharp focus, 8k studio quality",
                    "Cyberpunk / Futuristic (جدید سائنسی)": "cyberpunk style, neon aesthetic, glowing lights, highly detailed futuristic city, 8k resolution, cinematic composition",
                    "3D Pixar / Anime Animation (کارٹون سٹائل)": "3D Pixar animation style, vibrant colors, cute characters, ray tracing, Octane Render, 8k high quality",
                    "Oil Painting / Classical Art (روایتی پینٹنگ)": "oil painting style, rich textures, expressive brush strokes, masterpiece, classical art look, fine art gallery quality",
                }

                enhanced_prompt = (
                    f"{clean_prompt.strip()}, {style_enhancers[style]}"
                )
                st.info(f"🔍 **Auto-Enhanced Prompt:** {enhanced_prompt}")

                # 3. Request Image from Pollinations High-Quality Flux Pipeline
                encoded_prompt = urllib.parse.quote(enhanced_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"

                # Fetch Image Bytes for display and direct Download option
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
