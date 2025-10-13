# Fischertechnik Industry 4.0 API
REST API for controlling Fischertechnik Industry 4.0 factory automation system. The server manages storage operations, cargo processing, and provides real-time status monitoring.

## Table of Contents
- [Overview](#table-of-contents)
- [API Guide](#api-guide)
  - [Get Storage State](#get-storage-state)
  - [Get System Status](#get-system-status)
  - [Write Storage State](write-storage-state)
  - [Process Cargos](#process-cargos)
  - [Return Cargos](#return-cargos)
  - [Sort Cargos](#sort-cargos)
  - [Get Queue Status](#get-queue-status)
  - [Error Responses](#error-responses)
- [Quick Start](#build)
# API Guide
Base URL
```
http://localhost:8000
```

Storage Matrix Layout
```
(1,1) (1,2) (1,3)
(2,1) (2,2) (2,3)  
(3,1) (3,2) (3,3)
```

> [!NOTE]
> Tasks are executed asynchronously. Use /queue_status to monitor progress.

## Get Storage State
```
GET /get_storage
```
Retrieves the current state of the 3x3 storage matrix.

Response:
```
[
  [1, 1, 1],
  [2, 2, 2], 
  [3, 3, 3]
]
 ```
Color Codes:
- 1 - White cargo
- 2 - Blue cargo
- 3 - Red cargo
- 4 - Undefined cargo
- 5 - Empty cell

## Get System Status
```
GET /get_status
```
Retrieves the operational status of all microcontroller components.

Response:
```
{
  "storage": "Ожидаю",
  "crane": "Ожидаю",
  "handle_center": "Ожидаю",
  "sort_center": "Ожидаю"
}
```

Status Values:
- "Ожидаю" - Waiting/Idle
- "Anything else" - Working/Processing

## Write Storage State
```
POST /write_storage
```
Updates the entire storage storage with new cargo configuration.

Request:
```
{
  "cargos":
  [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
  ]
}
```

Response:
```
{
  "status": "queued",
  "task": "write_storage"
}
```

## Process Cargos
```
POST /process_cargos
```
Initiates cargo processing cycle for specified coordinates. Leaves processed cargos in the sorting center.

Request:
```
{
  "coords":
  [
    [2, 2],
    [1, 2]
  ]
}
```
Coordinate System:
[row, column] format (1-based indexing)
Example: [3, 3] = bottom-right cell

Response:
```
{
  "status": "queued", 
  "task": "process_cargos"
}
```

## Return Cargos
```
POST /return_cargos
```
Returns cargos from sorting center back to storage. 
> [!NOTE] 
> All storage cells must be empty before operation.

Request:
```
{
  "cargos":
  [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
  ]
}
```

Response:
```
{
  "status": "queued",
  "task": "return_cargos"
}
```

## Sort Cargos
```
POST /sort_cargos
```
Performs complete cargo cycle: identification and return to storage with final configuration.

Request:
```
{
  "cargos":
  [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
  ]
}
```

Response:
```
{
  "status": "queued",
  "task": "sort_cargos"
}
```

## Get Queue Status
```
GET /queue_status
```
Retrieves current state of the asynchronous task queue.

Response:
```
{
  "queue_size": 2,
  "tasks_in_progress": 1
}
```

Fields:
- queue_size - Number of pending tasks in queue
- tasks_in_progress - Number of currently executing tasks

## Error Responses
Not Found(404)

Responce:
```
{
  "detail": "Not Found"
}
```

# Build
The build takes place via docker. The server is routed through nginx

## Environment
The settings go through the environment variables in docker-compose.
```
- FACTORY_MODE=mock
- SERVER_HOST=0.0.0.0
- SERVER_PORT=8000
- STORAGE_IP=192.168.1.10
- CRANE_IP=192.168.1.11
- SORT_CENTER_IP=192.168.1.12
- SHIPMENT_CENTER_IP=192.168.1.13
- PAINT_CENTER_IP=192.168.1.14
```

The server can operate in two modes:
- mock
- real

> [!NOTE]
> In mock, the server does not connect to real hardware, but only simulates operation.

## Running
To run tests:
```
docker-compose up tests
```

To run server:
```
docker-compose up fastapi ngingx
```


