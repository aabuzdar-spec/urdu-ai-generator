import streamlit as st
import torch
from deep_translator import GoogleTranslator
from diffusers import StableDiffusionPipeline

st.title("🎨 ہمارا اپنا AI جنریٹر")
st.write("کوئی بھی تفصیل اردو یا انگریزی میں لکھیں اور مفت تصویر بنائیں!")


@st.cache_resource
def load_model():
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
    )
    return pipe.to("cuda" if torch.cuda.is_available() else "cpu")


pipe = load_model()

prompt = st.text_area("پرامپٹ لکھیں:", placeholder="مثال: سرسبز پہاڑوں کے درمیان جھیل")

if st.button("تصویر بنائیں"):
    if prompt:
        with st.spinner("تصویر بن رہی ہے..."):
            translated = GoogleTranslator(source="auto", target="en").translate(
                prompt
            )
            image = pipe(translated).images[0]
            st.image(image, caption=f"ترجمہ: {translated}")
    else:
        st.warning("براہِ کرم پہلے پرامپٹ درج کریں۔")
