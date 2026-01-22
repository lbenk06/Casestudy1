from serializable import Serializable
from database import DatabaseConnector
from datetime import datetime
from typing import Self

class Reservation(Serializable):

    db_connector =  DatabaseConnector().get_table("reservations")

    def __init__(self, user_id: str, device_id: str, start_date: datetime, end_date: datetime, creation_date: datetime = None, last_update: datetime = None, id: str = None) -> None:

        if not id:
            id = F"{user_id}_{device_id}_{start_date}"

        super().__init__(id, creation_date, last_update)
        self.user_id = user_id
        self.device_id = device_id
        self.start_date = start_date
        self.end_date = end_date
        
    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data['user_id'], data['device_id'], data['start_date'], data['end_date'], data['creation_date'], data['last_update'], data['id'])

    def __str__(self):
        return f"Reservation: from {self.user_id} for {self.device_id}: {self.start_date} - {self.end_date}"

if __name__ == "__main__":
    # Create a device
    reservation1 = Reservation("one@mci.edu", "Device1", "2021-01-01 00:00:00", "2021-01-02 00:00:00")
    reservation2 = Reservation("one@mci.edu", "Device2", "2021-01-01 00:00:00", "2021-01-02 00:00:00")
    reservation3 = Reservation("two@mci.edu", "Device2", "2021-01-02 00:00:00", "2021-01-03 00:00:00")


    reservation1.store_data()
    reservation2.store_data()
    reservation3.store_data()

    loaded_reservations = Reservation.find_by_attribute("device_id", "Device2", num_to_return=-1)
    if loaded_reservations:
        for loaded_reservation in loaded_reservations:
            print(f"Loaded: {loaded_reservation}")
    else:
        print("Reservation not found.")