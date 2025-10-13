import os
from dataclasses import dataclass

@dataclass
class Config:
    factory_mode: str
    server_host: str
    server_port: str
    storage_ip: str
    crane_ip: str
    sort_center_ip: str
    shipment_center_ip: str
    paint_center_ip: str

    @classmethod
    def from_env(cls):
        return cls(
            factory_mode=os.getenv('FACTORY_MODE', 'mock'),
            server_host=os.getenv('SERVER_HOST', '127.0.0.1'),
            server_port=os.getenv('SERVER_PORT', '8080'),
            storage_ip=os.getenv('STORAGE_IP', '192.168.1.10'),
            crane_ip=os.getenv('CRANE_IP', '192.168.1.11'),
            sort_center_ip=os.getenv('SORT_CENTER_IP', '192.168.1.12'),
            shipment_center_ip=os.getenv('SHIPMENT_CENTER_IP', '192.168.1.13'),
            paint_center_ip=os.getenv('PAINT_CENTER_IP', '192.168.1.14')
        )
