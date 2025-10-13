import uvicorn
from src import Config, Factory, MockFactory, create_app

if __name__ == "__main__":
    config = Config.from_env()
    if config.factory_mode == "real":
        factory = Factory({
            "storage_ip": config.storage_ip,
            "crane_ip": config.crane_ip,
            "sort_center_ip": config.sort_center_ip,
            "shipment_center_ip": config.shipment_center_ip,
            "paint_center_ip": config.paint_center_ip
        })
    elif config.factory_mode == "mock":
        factory = MockFactory({})
    else:
        raise ValueError(f"Unknown mode: {config.factory_mode}")

    app, host, port = create_app(factory, config.server_host, config.server_port)
    uvicorn.run(app, host=host, port=port)
