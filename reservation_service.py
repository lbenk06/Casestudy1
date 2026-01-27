from datetime import datetime
from reservations import Reservation
from devices_inheritance import Device
from users_inheritance import User


class ReservationService():

    def __init__(self) -> None:
        self.find_all_reservations()

    @classmethod
    def find_all_reservations(cls) -> list[Reservation]:
        cls.reservations = Reservation.find_all()
        return cls.reservations

    @classmethod
    def find_all_reservations_by_user_id(cls, user_id: str) -> list[Reservation]:
        return [reservation for reservation in cls.reservations if reservation.user_id == user_id]
    
    @classmethod
    def find_all_reservations_by_device_id(cls, device_id: str) -> list[Reservation]:
        return [reservation for reservation in cls.reservations if reservation.device_id == device_id]    
    
    @classmethod
    def find_all_reservations_by_user_id_and_device_id(cls, user_id: str, device_id: str) -> list[Reservation]:
        return [reservation for reservation in cls.reservations if reservation.device_id == device_id and reservation.user_id == user_id]

    @classmethod
    def check_conflict(cls, device_id: str, start_date: datetime, end_date: datetime) -> bool:
        for reservation in cls.reservations:
            if reservation.device_id == device_id:
                if (start_date >= reservation.start_date and start_date <= reservation.end_date) or (end_date >= reservation.start_date and end_date <= reservation.end_date):
                    return True
        return False

    @staticmethod
    def user_exists(user_id: str) -> bool:
        return User.find_by_attribute("id", user_id) is not None

    @staticmethod
    def device_exists(device_id: str) -> bool:
        return Device.find_by_attribute("id", device_id) is not None
    
    @classmethod
    def create_reservation(cls, user_id: str, device_id: str, start_date: str | datetime, end_date: str | datetime) -> bool:
        if not cls.user_exists(user_id):
            raise ValueError("User does not exist")
        
        if not cls.device_exists(device_id):
            raise ValueError("Device does not exist")
        
        # If the dates are provided as strings, convert them to datetime objects
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        jetzt = datetime.now()
        if start_date < jetzt:
            raise ValueError("Das Startdatum darf nicht in der Vergangenheit liegen.") # [cite: 98, 99]

        if end_date <= start_date:
            raise ValueError("Das Enddatum muss nach dem Startdatum liegen.") # [cite: 98, 99]

        # Prüfung auf Konflikte (First-come-first-serve)

        device = Device.find_by_attribute("id", device_id)
        if device and device.status == "maintenance":
            raise ValueError("Das Gerät befindet sich derzeit in Wartung und kann nicht reserviert werden.")
        
        if cls.check_conflict(device_id, start_date, end_date):
            raise ValueError("Reservation conflict detected")
        
        reservation = Reservation(user_id, device_id, start_date, end_date)
        reservation.store_data()
        cls.find_all_reservations()
        return True
    
        
      
    
    
    @classmethod
        
    def clean_expired_reservations(cls):
        res = cls.find_all_reservations()
        now = datetime.now()
        
        for reservation in res:
            val = reservation.end_date
            # Wenn es Text ist -> Umwandeln
            if isinstance(val, str):
                dt_obj = datetime.strptime(val[:19], "%Y-%m-%d %H:%M:%S")
            # Wenn es schon ein datetime-Objekt ist -> direkt nutzen
            elif isinstance(val, datetime):
                dt_obj = val
            else:
                # Fallback für reine date-Objekte
                dt_obj = datetime.combine(val, datetime.min.time())
                
            if dt_obj < now:
                reservation.delete()
        
        cls.find_all_reservations()
