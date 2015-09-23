from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager


engine = create_engine('sqlite:///:memory:')#, echo=True)
Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def db_connect():
    """Scope our db session around our transactional operations"""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def init_db():
    from .models import (
        Base,
        realname_nickname_association_table,
        Name
    )
    Base.metadata.create_all(bind=engine)


def destroy_db():
    from .models import (
        Base,
        realname_nickname_association_table,
        Name
    )
    Base.metadata.drop_all(bind=engine)


def create_db():
    import os
    import csv
    from beacon import ASSESTS_PATH

    init_db()

    # Populate our Names table with the Nicknames mapping found in assets/nicknames.csv
    with open(os.path.join(ASSESTS_PATH, 'nicknames.csv'), 'r') as nicknames_csv:
        from .models import Name
        for row in csv.reader(nicknames_csv):
            nickname, real_name, likelihood = row
            nickname = nickname.capitalize()
            real_name = real_name.capitalize()

            with db_connect() as session:
                # Pull the existing name and nickname out of the db if they exist
                db_name = session.query(Name).filter_by(real_name=real_name).first()
                db_nickname = session.query(Name).filter_by(real_name=nickname).first()

                if db_name:
                    # Both names existed, add existing nickname to name
                    if db_nickname:
                        db_name.nick_names.append(db_nickname)
                    # The nickname didn't exist in the db - create, add to name, add to db
                    else:
                        new_nickname = Name(nickname)
                        db_name.nick_names.append(new_nickname)
                        session.add(new_nickname)
                else:
                    # The real_name didn't exist in the db - create one and add to db
                    new_name = Name(real_name)
                    session.add(new_name)

                    # The nickname exists in the db - add to name
                    if db_nickname:
                        new_name.nick_names.append(db_nickname)
                    # The nickname didn't exist in the db - create, add to name, add to db
                    else:
                        new_nickname = Name(nickname)
                        new_name.nick_names.append(new_nickname)
                        session.add(new_nickname)
