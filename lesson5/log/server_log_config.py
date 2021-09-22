import logging
from logging.handlers import TimedRotatingFileHandler


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
