#!/usr/bin/env python3

import os
import time
import logging
import asyncio

import click
import logbook
from logbook import Logger
from aiogram.utils.executor import Executor

from alarmbot.loghandlers import ColorizedStderrHandler


# Configure logging
logger = Logger(__name__)
logger.handlers.append(ColorizedStderrHandler())


@click.command()
@click.option('-s', '--socket', type=click.Path())
@click.argument('port', default=8006, type=int)
def main(socket, port):
    from alarmbot.views import app
    from alarmbot.receptionist import dp
    logger.level = logbook.DEBUG
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    executor = Executor(dp, skip_updates=True, loop=loop)
    logger.info('{}', executor)
    executor.set_webhook(web_app=app)
    if not socket:
        executor.run_app(port=port)
    else:
        executor.run_app(path=socket)
        # Try to fix file permission
        for i in range(5):
            if os.path.exists(socket):
                os.chmod(socket, 0o666)
                break
            time.sleep(1)


if __name__ == '__main__':
    main()
