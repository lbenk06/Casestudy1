import streamlit as st
from datenbank import *

st.title("Gerätenetzwerk – Admin")

# ---------------- USER ----------------
st.header("Benutzerverwaltung")

with st.form("add_user"):
    user_name = st.text_input("Benutzername")
    add_user = st.form_submit_button("Benutzer anlegen")

if add_user:
    if create_user(user_name):
        st.success("Benutzer angelegt")
    else:
        st.error("Benutzer existiert bereits")

# ---------------- GERÄTE ----------------
st.header("Geräte anlegen")

device_name = st.text_input("Gerätename")
device_type = st.selectbox("Gerätetyp", ["3D-Drucker", "Drucker", "Lasercutter"])

if st.button("Gerät hinzufügen"):
    create_device(device_name, device_type)
    st.success("Gerät hinzugefügt")

# ---------------- GERÄTEÜBERSICHT ----------------
st.header("Geräteübersicht")

users = [u["name"] for u in get_users()]

for device in get_devices():
    col1, col2, col3, col4 = st.columns([3, 2, 3, 2])

    col1.write(f"{device['name']} ({device['type']})")
    col2.write(device["status"])

    # Wartung
    if col3.button("Wartung", key=f"maint_{device.doc_id}"):
        set_device_status(device.doc_id, "Wartung")

    # Reservierung
    if device["status"] == "verfügbar" and users:
        user = col4.selectbox(
            "User",
            users,
            key=f"user_{device.doc_id}"
        )
        if col4.button("Reservieren", key=f"res_{device.doc_id}"):
            reserve_device(device.doc_id, user)

    # Freigeben
    if device["status"] == "reserviert":
        if col4.button("Freigeben", key=f"free_{device.doc_id}"):
            release_device(device.doc_id)
