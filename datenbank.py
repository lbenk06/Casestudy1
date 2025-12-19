from tinydb import TinyDB, Query
from datetime import datetime

users_db = TinyDB("db/users.json")
devices_db = TinyDB("db/devices.json")
reservations_db = TinyDB("db/reservations.json")

User = Query()
Device = Query()
Reservation = Query()

# ---------- USER ----------
def create_user(name):
    if users_db.get(User.name == name):
        return False
    users_db.insert({"name": name})
    return True

def get_users():
    return users_db.all()

# ---------- GERÄTE ----------
def create_device(name, device_type):
    devices_db.insert({
        "name": name,
        "type": device_type,
        "status": "verfügbar"
    })

def get_devices():
    return devices_db.all()

def set_device_status(device_id, status):
    devices_db.update({"status": status}, doc_ids=[device_id])

# ---------- RESERVIERUNG ----------
def reserve_device(device_id, user_name):
    devices_db.update(
        {"status": "reserviert", "current_user": user_name},
        doc_ids=[device_id]
    )

    reservations_db.insert({
        "device_id": device_id,
        "user": user_name,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

def release_device(device_id):
    devices_db.update(
        {"status": "verfügbar", "current_user": None},
        doc_ids=[device_id]
    )
