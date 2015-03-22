from tornado import web, ioloop
from sockjs.tornado import SockJSRouter
from iu.server import GameConnection, main_loop
from iu.utils import logger



if __name__ == "__main__":
    logger.info("Starting up")

    gameRouter = SockJSRouter(GameConnection, '/game')
    app = web.Application(gameRouter.urls, debug=True)

    logger.info("Starting to listen for connections")
    app.listen(8000)

    loop = ioloop.IOLoop.instance()

    logger.info("Creating periodic callback")
    pc = ioloop.PeriodicCallback(main_loop, 1000/8)
    pc.start()

    logger.info("Starting IOLoop")
    loop.start()
