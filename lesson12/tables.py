from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey


engine = create_engine('sqlite:///db.sqlite', echo=True)
Base = declarative_base()

class Client(Base):

    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String)
    information = Column(String)
    history = relationship('ClientHistory', back_populates='client')
    contacts = relationship('Contact', back_populates='client', foreign_keys = 'Contact.client_id')

    def __init__(self, login, information=''):
        self.login = login
        self.information = information

    def __repr__(self):
        return self.login


class ClientHistory(Base):

    __tablename__ = 'clients_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_login_time = DateTime(String)
    ip_address = Column(String)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', back_populates='history')

    def __init__(self, last_login_time, ip_address, client_id):
        self.last_login_time = last_login_time
        self.ip_address = ip_address
        self.client_id = client_id

    def __repr__(self):
        return f"{self.last_login_time}, IP: {self.ip_address}: {self.client_id}"


class Contact(Base):

    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    contactee_client_id = Column(Integer, ForeignKey('clients.id'))

    client = relationship('Client', back_populates='contacts', foreign_keys=[client_id])
    contactee = relationship('Client', foreign_keys=[contactee_client_id])

    def __init__(self, client_id, contactee_client_id):
        self.client_id = client_id
        self.contactee_client_id = contactee_client_id

    def __repr__(self):
        return f"{self.client_id} contacted {self.contactee_client_id}"


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    