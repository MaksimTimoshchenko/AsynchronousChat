from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///client_db.sqlite', echo=True)
Base = declarative_base()

class MessageHistory(Base):

    __tablename__ = 'messages_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_sender_login = Column(String)
    client_recipient_login = Column(String)
    message = Column(String)
    sent_at = Column(DateTime)

    def __init__(self, client_sender_login, client_recipient_login, message, sent_at):
        self.client_sender_login = client_sender_login
        self.client_recipient_login = client_recipient_login
        self.message = message
        self.sent_at = sent_at

    def __repr__(self):
        return f'{self.send_time} {self.client_sender_login} to {self.client_recipient_login} message: {self.message}'


class ClientContact(Base):

    __tablename__ = 'client_contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_login = Column(String)
    contactee_login = Column(String)

    def __init__(self, client_login, contactee_login):
        self.client_login = client_login
        self.contactee_login = contactee_login

    def __repr__(self):
        return f"{self.client_login} contacted {self.contactee_login}"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
