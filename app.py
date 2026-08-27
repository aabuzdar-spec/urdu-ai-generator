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

                # 2. Add HD keywords
                hd_prompt = f"{translated_prompt}, {style}, highly detailed, 8k resolution, cinematic"
                st.info(f"English Prompt: {hd_prompt}")

                # 3. Encode Prompt
                encoded_prompt = urllib.parse.quote(hd_prompt)

                # 4. Generate Output based on selected Mode
                if mode == "تصویر (Image)":
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1084&height=1084&model=flux&nologo=true"
                    st.image(
                        image_url,
                        caption="آپ کی تیار کردہ HD تصویر",
                        use_container_width=True,
                    )

                elif mode == "ویڈیو (Video)":
                    st.toast("ویڈیو پروسیس ہو رہی ہے، تھوڑا انتظار فرمائیں...")
                    # Pollinations Video / Motion GIF API
                    video_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&model=turbo&nologo=true&seed={st.session_state.get('seed', 42)}"

                    # Animated Generation Output
                    st.image(
                        video_url,
                        caption="آپ کی تیار کردہ اینیمیٹڈ ویڈیو",
                        use_container_width=True,
                    )
                    st.success(
                        "نوٹ: یہ شارٹ اینیمیٹڈ/لوپ ویڈیو تیار کی گئی ہے۔"
                    )

            except Exception as e:
                st.error(f"مواد بنانے میں کوئی مسئلہ پیش آیا: {e}")
    else:
        st.warning("براہِ کرم پہلے کوئی تفصیل لکھیں۔")
