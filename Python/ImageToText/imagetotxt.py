import streamlit as st
from PIL import Image
import pytesseract
import io

# Optional: If tesseract is installed in a non-standard location, specify the path here
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_tesseract_executable>'

st.set_page_config(page_title="Image to Text OCR App", page_icon="✍️", layout="centered")

st.title("Image to Text OCR Converter")
st.write("Upload an image containing text, and this app will extract and display the text using OCR.")

uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg", "bmp", "tiff"])

if uploaded_file is not None:
    try:
        # Read image as PIL Image
        image = Image.open(io.BytesIO(uploaded_file.read()))
        st.image(image, caption="Uploaded Image", use_container_width=True)  # Updated line
        
        # Perform OCR
        with st.spinner("Extracting text from image..."):
            text = pytesseract.image_to_string(image)
        
        st.subheader("Extracted Text:")
        if text.strip():
            st.text_area("Text output", value=text, height=250)
        else:
            st.warning("No text detected in the image.")
    except Exception as e:
        st.error(f"An error occurred while processing the image: {e}")

if st.button("About"):
    st.info(
        """
        This app uses the [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) engine via the **pytesseract** Python wrapper.
        \n
        - Supports multiple image formats: PNG, JPG, BMP, TIFF.
        - Works best on clear, high-contrast images containing readable text.
        - For best results, use scanned documents or high-quality images.
        \n
        Developed with Streamlit for quick and easy web UI.
        """
    )
