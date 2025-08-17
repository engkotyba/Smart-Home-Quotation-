import streamlit as st
from datetime import datetime
from fpdf import FPDF
import tempfile
import os
from collections import Counter
import base64

# --- Helper to load images as base64 ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Load images
logo_b64 = get_base64_image("static/logo.png")
whatsapp_icon_b64 = get_base64_image("static/whatsapp.png")
stamp_b64 = get_base64_image("static/stamp_signature.png")
smarthome_b64 = get_base64_image("static/smarthome.png")

# --- Inject CSS ---
st.markdown(f"""
<style>
    /* Remove Streamlit header, footer, and menu */
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Button styling to fill container width */
    div.stButton > button {{
        width: 100%;
    }}

    /* Center content */
    .main .block-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 700px;
        margin: auto;
        padding-top: 30px;
    }}

    /* Mobile optimization */
    @media (max-width: 768px) {{
        .main .block-container {{
            max-width: 95% !important;
            padding-left: 10px;
            padding-right: 10px;
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
        border-radius: 50px;
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


# --- Helper Functions ---
def generate_pdf(name, mobile, email, date, system_type, all_selected, total, wifi_options):
    pdf = FPDF()
    pdf.add_page()

    # Add logo if exists
    if logo_b64:
        logo_path = os.path.join(tempfile.gettempdir(), "logo.png")
        with open(logo_path, "wb") as f:
            f.write(base64.b64decode(logo_b64))
        logo_width_pdf = 50
        x_centered = (pdf.w - logo_width_pdf) / 2
        pdf.image(logo_path, x=x_centered, y=8, w=logo_width_pdf)

    pdf.ln(20)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Smart Buildings Solutions Quotation", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, f"Customer Name: {name}", ln=0)
    pdf.cell(0, 10, f"Date: {date}", ln=1)
    pdf.cell(100, 10, f"Mobile: {mobile}", ln=0)
    pdf.cell(0, 10, f"Email: {email}", ln=1)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"System Type: {system_type}", ln=1)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Room Breakdown", ln=1)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.w - 10, pdf.get_y())
    pdf.ln(5)

    for room, features_list, cost in all_selected:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"{room}", ln=1)
        pdf.set_font("Arial", '', 12)

        feature_counts = Counter(features_list)
        for feat, count in feature_counts.items():
            display_text = f"- {feat}"
            if count > 1:
                display_text += f" x{count}"
            display_text += f": {wifi_options.get(feat, 0) * count} AED"
            pdf.cell(0, 10, display_text, ln=1)
        pdf.cell(0, 10, f"Subtotal: {cost} AED", ln=1)
        pdf.ln(2)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Total Estimated Cost: {total} AED", ln=1)
    pdf.ln(10)

    # Stamp image
    if stamp_b64:
        stamp_path = os.path.join(tempfile.gettempdir(), "stamp_signature.png")
        with open(stamp_path, "wb") as f:
            f.write(base64.b64decode(stamp_b64))
        pdf.image(stamp_path, x=150, y=pdf.get_y(), w=40)

    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, "quotation.pdf")
    pdf.output(pdf_path)
    with open(pdf_path, "rb") as file:
        st.download_button(
            label="📥 Download Quotation PDF",
            data=file,
            file_name="quotation.pdf",
            mime="application/pdf"
        )


def generate_quotation(name, mobile, email, date, system_type, all_selected, total, wifi_options):
    st.success("Quotation generated below.")
    st.markdown("---")
    with st.container(border=True):
        st.markdown("## 📄 Quotation Details")
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Customer Name:** {name}")
        with col2:
            st.markdown(f"**Mobile:** {mobile}")
            st.markdown(f"**Email:** {email}")
    st.markdown("---")
    st.markdown(f"### 💡 **System Type:** {system_type}")
    st.markdown("---")
    st.markdown("### 📋 **Room Breakdown**")
    for room, features_list, cost in all_selected:
        st.markdown(f"**{room}**")
        if features_list:
            feature_counts = Counter(features_list)
            for feat, count in feature_counts.items():
                display_text = f"- {feat}"
                if count > 1:
                    display_text += f" x{count}"
                display_text += f": {wifi_options.get(feat, 0) * count} AED"
                st.markdown(display_text)
        else:
            st.markdown("- No features selected.")
        st.markdown(f"**Subtotal:** {cost} AED")
        st.markdown("---")
    st.markdown(f"### 💰 **Total Estimated Cost:** {total} AED")
    if stamp_b64:
        st.image("static/stamp_signature.png", width=200)
    generate_pdf(name, mobile, email, date, system_type, all_selected, total, wifi_options)


# --- Main App Logic ---
if logo_b64:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("static/logo.png", width=300)
st.markdown("---")

st.markdown("<h1 style='text-align: center; color: #2C3E50; font-family: sans-serif;'>🏡 Smart Buildings Solutions Quotation</h1>", unsafe_allow_html=True)
st.markdown("---")

if smarthome_b64 and ('package_selected' not in st.session_state or st.session_state.package_selected is None):
    st.image("static/smarthome.png", use_container_width=True)

# Initialize session state
if 'package_selected' not in st.session_state:
    st.session_state.package_selected = None
if 'system_type' not in st.session_state:
    st.session_state.system_type = "WiFi Smart Home"

# --- Customer Info ---
st.subheader("👤 Customer Information")
name = st.text_input("Name", "")
col_mobile, col_email = st.columns(2)
with col_mobile:
    mobile = st.text_input("Mobile", "")
with col_email:
    email = st.text_input("Email", "")
date = datetime.now().strftime("%B %d, %Y")

# --- System Type ---
st.subheader("💡 Select System Type")
col_wifi, col_wired = st.columns(2)
with col_wifi:
    if st.button("WiFi Smart Home"):
        st.session_state.system_type = "WiFi Smart Home"
with col_wired:
    if st.button("Wired Smart Home"):
        st.session_state.system_type = "Wired Smart Home"

system_type = st.session_state.system_type

if system_type == "WiFi Smart Home":
    # Package selection
    st.subheader("🎁 Choose a Smart Home Package or Configure Manually")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🛏️ One Bedroom Package"):
            st.session_state.package_selected = "one_bedroom"
    with col2:
        if st.button("🏡 Two Bedroom Package"):
            st.session_state.package_selected = "two_bedroom"
    with col3:
        if st.button("🏘️ Three Bedroom Package"):
            st.session_state.package_selected = "three_bedroom"
    with col4:
        if st.button("🔧 Custom Configuration"):
            st.session_state.package_selected = "manual"

    if st.session_state.package_selected:
        st.button("↩️ Reset", on_click=lambda: st.session_state.update(package_selected=None))

    wifi_options = {
        "Wifi Thermostat": 500,
        "Wifi Lights Switch": 300,
        "Wifi Lights Dimmer": 300,
        "Wifi Curtain Switch": 350,
        "Wifi Video Intercom": 600,
        "Wifi Smart Door lock": 540,
        "Wifi Camera": 350,
        "Wifi Power Socket": 250,
        "Alexa": 600,
        "Wifi WaterHeater": 500,
    }

    if st.session_state.package_selected == "one_bedroom":
        one_bedroom_features = [
            "Wifi Thermostat",
            "Wifi Lights Switch", "Wifi Lights Switch", "Wifi Lights Switch",
            "Wifi WaterHeater",
            "Wifi Smart Door lock"
        ]
        total = sum([wifi_options.get(feature, 0) for feature in one_bedroom_features])
        all_selected = [("One Bedroom Package", one_bedroom_features, total)]
        generate_quotation(name, mobile, email, date, system_type, all_selected, total, wifi_options)

    elif st.session_state.package_selected == "two_bedroom":
        two_bedroom_features = [
            "Wifi Thermostat", "Wifi Thermostat",
            "Wifi Lights Switch", "Wifi Lights Switch", "Wifi Lights Switch", "Wifi Lights Switch", "Wifi Lights Switch",
            "Wifi WaterHeater", "Wifi WaterHeater",
            "Wifi Smart Door lock"
        ]
        total = sum([wifi_options.get(feature, 0) for feature in two_bedroom_features])
        all_selected = [("Two Bedroom Package", two_bedroom_features, total)]
        generate_quotation(name, mobile, email, date, system_type, all_selected, total, wifi_options)

    elif st.session_state.package_selected == "three_bedroom":
        three_bedroom_features = [
            "Wifi Thermostat", "Wifi Thermostat", "Wifi Thermostat",
            "Wifi Lights Switch", "Wifi Lights Switch", "Wifi Lights Switch",
            "Wifi Lights Switch", "Wifi Lights Switch", "Wifi Lights Switch", "Wifi Lights Switch",
            "Wifi WaterHeater", "Wifi WaterHeater", "Wifi WaterHeater",
            "Wifi Smart Door lock"
        ]
        total = sum([wifi_options.get(feature, 0) for feature in three_bedroom_features])
        all_selected = [("Three Bedroom Package", three_bedroom_features, total)]
        generate_quotation(name, mobile, email, date, system_type, all_selected, total, wifi_options)

    elif st.session_state.package_selected == "manual":
        num_rooms = st.number_input("How many rooms?", min_value=1, max_value=20, value=1, key='num_rooms')
        all_selected = []
        for i in range(num_rooms):
            st.markdown(f"### 🛏️ Room {i + 1}")
            selected = st.multiselect(f"Select features for Room {i+1}", wifi_options.keys(), key=f"room_{i}")
            cost = sum([wifi_options.get(feature, 0) for feature in selected])
            all_selected.append((f"Room {i+1}", selected, cost))
        total = sum(item[2] for item in all_selected)
        if st.button("🧾 Generate Quotation"):
            generate_quotation(name, mobile, email, date, system_type, all_selected, total, wifi_options)

else:
    st.info("📞 Please contact us at info@ketechs.com or 0566184681 for Wired Smart Home quotations.")
