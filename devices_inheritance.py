from typing import Self
from datetime import datetime, timedelta

from serializable import Serializable
from database import DatabaseConnector

class Device(Serializable):

    db_connector =  DatabaseConnector().get_table("devices")

    def __init__(self, id: str, name: str, managed_by_user_id: str, maintenance_interval: int, maintenance_cost: float, status:str, end_of_life: datetime = None, creation_date: datetime = None, last_update: datetime = None, next_maintenance: datetime =None):
        super().__init__(id, creation_date, last_update)
        # The user id of the user that manages the device
        # We don't store the user object itself, but only the id (as a key)
        self.name=name
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True
        self.status=status
        self.end_of_life = end_of_life if end_of_life else datetime.today().date()
        self.maintenance_cost=maintenance_cost
        self.maintenance_interval=maintenance_interval
        self.next_maintenance=next_maintenance
   
    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(
            id=data['id'],
            name=data.get('name', 'Unbekannt'), 
            managed_by_user_id=data['managed_by_user_id'],
            maintenance_interval=data.get('maintenance_interval', 30),
            maintenance_cost=data.get('maintenance_cost', 0.0),
            status=data.get('status', 'available'),
            end_of_life=data.get('end_of_life'),
            first_maintenance=data.get('first_maintenance'),
            next_maintenance=data.get('next_maintenance'),
            creation_date=data.get('creation_date'),
            last_update=data.get('last_update')
        )

    def __str__(self) -> str:
        return f"Device: {self.id} ({self.managed_by_user_id}) - Active: {self.is_active} - Created: {self.creation_date} - Last Update: {self.last_update}"

    def set_managed_by_user_id(self, managed_by_user_id: str):
        """Expects `managed_by_user_id` to be a valid user id that exists in the database."""
        self.managed_by_user_id = managed_by_user_id

    def set_maintenance(self, is_maintenance: bool):
        self.status="maintenance" if is_maintenance else "available"
        self.store_data()

    def update_next_maintenance(self):
        if self.next_maintenance and self.maintenance_interval:
            self.next_maintenance = self.next_maintenance + timedelta(days=self.maintenance_interval)
            self.store_data()
    
    def get_maintenance_cost_for_period(self, start_date: datetime, end_date: datetime) -> float:
        if start_date <= self.next_maintenance <= end_date:
            return self.maintenance_cost
        return 0.0