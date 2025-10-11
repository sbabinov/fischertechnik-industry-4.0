import os
from dataclasses import dataclass

@dataclass
class Config:
    storage_ip: str
    crane_ip: str
    sort_center_ip: str
    shipment_center_ip: str
    paint_center_ip: str

    @classmethod
    def from_env(cls):
        return cls(
            storage_ip=os.getenv('STORAGE_IP', '192.168.1.10'),
            crane_ip=os.getenv('CRANE_IP', '192.168.1.11'),
            sort_center_ip=os.getenv('SORT_CENTER_IP', '192.168.1.12'),
            shipment_center_ip=os.getenv('SHIPMENT_CENTER_IP', '192.168.1.13'),
            paint_center_ip=os.getenv('PAINT_CENTER_IP', '192.168.1.14')
        )
