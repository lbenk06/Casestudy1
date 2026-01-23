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
            if u_id and u_name:
                new_user = User(u_id, u_name)
                new_user.store_data()
                st.success(f"Nutzer {u_name} angelegt!")
                st.rerun()
            else:
                st.error("Bitte beide Felder  ausfüllen.")

    st.divider()

    #Liste mit allen Nutzern drunter
    st.subheader("Alle Nutzer:")
    all_users = User.find_all()

    if all_users:
        cols=st.columns([2,2,1])
        cols[0].write("**Name**")
        cols[1].write("**E-Mail (ID)**")
        cols[2].write("**Aktion**")

        for u in all_users:
            c1, c2, c3=st.columns([2,2,1])
            c1.write(u.name)
            c2.write(u.id)
            
            if c3.button("Löschen", key=f"delete_{u.id}"):
                assigned_devices=Device.find_by_attribute("managed_by_user_id", u.id, num_to_return=-1)

                if assigned_devices:
                    st.error(f"Nutzer {u.name} kann nicht gelöscht werden, da er/sie für Geräte verantwortlich ist.")
                else:
                    u.delete()
                    st.success(f"Nutzer {u.name} gelöscht!")
                    st.rerun()
    else:
        st.info("Noch keine Nutzer angelegt.")

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

    st.divider()
    # Liste mit allen Geräten drunter
    st.subheader("Alle Geräte:")
    all_devices = Device.find_all()
    if all_devices:
        cols=st.columns([2,2,2,1])
        cols[0].write("**Name**")
        cols[1].write("**Inventarnummer (ID)**")
        cols[2].write("**Verantwortliche Person**")
        cols[3].write("**Aktion**")

        for d in all_devices:
            c1, c2, c3, c4=st.columns([2,2,2,1])
            c1.write(d.name)
            c2.write(d.id)
            c3.write(d.managed_by_user_id)
            
            if c4.button("Löschen", key=f"delete_{d.id}"):
                d.delete()
                st.success(f"Gerät {d.name} gelöscht!")
                st.rerun()
    else:
        st.info("Noch keine Geräte angelegt.")



#3. reservierungssystem
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