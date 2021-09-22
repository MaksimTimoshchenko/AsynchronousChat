import logging
from logging.handlers import RotatingFileHandler


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
