import streamlit as st
from datetime import datetime
from fpdf import FPDF
import tempfile
import os
from collections import Counter

# --- Helper Functions (Moved to the top) ---
def generate_pdf(name, mobile, email, date, system_type, all_selected, total, wifi_options):
    pdf = FPDF()
    pdf.add_page()
    pdf.image("static/logo.png", x=10, y=8, w=50)
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
            display_text += f": {wifi_options[feat] * count} AED"
            pdf.cell(0, 10, display_text, ln=1)
        pdf.cell(0, 10, f"Subtotal: {cost} AED", ln=1)
        pdf.ln(2)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Total Estimated Cost: {total} AED", ln=1)
    pdf.ln(10)
    if os.path.exists("static/stamp_signature.png"):
        pdf.image("static/stamp_signature.png", x=150, y=pdf.get_y(), w=40)
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
            st.markdown(f"**Mobile:** {mobile}")
        with col2:
            st.markdown(f"**Date:** {date}")
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
                    display_text += f": {wifi_options[feat] * count} AED"
                    st.markdown(display_text)
            else:
                st.markdown("- No features selected.")
            st.markdown(f"**Subtotal:** {cost} AED")
            st.markdown("---")
        st.markdown(f"### 💰 **Total Estimated Cost:** {total} AED")
    st.image("static/stamp_signature.png", width=200)
    generate_pdf(name, mobile, email, date, system_type, all_selected, total, wifi_options)

# --- Main App Logic ---
st.image("static/logo.png", width=300)
st.markdown("---")
st.title("🏡 Smart Buildings Solutions Quotation")

# Initialize session state for the package selection
if 'package_selected' not in st.session_state:
    st.session_state.package_selected = None

# --- Customer Info ---
st.subheader("👤 Customer Information")
name = st.text_input("Name", "")
mobile = st.text_input("Mobile", "")
email = st.text_input("Email", "")
date = datetime.now().strftime("%B %d, %Y")

# --- System Type ---
st.subheader("💡 Select System Type")
system_type = st.radio("Choose a system:", ["WiFi Smart Home", "Wired Smart Home"])

if system_type == "WiFi Smart Home":
    # --- Package Selection Buttons ---
    st.subheader("🎁 Choose a Smart Home Package")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛏️ One Bedroom Package"):
            st.session_state.package_selected = "one_bedroom"
    with col2:
        if st.button("🏡 Two Bedroom Package"):
            st.session_state.package_selected = "two_bedroom"
    with col3:
        if st.button("🏠 Three Bedroom Package"):
            st.session_state.package_selected = "three_bedroom"

    if st.session_state.package_selected:
        st.button("↩️ Reset to Manual Selection", on_click=lambda: st.session_state.update(package_selected=None))

    # Define the core wifi options
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
        " Wifi WaterHeater": 600,
    }

    if st.session_state.package_selected == "one_bedroom":
        st.subheader("📦 One Bedroom Package Configuration")
        one_bedroom_features = [
            "Wifi Thermostat",
            "Wifi Lights Switch",
            "Wifi Lights Switch",
            "Wifi Curtain Switch",
            "Wifi Smart Door lock",
            "Alexa"
        ]
        total = sum([wifi_options[feature] for feature in one_bedroom_features])
        all_selected = [("Room 1", one_bedroom_features, total)]
        generate_quotation(name, mobile, email, date, system_type, all_selected, total, wifi_options)

    elif st.session_state.package_selected == "two_bedroom":
        st.subheader("📦 Two Bedroom Package Configuration")
        two_bedroom_features = [
            "Wifi Thermostat",
            "Wifi Lights Switch",
            "Wifi Lights Switch",
            "Wifi Lights Switch", # Two bedrooms, let's assume 3 switches
            "Wifi Curtain Switch",
            "Wifi Smart Door lock",
            "Wifi Camera",
            "Alexa"
        ]
        total = sum([wifi_options[feature] for feature in two_bedroom_features])
        all_selected = [("Main Bedroom", ["Wifi Thermostat", "Wifi Lights Switch", "Wifi Curtain Switch", "Wifi Smart Door lock"], 500+300+350+540), 
                        ("Second Bedroom", ["Wifi Lights Switch", "Wifi Lights Switch"], 300+300),
                        ("Living Room", ["Wifi Camera", "Alexa"], 350+600)
        ]
        generate_quotation(name, mobile, email, date, system_type, all_selected, total, wifi_options)

    elif st.session_state.package_selected == "three_bedroom":
        st.subheader("📦 Three Bedroom Package Configuration")
        three_bedroom_features = [
            "Wifi Thermostat",
            "Wifi Lights Switch",
            "Wifi Lights Switch",
            "Wifi Lights Switch",
            "Wifi Lights Switch", # Three bedrooms, let's assume 4 switches
            "Wifi Curtain Switch",
            "Wifi Curtain Switch",
            "Wifi Smart Door lock",
            "Wifi Smart Door lock",
            "Wifi Camera",
            "Wifi Video Intercom",
            "Alexa"
        ]
        total = sum([wifi_options[feature] for feature in three_bedroom_features])
        all_selected = [("Main Bedroom", ["Wifi Thermostat", "Wifi Lights Switch", "Wifi Curtain Switch", "Wifi Smart Door lock", "Alexa"], 500+300+350+540+600),
                        ("Second Bedroom", ["Wifi Lights Switch", "Wifi Lights Switch"], 300+300),
                        ("Third Bedroom", ["Wifi Lights Switch", "Wifi Curtain Switch"], 300+350),
                        ("Living Room", ["Wifi Video Intercom", "Wifi Camera"], 600+350)
        ]
        generate_quotation(name, mobile, email, date, system_type, all_selected, total, wifi_options)

    else: # Manual selection
        st.subheader("📦 Room Configuration (Manual)")
        num_rooms = st.number_input("How many rooms?", min_value=1, max_value=20, value=1, key='num_rooms')
        
        all_selected = []
        for i in range(num_rooms):
            st.markdown(f"### 🛏️ Room {i + 1}")
            selected = st.multiselect(f"Select features for Room {i+1}", wifi_options.keys(), key=f"room_{i}")
            cost = sum([wifi_options[feature] for feature in selected])
            all_selected.append((f"Room {i+1}", selected, cost))
        
        total = sum(item[2] for item in all_selected)
        
        if st.button("🧾 Generate Quotation"):
            generate_quotation(name, mobile, email, date, system_type, all_selected, total, wifi_options)

else:
    st.info("📞 Please contact us at info@ketechs.com or 0566184681 for Wired Smart Home quotations.")
