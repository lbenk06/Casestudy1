import streamlit as st
from datenbank import *
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Seite alle 10 Sekunden automatisch neu laden
st_autorefresh(interval=10 * 1000, key="auto_refresh")

st.set_page_config(page_title="Gerätenetzwerk – Admin", layout="wide")
st.title("Gerätenetzwerk – Admin")

# ---------------- Benutzerverwaltung ----------------
st.header("👤 Benutzerverwaltung")

# Benutzer anlegen
with st.form("add_user"):
    new_user_name = st.text_input("Benutzername")
    add_user_btn = st.form_submit_button("Benutzer anlegen")

if add_user_btn:
    if create_user(new_user_name):
        st.success(f"Benutzer '{new_user_name}' angelegt")
    else:
        st.error("Benutzer existiert bereits oder Name leer")

# Benutzerliste mit Löschen
st.subheader("Benutzerliste")
users = get_users()
for user in users:
    col1, col2 = st.columns([3, 1])
    col1.write(user["name"])
    if col2.button("Löschen", key=f"del_user_{user['name']}"):
        delete_user(user["name"])
        st.success(f"Benutzer '{user['name']}' gelöscht")

# ---------------- Geräteverwaltung ----------------
st.header("🖨️ Geräteverwaltung")

# Gerät anlegen
st.subheader("Gerät hinzufügen")
device_name = st.text_input("Gerätename", key="new_device_name")
device_type = st.selectbox("Gerätetyp", ["3D-Drucker", "Drucker", "Lasercutter"], key="new_device_type")
if st.button("Gerät hinzufügen"):
    create_device(device_name, device_type)
    st.success(f"Gerät '{device_name}' hinzugefügt")

# Geräteliste mit Aktionen und Timer
st.subheader("Geräteliste")
devices = get_devices()
users_list = [u["name"] for u in get_users()]

for device in devices:
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 2, 2, 2, 3])
    
    # Statusfarbe
    if device["status"] == "verfügbar":
        status_display = "🟢 verfügbar"
    elif device["status"] == "reserviert":
        status_display = "🟡 reserviert"
    elif device["status"] == "Wartung":
        status_display = "🔴 Wartung"
    else:
        status_display = device["status"]

    col1.write(f"{device['name']} ({device['type']})")
    col2.write(status_display)

    # Aktueller User und Restzeit
    current_user = device.get("current_user", "-")
    if device["status"] == "reserviert" and current_user != "-":
        res = reservations_db.get(Reservation.device_id == device.doc_id)
        if res:
            end_time = datetime.strptime(res["end_time"], "%Y-%m-%d %H:%M:%S")
            remaining = end_time - datetime.now()
            if remaining.total_seconds() < 0:
                remaining_str = "abgelaufen"
            else:
                minutes = remaining.seconds // 60
                remaining_str = f"{minutes} Min übrig"
            col3.write(f"{current_user} (bis {end_time.strftime('%H:%M %d.%m')}, {remaining_str})")
        else:
            col3.write(current_user)
    else:
        col3.write(current_user)

    # Wartung
    if col4.button("Wartung", key=f"maint_{device.doc_id}"):
        set_device_status(device.doc_id, "Wartung")

    # Reservieren
    if device["status"] == "verfügbar" and users_list:
        user = col5.selectbox("User", users_list, key=f"user_{device.doc_id}")
        duration = col5.number_input("Dauer (Minuten)", min_value=1, value=60, key=f"dur_{device.doc_id}")
        if col5.button("Reservieren", key=f"res_{device.doc_id}"):
            reserve_device(device.doc_id, user, duration)

    # Manuelles Freigeben
    if device["status"] == "reserviert":
        if col5.button("Freigeben", key=f"free_{device.doc_id}"):
            release_device(device.doc_id)

    # Gerät löschen
    if col6.button("Löschen", key=f"del_device_{device.doc_id}"):
        delete_device(device.doc_id)
        st.success(f"Gerät '{device['name']}' gelöscht")
