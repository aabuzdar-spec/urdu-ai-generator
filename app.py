# 1. Translate Prompt
translated_prompt = translate_to_english(user_prompt_urdu)

# Clean prompt
unwanted_words = [
    "make a",
    "draw a",
    "create a",
    "picture of",
    "image of",
    "banao",
    "bnao",
    "ek",
]
clean_prompt = translated_prompt.lower()
for w in unwanted_words:
    clean_prompt = clean_prompt.replace(w, "")

# اگر یوزر نے دو چیزوں کا ذکر کیا ہے تو AI کو صاف اور واضح پرامپٹ بھیجیں
# Enhancing structure for multiple subjects
final_subject = clean_prompt.strip()

# 2. Styles Definition & Prompt Assembly
# ہم نے یہاں clarity اور subject definition کو پہلے نمبر پر رکھا ہے
final_prompt = f"a clear detailed picture of {final_subject}, distinct features, {scene_details}, {style_enhancers[style]}"
