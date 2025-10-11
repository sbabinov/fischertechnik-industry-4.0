import uvicorn
from src import Config, Factory, create_app

if __name__ == "__main__":
    config = Config.from_env()
    factory = Factory({
        'storage_ip': config.storage_ip,
        'crane_ip': config.crane_ip,
        'sort_center_ip': config.sort_center_ip,
        'shipment_center_ip': config.shipment_center_ip,
        'paint_center_ip': config.paint_center_ip
    })

    app, host, port = create_app(factory, "192.168.1.41", 8000)
    uvicorn.run(app, host=host, port=port)
