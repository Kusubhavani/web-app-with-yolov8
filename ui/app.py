import streamlit as st
import requests
from PIL import Image
import os

st.set_page_config(page_title="YOLOv8 Object Detection", layout="wide")
st.title("YOLOv8 Object Detection")

# Get API URL from environment variable
API_URL = os.getenv("API_URL", "http://api:8000/detect")

st.sidebar.header("Settings")
confidence = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Detect Objects"):
        with st.spinner("Detecting..."):
            files = {"image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"confidence_threshold": confidence}
            try:
                response = requests.post(API_URL, files=files, data=data)
                if response.status_code == 200:
                    result = response.json()
                    st.success("Detection complete!")
                    with col2:
                        st.subheader("Detection Results")
                        detections = result.get("detections", [])
                        summary = result.get("summary", {})
                        if detections:
                            st.write(f"**Total objects detected:** {len(detections)}")
                            st.write("**Summary by class:**")
                            for label, count in summary.items():
                                st.write(f"- {label}: {count}")
                            st.write("**Detections:**")
                            for i, d in enumerate(detections):
                                st.write(f"{i+1}. {d['label']} (score: {d['score']:.2f}) at box {d['box']}")
                        else:
                            st.write("No objects detected.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")