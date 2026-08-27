import urllib.parse
from deep_translator import GoogleTranslator
import streamlit as st

# Streamlit UI Setup
st.set_page_config(page_title="HD Urdu AI Generator", page_icon="🎨")
st.title("🎨 ہمارا AI جنریٹر (HD Quality)")
st.write("کوئی بھی تفصیل اردو یا انگریزی میں لکھیں اور HD تصویر بنائیں!")

# User Input
user_prompt = st.text_input(
    "یہاں اپنی تصویر کی تفصیل لکھیں:", "ایک خوبصورت نہر اور سرسبز درخت"
)

# Quality Enhancers
style = st.selectbox(
    "تصویر کا سٹائل منتخب کریں:",
    ["Photorealistic (اصلی تصویر)", "Digital Art", "Anime / Cartoon", "3D Render"],
)

if st.button("HD تصویر بنائیں (Generate Image)"):
    if user_prompt:
        with st.spinner("تصویر کو HD کوالٹی میں تیار کیا جا رہا ہے..."):
            try:
                # 1. Translate Urdu to English
                translated_prompt = GoogleTranslator(
                    source="auto", target="en"
                ).translate(user_prompt)

                # 2. Add HD keywords based on style
                hd_prompt = f"{translated_prompt}, {style}, highly detailed, 8k resolution, photorealistic, sharp focus, masterpiece"
                st.info(f"English Prompt: {hd_prompt}")

                # 3. Encode Prompt with Flux Model (High Quality)
                encoded_prompt = urllib.parse.quote(hd_prompt)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1084&height=1084&model=flux&nologo=true"

                # 4. Display Image
                st.image(
                    image_url,
                    caption="آپ کی تیار کردہ HD تصویر",
                    use_container_width=True,
                )

            except Exception as e:
                st.error(f"تصویر بنانے میں کوئی مسئلہ پیش آیا: {e}")
    else:
        st.warning("براہِ کرم پہلے کوئی کیپشن لکھیں۔")
