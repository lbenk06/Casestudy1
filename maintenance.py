from serializable import Serializable
from database import DatabaseConnector
from datetime import datetime
from typing import Self

class Maintenance(Serializable):

    db_connector=DatabaseConnector().get_table("maintenances")

    def __init__(self, device_id: str, description: str, maintenance_date: datetime= None, id: str=None, creation_date: datetime=None, last_update: datetime=None)->None:
        
        
        if not id:
            id = f"maint_{device_id}_{datetime.now().timestamp()}"

        super().__init__(id, creation_date, last_update)
        self.device_id=device_id
        self.description=description
        self.maintenance_date=maintenance_date if maintenance_date else datetime.now()
    
    @classmethod
    def instantiate_from_dict(cls, data: dict)->Self:
        return cls(data['device_id'], data['description'], data['maintenance_date'], data['id'], data['creation_date'], data['last_update'])
    
    def __str__(self):
        return f"Wartung für Gerät: {self.device_id} am {self.maintenance_date} - Beschreibung: {self.description}"
    
if __name__ == "__main__":
    # Create a maintenance record
    maintenance1 = Maintenance("Device1", "Routine check")
    maintenance2 = Maintenance("Device2", "Battery replacement")
    maintenance3 = Maintenance("Device3", "Screen repair")

    maintenance1.store_data()
    maintenance2.store_data()
    maintenance3.store_data()

    loaded_maintenance = Maintenance.find_by_attribute("device_id", "Device1", num_to_return=-1)
    if loaded_maintenance:
        for maintenance in loaded_maintenance:
            print(f"Loaded: {maintenance}")
    else:
        print("Maintenance record not found.")