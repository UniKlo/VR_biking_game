#!/usr/bin/env python3

import asyncio
import websockets
from gpiozero import Button
import time
from time import time_ns as now

async def hello(websocket, path):
    button = Button(17)
    begin = now()
    arr = list()
    arr.append(begin)
    step = 0
    prev = 0
    speed = 0
    pre_decay = 0
    sample_size = 5
    ns_to_min = 60000000000

    while True:
        if (button.is_pressed) and prev == 0:
            step += 1
            prev = 1
            press_time = now()
            arr.append(press_time)
            if len(arr) > sample_size:
                arr.pop(0);

            diff = arr[len(arr) -1] - arr[0]
            #rotation per minut
            current_speed = (len(arr) * ns_to_min) / diff
            if step < 40:
                print("step", step)
                scaler = (-(1/2)**(step/5 -1) + 2)/2
#                print("I m scaler", scaler, "for step", step,
#                     "current_speed before:", current_speed)
                speed = scaler * current_speed
        if not (button.is_pressed):
            prev = 0

        if speed > 1:
            #decay is the time diff from the last click to current, unit in second
            decay = int((now() - arr[len(arr) - 1])/1000000000)
            if decay > pre_decay:
#                print("this is decay", decay, "prev", pre_decay)
                scaler = ((1/2) ** (decay/2 - 1))/2
                speed = scaler * speed
                pre_decay = decay
                print("this is decay", decay, "prev", pre_decay, "scaler", scaler)
            if decay < 1:
                pre_decay = 0
                
        else:
            speed = 0
            step = 0

        speed_str = str(speed)
        print("speed:", speed_str)
        await websocket.send(speed_str)

start_server = websockets.serve(hello, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
