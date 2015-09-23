from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


# Our common Model base class
Base = declarative_base()


# Many-to-Many table to track a Name's Nicknames
"""
Column   Type
======   ====
RealNameID Integer
NickNameID String(100)
"""
realname_nickname_association_table = Table(
    'RealnameNicknameAssociation', Base.metadata,
    Column('RealNameID', Integer, ForeignKey('Names.ID'), primary_key=True),
    Column('NickNameID', Integer, ForeignKey('Names.ID'), primary_key=True)
)


class Name(Base):
    """
    A model to represent a first name and its alternative names (i.e. nicknames)

    Column   Type
    ======   ====
    ID       Integer
    RealName String(100)

    """
    __tablename__ = 'Names'

    id = Column('ID', Integer, primary_key=True)
    real_name = Column('RealName', String(100), nullable=False, index=True, unique=True)
    nick_names = relationship(
        'Name',
        secondary=realname_nickname_association_table,
        primaryjoin=id == realname_nickname_association_table.c.RealNameID,
        secondaryjoin=id == realname_nickname_association_table.c.NickNameID,
        backref='real_names'
    )

    def __init__(self, real_name=None, nick_names=None):
        if real_name:
            self.real_name = real_name
        if nick_names:
            self.nick_names = nick_names

    def __repr__(self):
        return 'Name({n})'.format(n=self.real_name)
