import streamlit as st
import fitz
from PIL import Image
import io

st.title("PDF Compressor")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    image_list = []
    target_size_bytes = 500 * 1024
    
    for page in doc:
        pix = page.get_pixmap(dpi=150)
        img = Image.open(io.BytesIO(pix.tobytes()))
        
        for quality in range(95, 5, -5):
            temp_stream = io.BytesIO()
            img.save(temp_stream, format="JPEG", quality=quality)
            if temp_stream.tell() <= target_size_bytes:
                break
                
        compressed_img = Image.open(temp_stream)
        image_list.append(compressed_img)
        
    pdf_bytes = io.BytesIO()
    if image_list:
        image_list[0].save(pdf_bytes, format="PDF", save_all=True, append_images=image_list[1:])
        
    st.success("Compression Complete!")
    st.download_button("Download Compressed PDF", data=pdf_bytes.getvalue(), file_name="compressed.pdf", mime="application/pdf")