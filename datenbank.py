from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import os

# Ordner sicherstellen
os.makedirs("db", exist_ok=True)

users_db = TinyDB("db/users.json")
devices_db = TinyDB("db/devices.json")
reservations_db = TinyDB("db/reservations.json")

User = Query()
Device = Query()
Reservation = Query()

# ---------------- User ----------------
def create_user(name):
    if not name or users_db.get(User.name == name):
        return False
    users_db.insert({"name": name})
    return True

def delete_user(name):
    # Benutzer entfernen
    users_db.remove(User.name == name)
    # Alle Reservierungen dieses Users löschen und Geräte freigeben
    for res in reservations_db.search(Reservation.user == name):
        release_device(res["device_id"])


def get_users():
    return users_db.all()

# ---------------- Geräte ----------------
def create_device(name, device_type):
    if not name:
        return
    devices_db.insert({
        "name": name,
        "type": device_type,
        "status": "verfügbar",
        "current_user": None
    })

def delete_device(device_id):
    # Gerät aus devices_db löschen
    devices_db.remove(doc_ids=[device_id])
    # Alle Reservierungen für das Gerät löschen
    reservations_db.remove(Reservation.device_id == device_id)



def get_devices():
    # Vorher abgelaufene Reservierungen prüfen
    check_expired_reservations()
    return devices_db.all()

def set_device_status(device_id, status):
    devices_db.update({"status": status, "current_user": None}, doc_ids=[device_id])

# ---------------- Reservierungen ----------------
def reserve_device(device_id, user_name, duration_minutes):
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration_minutes)

    devices_db.update(
        {"status": "reserviert", "current_user": user_name},
        doc_ids=[device_id]
    )

    reservations_db.insert({
        "device_id": device_id,
        "user": user_name,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S")
    })

def release_device(device_id):
    devices_db.update({"status": "verfügbar", "current_user": None}, doc_ids=[device_id])
    reservations_db.remove(Reservation.device_id == device_id)

def check_expired_reservations():
    now = datetime.now()
    for res in reservations_db.all():
        end_time = datetime.strptime(res["end_time"], "%Y-%m-%d %H:%M:%S")
        if now >= end_time:
            # Gerät freigeben
            release_device(res["device_id"])
