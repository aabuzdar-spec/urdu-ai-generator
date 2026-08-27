import io
import requests
import streamlit as st
from deep_translator import GoogleTranslator
from PIL import Image

st.set_page_config(page_title="AI Image Generator", page_icon="🎨")

st.title("🎨 ہمارا اپنا AI جنریٹر")
st.write("کوئی بھی تفصیل اردو یا انگریزی میں لکھیں اور مفت تصویر بنائیں!")

# Hugging Face Free Inference API URL
API_URL = (
    "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
)


def query_api(payload):
    response = requests.post(API_URL, json=payload)
    return response.content


prompt = st.text_area(
    "پرامپٹ لکھیں:",
    placeholder="مثال: سرسبز پہاڑوں کے درمیان خوبصورت جھیل",
)

if st.button("تصویر بنائیں"):
    if prompt:
        with st.spinner("تصویر بن رہی ہے..."):
            try:
                # اردو سے انگلش ترجمہ
                translated = GoogleTranslator(
                    source="auto", target="en"
                ).translate(prompt)

                # API کے ذریعے تصویر جنریٹ کرنا
                image_bytes = query_api({"inputs": translated})
                image = Image.open(io.BytesIO(image_bytes))

                st.image(image, caption=f"ترجمہ: {translated}")
            except Exception as e:
                st.error(
                    "تصویر بنانے میں مسئلہ آیا، براہِ کرم دوبارہ کوشش کریں۔"
                )
    else:
        st.warning("براہِ کرم پہلے پرامپٹ درج کریں۔")
