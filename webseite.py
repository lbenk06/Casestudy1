import streamlit as st

# --- Beispiel-Benutzer (später durch DB ersetzen) ---
users = {
    "user1": {"password": "1234", "role": "user"},
    "admin": {"password": "admin", "role": "admin"},
}

# --- Beispiel-Geräte ---
if "devices" not in st.session_state:
    st.session_state.devices = [
        {"name": "Laptop 1", "status": "verfügbar"},
        {"name": "Beamer", "status": "verfügbar"},
        {"name": "Tablet A", "status": "reserviert"},
    ]

# --- Session-State Initialisierung ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

# --- Login-Seite ---
def login_page():
    st.title("Gerätemanagement - Login")

    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.session_state.role = users[username]["role"]
        else:
            st.error("Falscher Benutzername oder Passwort")

# --- User-Seite: Geräte reservieren ---
def user_page():
    st.title("Geräteübersicht")

    for i, device in enumerate(st.session_state.devices):
        col1, col2, col3 = st.columns([3, 2, 2])
        col1.write(device["name"])
        col2.write(device["status"])

        if device["status"] == "verfügbar":
            if col3.button("Reservieren", key=f"reserve_{i}"):
                st.session_state.devices[i]["status"] = "reserviert"
                st.success(f"{device['name']} reserviert!")

# --- Admin-Seite: Geräte außer Betrieb setzen ---
def admin_page():
    st.title("Admin - Geräteverwaltung")

    for i, device in enumerate(st.session_state.devices):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        col1.write(device["name"])
        col2.write(device["status"])

        # außer Betrieb setzen
        if col3.button("Außer Betrieb", key=f"disable_{i}"):
            st.session_state.devices[i]["status"] = "außer Betrieb"

        # wieder aktivieren
        if device["status"] == "außer Betrieb":
            if col4.button("Reaktivieren", key=f"enable_{i}"):
                st.session_state.devices[i]["status"] = "verfügbar"

# --- Hauptlogik ---
if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.write(f"Angemeldet als: **{st.session_state.user}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.role = None

    if st.session_state.role == "admin":
        admin_page()
    else:
        user_page()
