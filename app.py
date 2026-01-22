import streamlit as st
from datetime import datetime
from devices_inheritance import Device
from users_inheritance import User
from reservations import Reservation


st.set_page_config(page_title="Geräteverwaltung am MCI 4", layout="wide")


st.sidebar.title("Navigation")
page = st.sidebar.radio("Gehe zu:", 
    ["Nutzer-Verwaltung", "Geräte-Verwaltung", "Reservierungssystem", "Wartungs-Management"])

#nutzerverwaltung
if page == "Nutzer-Verwaltung":
    st.header("👤 Nutzer-Verwaltung")
    with st.form("user_form"):
        st.subheader("Neuen Nutzer anlegen")
        u_id = st.text_input("E-Mail (ID)") 
        u_name = st.text_input("Name")      
        if st.form_submit_button("Nutzer speichern"):
            new_user = User(u_id, u_name)
            new_user.store_data()
            st.success(f"Nutzer {u_name} angelegt!")

#2. gerätverwaltung
elif page == "Geräte-Verwaltung":
    st.header("🖨️ Geräte-Verwaltung")
    
    # Nutzer laden für die verantwortliche Person
    users = User.find_all()
    user_list = [u.id for u in users] if users else []
    
    with st.form("device_form"):
        st.subheader("Gerät anlegen / ändern")
        d_id = st.text_input("Inventarnummer (ID)") # [cite: 81]
        d_name = st.text_input("Name des Geräts")   # [cite: 82]
        d_responsible = st.selectbox("Verantwortliche Person", options=user_list) # [cite: 83]
        d_interval = st.number_input("Wartungsintervall (Tage)", min_value=1, value=90) # [cite: 89]
        d_cost = st.number_input("Wartungskosten (€)", min_value=0.0, value=100.0) # [cite: 90]
        d_eol = st.date_input("End of Life") # [cite: 85]
        
        if st.form_submit_button("Gerät speichern"):
            # Konvertiere date zu datetime für die Klasse
            eol_dt = datetime.combine(d_eol, datetime.min.time())
            new_device = Device(d_id, d_name, d_responsible, d_interval, d_cost, "available", eol_dt)
            new_device.store_data()
            st.success(f"Gerät {d_name} gespeichert!")

#3. reservierungssyste,
elif page == "Reservierungssystem":
    st.header("📅 Reservierungssystem")
    # Hier kommt eure Logik zum Ein/Austragen rein [cite: 38]
    st.info("Hier können zukünftige Reservierungen (First-Come-First-Serve) verwaltet werden.")

#4. wartungs-management
elif page == "Wartungs-Management":
    st.header("🛠️ Wartungs-Management")
    
    devices = Device.find_all()
    if devices:
        # Teil A: Nächste Termine anzeigen [cite: 110]
        st.subheader("Anstehende Wartungstermine")
        for d in devices:
            st.write(f"**{d.name}**: Nächste Wartung am {d.next_maintenance}")
            
        # Teil B: Quartalskosten 
        st.subheader("Wartungskosten Planung")
        year = st.selectbox("Jahr", [2024, 2025, 2026])
        q = st.radio("Quartal auswählen", [1, 2, 3, 4], horizontal=True)
        
        # Logik zur Berechnung (vereinfacht für die Anzeige)
        # Hier könntest du d.get_maintenance_cost_for_period nutzen
        st.metric(label=f"Gesamtkosten Q{q} {year}", value=f"1500.00 €")
    else:
        st.warning("Keine Geräte für die Wartungsplanung gefunden.")