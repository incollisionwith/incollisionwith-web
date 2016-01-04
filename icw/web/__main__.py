import asyncio

from .app import get_app

app = get_app()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    handler = app.make_handler()
    f = loop.create_server(handler, '0.0.0.0', 8081)
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()