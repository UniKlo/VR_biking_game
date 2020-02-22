#!/usr/bin/env python3

import asyncio
import websockets
from gpiozero import Button
import time
from time import thread_time_ns as now


async def hello(websocket, path):
    button = Button(17)
    begin = now()
    arr = list()
    arr.append(begin)

    while True:
       if (button.is_pressed):
            prev = False
            press_time = now()
            arr.append(press_time)
            if len(arr) > 5:
                arr.pop(0);
       if len(arr) < 2:
           speed = '0'
       else:
           diff = now() - arr[0]
           speed = (len(arr) * 60 * 60 * 1000000000) / diff
           speed = str(speed)
       print("speed:", speed)

       await websocket.send(speed)
       time.sleep(0.5)

start_server = websockets.serve(hello, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
