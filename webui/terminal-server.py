import os, asyncio, websockets

WELCOME = "Kydras terminal ready"
HOST = os.getenv("KES_TERMINAL_HOST", "127.0.0.1")
PORT = int(os.getenv("KES_TERMINAL_PORT", "8788"))

async def handler(ws):
    await ws.send(WELCOME)
    async for msg in ws:
        await ws.send("ping" if msg == "ping" else msg)

async def main():
    async with websockets.serve(handler, HOST, PORT):
        await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
