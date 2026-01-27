from typing import Self
from datetime import datetime, timedelta
from serializable import Serializable
from database import DatabaseConnector

class Device(Serializable):
    db_connector = DatabaseConnector().get_table("devices")

    def __init__(self, id: str, name: str, managed_by_user_id: str, maintenance_interval: int, maintenance_cost: float, status: str, end_of_life: datetime = None, creation_date: datetime = None, last_update: datetime = None, next_maintenance: datetime = None):
        super().__init__(id, creation_date, last_update)
        self.name = name
        self.managed_by_user_id = managed_by_user_id
        self.is_active = True
        self.status = status
        self.maintenance_cost = maintenance_cost
        self.maintenance_interval = maintenance_interval
        
        if isinstance(next_maintenance, str):
            self.next_maintenance = datetime.strptime(next_maintenance[:10], "%Y-%m-%d")
        else:
            self.next_maintenance = next_maintenance if next_maintenance else datetime.today()

        if isinstance(end_of_life, str):
            self.end_of_life = datetime.strptime(end_of_life[:10], "%Y-%m-%d")
        else:
            self.end_of_life = end_of_life if end_of_life else datetime.today()

    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        nm = data.get('next_maintenance')
        if isinstance(nm, str):
            nm = datetime.strptime(nm[:10], "%Y-%m-%d")
            
        eol = data.get('end_of_life')
        if isinstance(eol, str):
            eol = datetime.strptime(eol[:10], "%Y-%m-%d")

        return cls(
            id=data['id'],
            name=data.get('name', 'Unbekannt'), 
            managed_by_user_id=data['managed_by_user_id'],
            maintenance_interval=data.get('maintenance_interval', 30),
            maintenance_cost=data.get('maintenance_cost', 0.0),
            status=data.get('status', 'available'),
            end_of_life=eol,
            next_maintenance=nm,
            creation_date=data.get('creation_date'),
            last_update=data.get('last_update')
        )

    def __str__(self) -> str:
        return f"Device: {self.id} ({self.managed_by_user_id}) - Status: {self.status}"

    def set_managed_by_user_id(self, managed_by_user_id: str):
        self.managed_by_user_id = managed_by_user_id

    def set_maintenance(self, is_maintenance: bool):
        self.status = "maintenance" if is_maintenance else "available"
        self.store_data()

    def update_next_maintenance(self):
        if isinstance(self.next_maintenance, str):
            self.next_maintenance = datetime.strptime(self.next_maintenance[:10], "%Y-%m-%d")
            
        if self.next_maintenance and self.maintenance_interval:
            self.next_maintenance = self.next_maintenance + timedelta(days=self.maintenance_interval)
            self.store_data()
    
    def get_maintenance_cost_for_period(self, start_date: datetime, end_date: datetime) -> float:
        m_date = self.next_maintenance
        if isinstance(m_date, str):
            m_date = datetime.strptime(m_date[:10], "%Y-%m-%d")
        
        if m_date and start_date <= m_date <= end_date:
            return float(self.maintenance_cost)
        return 0.0