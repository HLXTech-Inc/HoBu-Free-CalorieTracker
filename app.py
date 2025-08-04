import streamlit as st
from PIL import Image
import requests

st.set_page_config(page_title="HoBu - Free AI Calorie Tracker", layout="centered")
st.title("🍱 HoBu – Free AI Calorie Tracker")
st.write("Upload a meal photo, classify the food, and get a calorie estimate.")

calorie_lookup = {
    "pizza": 285, "burger": 354, "apple": 95,
    "banana": 105, "salad": 150, "fries": 365,
    "sushi": 200, "pasta": 310, "steak": 679,
    "sandwich": 300
}

API_URL = "https://api-inference.huggingface.co/models/dima806/food-image-classification"

def classify(image_bytes):
    try:
        response = requests.post(API_URL, files={"file": image_bytes})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error("⚠️ Network or server error: " + str(e))
        return []
    except ValueError:
        st.error("⚠️ Unexpected response format — model may be loading or busy.")
        return []


uploaded = st.file_uploader("Upload food image", type=["jpg","jpeg","png"])
if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Your Image", use_column_width=True)
    st.write("Processing…")
    result = classify(uploaded.getvalue())
    if isinstance(result, list) and result:
        label = result[0]["label"].lower()
        score = result[0]["score"]
        st.success(f"{label.capitalize()} ({score*100:.1f}%) detected.")
        kcal = calorie_lookup.get(label)
        if kcal:
            st.info(f"Estimated Calories: **{kcal} kcal**")
        else:
            st.warning("Calorie lookup not found for this food.")
    else:
        st.error("Could not classify the image.")
