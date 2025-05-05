import streamlit as st
from PIL import Image, ImageFilter, ImageOps
import io

st.set_page_config(page_title="Image to Cartoon using Streamlit")
st.title("Image to Cartoon Style Generator")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    if st.button("Generate Cartoon Image"):
        with st.spinner("Processing image..."):
            # Apply cartoon effect (stylized using PIL filters)
            # Step 1: Edge enhancement
            edges = image.convert("L").filter(ImageFilter.FIND_EDGES)
            edges = ImageOps.invert(edges).convert("1")

            # Step 2: Combine with color quantized version
            color = image.convert("P", palette=Image.ADAPTIVE, colors=64).convert("RGB")
            cartoon = Image.composite(color, Image.new("RGB", image.size, (255, 255, 255)), edges)

            st.image(cartoon, caption="Cartoonized Image", use_column_width=True)
            cartoon.save("cartoon_output.png")
            with open("cartoon_output.png", "rb") as f:
                st.download_button("Download Cartoon Image", f, file_name="cartoon_image.png")
