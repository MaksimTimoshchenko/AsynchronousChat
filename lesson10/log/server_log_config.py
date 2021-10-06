import inspect
import logging

from logging.handlers import TimedRotatingFileHandler
from functools import wraps

server_logger = logging.getLogger('server')

handler = TimedRotatingFileHandler(
    filename='log/files/server.log',
    when='midnight',
    backupCount=5,
    utc=True,
    delay=True
)
handler.namer = lambda name: name.replace(".log", "") + ".log"
formater = logging.Formatter("%(asctime)-25s %(levelname)s %(module)s: %(message)s")
handler.setFormatter(formater)

server_logger.addHandler(handler)
server_logger.setLevel(logging.INFO)

def log(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        server_logger.info(f'Function {log.__name__}({args, kwargs}) called from function {inspect.stack()[1][3]}')
        return func(*args, **kwargs)
    return decorator
