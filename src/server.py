from aiohttp import web

async def handle_ping(request):
    return web.Response(text="Durov is watching you. Status: 200 OK", status=200)

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping) # Корень сайта
    
    # Настройка порта для Render
    from src.config import config
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', config.PORT)
    print(f"--- Веб-сервер запущен на порту {config.PORT} ---")
    await site.start()