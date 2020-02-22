#!/usr/bin/env python3

# WS client example

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
       while True:
            speed = await websocket.recv()
            print(f"< {speed}")

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
