#!/usr/bin/env python3

import mercury
import json
import signal
import asyncio
import websockets

from datetime import datetime

connected = set()

def stats_received(stats):
    print({"temp" : stats.temperature})
    print({"antenna" : stats.antenna})
    print({"protocol" : stats.protocol})
    print({"frequency" : stats.frequency})

def p(tag):
    x = {
        "tag": tag.epc.decode("utf-8"),
        "ts": tag.timestamp
    }
    print(json.dumps(x, indent=4, sort_keys=True))
    websockets.broadcast(connected, json.dumps(x, indent=4, sort_keys=True))

def signal_handler(sig, frame):
    pass

reader = mercury.Reader("tmr:///dev/ttyUSB1")

reader.set_region("EU3")
reader.set_read_plan(antennas=[1], protocol="GEN2", bank=["epc"], read_power=2000)



#reader.enable_stats(stats_received)
reader.start_reading(p)
#signal.signal(signal.SIGINT, signal_handler)
#signal.pause()
#reader.stop_reading()



async def handler(websocket):
    connected.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected.remove(websocket)

    async for message in websocket:
        await websocket.send(message)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
