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
    step = 0
    prev = 0

    while True:
        if (button.is_pressed) and prev == 0:
            step += 1
            prev = 1
            press_time = now()
            arr.append(press_time)
            if len(arr) > 5:
                arr.pop(0);
            diff = press_time - arr[0]
            print("diff", diff)
            current_speed = (len(arr) * 60* 1000000000) / diff
            if len(arr) < 2:
                current_speed = 0
            speed_str = str(current_speed)
            print("speed:", speed_str)
            await websocket.send(speed_str)

        if not (button.is_pressed):
            prev = 0

start_server = websockets.serve(hello, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
