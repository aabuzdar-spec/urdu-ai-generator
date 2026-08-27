# 1. Automatic Urdu to English Translation
translated_prompt = GoogleTranslator(source="auto", target="en").translate(
    user_prompt
)

# Clean unnecessary instruction words that confuse the AI
unwanted_words = [
    "picture of",
    "image of",
    "draw a",
    "make a",
    "photo of",
    "a picture of",
]
clean_prompt = translated_prompt.lower()
for word in unwanted_words:
    clean_prompt = clean_prompt.replace(word, "")

# Final prompt focusing ONLY on the subject
enhanced_prompt = f"ancient Pakistani heritage mansion, old architectural haveli, detailed facade, {style_enhancers[style]}"
