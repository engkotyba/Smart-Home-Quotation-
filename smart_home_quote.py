import streamlit as st
from datetime import datetime
from fpdf import FPDF
import tempfile
import os
import base64

# --- Utility: Convert image to base64 ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# --- Load icons/images ---
whatsapp_icon_b64 = get_base64_image("static/whatsapp.png")
logo_b64 = get_base64_image("static/logo.png")
stamp_b64 = get_base64_image("static/stamp_signature.png")

# --- Inject CSS ---
st.markdown(f"""
<style>
    /* REMOVE STREAMLIT DEFAULT HEADER, MENU & FOOTER COMPLETELY */
    #MainMenu, header, footer {{display: none !important;}}
    section[data-testid="stHeader"] {{display: none !important;}}
    div.block-container {{padding-top: 2rem !important;}}

    /* Button styling */
    div.stButton > button {{
        width: 100%;
    }}
    
    /* Center main content */
    .main .block-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 700px;
        margin: auto;
        padding-top: 20px;
    }}

    /* Mobile optimization */
    @media (max-width: 768px) {{
        .main .block-container {{
            max-width: 95% !important;
            margin: auto !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
        }}
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
    }}

    /* Floating WhatsApp button */
    .whatsapp-float {{
        position: fixed;
        width: 60px;
        height: 60px;
        bottom: 40px;
        right: 40px;
        background-color: #25d366;
        color: #FFF;
        border-radius: 50%;
        text-align: center;
        box-shadow: 2px 2px 3px #999;
        z-index: 1000;
    }}
    .whatsapp-float img {{
        margin-top: 15px;
        width: 30px;
        height: 30px;
    }}

    @media (max-width: 768px) {{
        .whatsapp-float {{
            width: 50px;
            height: 50px;
            bottom: 20px;
            right: 20px;
        }}
        .whatsapp-float img {{
            margin-top: 10px;
            width: 25px;
            height: 25px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# --- Floating WhatsApp Button ---
if whatsapp_icon_b64:
    st.markdown(f"""
    <a href="https://wa.me/971566184681" class="whatsapp-float" target="_blank">
        <img src="data:image/png;base64,{whatsapp_icon_b64}" alt="WhatsApp Icon">
    </a>
    """, unsafe_allow_html=True)
else:
    st.error("WhatsApp icon not found. Please check 'static/whatsapp.png'.")

# --- HEADER / LOGO ---
if logo_b64:
    st.markdown(
        f"<div style='text-align: center;'><img src='data:image/png;base64,{logo_b64}' width='250'></div>",
        unsafe_allow_html=True
    )
else:
    st.image("static/logo.png", width=250)

st.title("🏡 Smart Buildings Solutions Quotation")

# --- Customer Info ---
st.subheader("👤 Customer Information")
name = st.text_input("Customer Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address")

# --- Example Quotation Form ---
st.subheader("📦 Package Selection")
package = st.selectbox("Select a package", ["Basic", "Standard", "Premium"])
price = {"Basic": 1000, "Standard": 2000, "Premium": 3000}[package]

st.write(f"💰 Price: AED {price}")

# --- PDF Generation ---
if st.button("📄 Generate Quotation PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Add logo
    if logo_b64:
        logo_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        logo_file.write(base64.b64decode(logo_b64))
        logo_file.close()
        pdf.image(logo_file.name, x=80, y=10, w=50)

    pdf.ln(40)
    pdf.cell(200, 10, "Smart Buildings Solutions Quotation", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Customer Name: {name}", ln=True)
    pdf.cell(200, 10, f"Phone: {phone}", ln=True)
    pdf.cell(200, 10, f"Email: {email}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, f"Selected Package: {package}", ln=True)
    pdf.cell(200, 10, f"Price: AED {price}", ln=True)

    # Add stamp
    if stamp_b64:
        stamp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        stamp_file.write(base64.b64decode(stamp_b64))
        stamp_file.close()
        pdf.image(stamp_file.name, x=80, y=200, w=50)

    # Save PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        tmp_file_path = tmp_file.name

    with open(tmp_file_path, "rb") as f:
        st.download_button("⬇️ Download Quotation", f, file_name="quotation.pdf", mime="application/pdf")
