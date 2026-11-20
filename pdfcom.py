import streamlit as st
import fitz
from PIL import Image
import io
st.title("PDF Compressor")
uploaded_file = st.file_uploader("Upload PDF", type="pdf")
if uploaded_file is not None:
  doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
image_list = []
for page in doc:
  pix = page.get_pixmap(dpi=150)
img = Image.open(io.BytesIO(pix.tobytes()))
low = 10
high = 95
best_stream = None
while low <= high:
                mid = (low + high) // 2
                temp_stream = io.BytesIO()
                img.save(temp_stream, format="JPEG", quality=mid)
                size = temp_stream.tell()
if 480 * 1024 <= size <= 500 * 1024:
                    best_stream = temp_stream
                    break
elif size < 480 * 1024:
                    best_stream = temp_stream
                    low = mid + 1
else:
                    high = mid - 1
best_stream.seek(0)
compressed_img = Image.open(best_stream)
image_list.append(compressed_img)
pdf_bytes = io.BytesIO()
if image_list:
  image_list[0].save(pdf_bytes, format="PDF", save_all=True, append_images=image_list[1:])
st.success("Compression Complete!")
st.download_button("Download Compressed PDF", data=pdf_bytes.getvalue(), file_name="compressed.pdf", mime="application/pdf")
