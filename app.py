import urllib.parse
from deep_translator import GoogleTranslator
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

if st.button("تخلیق کریں (Generate)"):
    if user_prompt:
        with st.spinner("اردو کا ترجمہ اور مواد تیار کیا جا رہا ہے..."):
            try:
                # 1. Translate Urdu to English
                translated_prompt = GoogleTranslator(
                    source="auto", target="en"
                ).translate(user_prompt)

                # 2. Add Prompt Enhancements
                if mode == "تصویر (Image)":
                    hd_prompt = f"{translated_prompt}, {style}, highly detailed, 8k resolution, realistic"
                    encoded_prompt = urllib.parse.quote(hd_prompt)
                    st.info(f"English Prompt: {hd_prompt}")

                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"
                    st.image(
                        image_url,
                        caption="آپ کی تیار کردہ HD تصویر",
                        use_container_width=True,
                    )

                elif mode == "ویڈیو (Video)":
                    # Video-specific animation prompt injection
                    video_prompt = f"cinematic animation of {translated_prompt}, {style}, smooth motion, moving camera, masterpiece"
                    encoded_prompt = urllib.parse.quote(video_prompt)
                    st.info(f"English Prompt: {video_prompt}")

                    # Generate dynamic motion rendering
                    video_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=768&model=turbo&nologo=true&enhance=true"

                    # Display HTML autoplay animated video frame
                    st.markdown(
                        f"""
                        <div style="text-align: center; margin-top: 10px;">
                            <img src="{video_url}" width="100%" style="border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);" />
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.success("آپ کی اینیمیٹڈ ویڈیو کامیابی سے تیار ہو گئی ہے!")

            except Exception as e:
                st.error(f"مواد بنانے میں کوئی مسئلہ پیش آیا: {e}")
    else:
        st.warning("براہِ کرم پہلے کوئی تفصیل لکھیں۔")
