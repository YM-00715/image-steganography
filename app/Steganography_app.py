import streamlit as st
import importlib
from PIL import Image
import numpy as np
import io

# ----------------------------
# Utility Functions
# ----------------------------
def image_to_png_bytes(img: np.ndarray) -> bytes:
    """Convert NumPy image array to PNG bytes (lossless)."""
    pil_img = Image.fromarray(img.astype(np.uint8))
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG", compress_level=0)
    return buf.getvalue()

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Image Steganography", layout="centered")
st.title("🖼️ Modular Image Steganography Tool")

# Available methods (modules in /methods)
available_methods = {
    "LSB (Least Significant Bit)": "lsb",
    "Edge-based LSB": "edge_lsb"
}

selected_method_name = st.selectbox("Select Encoding Method", list(available_methods.keys()))
selected_method = available_methods[selected_method_name]

# Dynamically import method
try:
    method_module = importlib.import_module(f"methods.{selected_method}")
except ImportError as e:
    st.error(f"Error loading method `{selected_method}`: {e}")
    st.stop()

# ---------------- ENCODING SECTION ----------------
st.header("🔐 Encode Message into Image")

uploaded_file = st.file_uploader("Upload an image to encode", type=["png", "jpg", "jpeg"])
message = st.text_area("Enter the secret message:")

if uploaded_file is not None:
    image = np.array(Image.open(uploaded_file).convert("RGB"))
    st.image(image, caption="Original Image", use_container_width=True)

    if st.button("Encode Message"):
        if not message.strip():
            st.warning("⚠️ Please enter a secret message first.")
        else:
            try:
                encoded_image = method_module.encode(image, message)
                st.image(encoded_image, caption="Encoded Image", use_container_width=True)

                # Convert to PNG bytes (lossless)
                encoded_bytes = image_to_png_bytes(encoded_image)

                # Download button
                st.download_button(
                    label="⬇️ Download Encoded Image (PNG)",
                    data=encoded_bytes,
                    file_name="encoded_image.png",
                    mime="image/png"
                )
                st.success("✅ Encoding successful! You can now download the encoded image.")
            except Exception as e:
                st.error(f"Encoding error: {e}")

# ---------------- DECODING SECTION ----------------
st.header("🔓 Decode Message from Image")

decode_file = st.file_uploader("Upload an encoded PNG image to decode", type=["png"])

if decode_file is not None:
    try:
        encoded_image = np.array(Image.open(decode_file).convert("RGB"))
        decoded_message = method_module.decode(encoded_image)
        st.success(f"💬 Decoded Message:\n\n**{decoded_message}**")
    except Exception as e:
        st.error(f"Decoding error: {e}")
