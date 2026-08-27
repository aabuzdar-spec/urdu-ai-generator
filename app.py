import io
import urllib.parse
from deep_translator import GoogleTranslator
from PIL import Image
import requests
import streamlit as st

# Streamlit UI Setup
st.set_page_config(page_title="Urdu AI Image & Video Generator", page_icon="🎬")
st.title("🎬 ہمارا AI تصویر اور ویڈیو جنریٹر")
st.write(
    "کوئی بھی تفصیل اردو یا انگریزی میں لکھیں اور مفت HD تصویر یا ویڈیو بنائیں!"
)

# Mode Selection
mode = st.radio("آپ کیا بنانا چاہتے ہیں؟", ["تصویر (Image)", "ویڈیو (Video)"])

# User Input
user_prompt = st.text_input(
    "یہاں اپنی تفصیل لکھیں:", "ایک خوبصورت نہر اور سرسبز درخت"
)

# Quality Style Selection
style = st.selectbox(
    "سٹائل منتخب کریں:",
    ["Photorealistic (اصلی)", "Digital Art", "Anime / Cartoon", "3D Render"],
)


# Hugging Face Video Generation Function
def generate_video_hf(prompt):
    # Free Animated Video Model
    API_URL = "https://api-inference.huggingface.co/models/guoyww/animatediff-motion-adapter-v1-5-2"
    payload = {"inputs": prompt}
    response = requests.post(API_URL, json=payload, timeout=60)
    return response.content


if st.button("تخلیق کریں (Generate)"):
    if user_prompt:
        with st.spinner("اردو کا ترجمہ اور مواد تیار کیا جا رہا ہے..."):
            try:
                # 1. Translate Urdu to English
                translated_prompt = GoogleTranslator(
                    source="auto", target="en"
                ).translate(user_prompt)
                hd_prompt = f"{translated_prompt}, {style}, highly detailed, motion, cinematic video"
                st.info(f"English Prompt: {hd_prompt}")

                # 2. Generate Output based on selected Mode
                if mode == "تصویر (Image)":
                    encoded_prompt = urllib.parse.quote(hd_prompt)
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1084&height=1084&model=flux&nologo=true"
                    st.image(
                        image_url,
                        caption="آپ کی تیار کردہ HD تصویر",
                        use_container_width=True,
                    )

                elif mode == "ویڈیو (Video)":
                    st.warning(
                        "ویڈیو بننے میں 30 سے 60 سیکنڈ لگ سکتے ہیں، برائے مہربانی صبر رکھیں..."
                    )
                    video_bytes = generate_video_hf(hd_prompt)

                    # Check response
                    if (
                        b"error" in video_bytes
                        or len(video_bytes) < 50000
                    ):
                        st.error(
                            "سرور مصروف ہے یا ماڈل ڈاؤن لوڈ ہو رہا ہے۔ برائے کرم چند سیکنڈ بعد دوبارہ کوشش کریں۔"
                        )
                    else:
                        st.video(video_bytes)
                        st.success("آپ کی AI ویڈیو تیار ہے!")

            except Exception as e:
                st.error(f"مواد بنانے میں کوئی مسئلہ پیش آیا: {e}")
    else:
        st.warning("براہِ کرم پہلے کوئی تفصیل لکھیں۔")
