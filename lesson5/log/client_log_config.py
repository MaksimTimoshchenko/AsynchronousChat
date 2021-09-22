import logging
from logging.handlers import RotatingFileHandler
from functools import wraps


client_logger = logging.getLogger('client')

handler = RotatingFileHandler(
    filename='log/files/client.log',
    maxBytes=1000,
    backupCount=5,
    delay=True
)
handler.namer = lambda name: name.replace(".log", "") + ".log"
formater = logging.Formatter("%(asctime)-25s %(levelname)s %(module)s: %(message)s")
handler.setFormatter(formater)

client_logger.addHandler(handler)
client_logger.setLevel(logging.INFO)

def log(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        client_logger.info(f'Function {log.__name__}({args, kwargs}) called from {func.__name__}')
        return func(*args, **kwargs)
    return decorator
