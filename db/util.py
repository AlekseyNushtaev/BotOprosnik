import datetime

from sqlalchemy import select, insert, update

from db.models import Session, User


def add_user_to_db(id, username, first_name, last_name, time_start):
    with Session() as session:
        try:
            query = select(User).where(User.id == id)
            results = session.execute(query)
            if not results.all():
                stmt = insert(User).values(
                    id=id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    time_start=time_start
                )
                session.execute(stmt)
                session.commit()
        except Exception as e:
            print(e)


def update_user_credit(id, credit):
    with Session() as session:
        try:
            stmt = update(User).where(User.id == id).values(credit=credit, time_credit=datetime.datetime.now())
            session.execute(stmt)
            session.commit()
        except Exception as e:
            print(e)


def update_user_ipoteka(id, ipoteka):
    with Session() as session:
        try:
            stmt = update(User).where(User.id == id).values(ipoteka=ipoteka, time_ipoteka=datetime.datetime.now())
            session.execute(stmt)
            session.commit()
        except Exception as e:
            print(e)


def update_user_house(id, house):
    with Session() as session:
        try:
            stmt = update(User).where(User.id == id).values(house=house, time_house=datetime.datetime.now())
            session.execute(stmt)
            session.commit()
        except Exception as e:
            print(e)


def update_user_auto(id, auto):
    with Session() as session:
        try:
            stmt = update(User).where(User.id == id).values(auto=auto, time_auto=datetime.datetime.now())
            session.execute(stmt)
            session.commit()
        except Exception as e:
            print(e)


def update_user_sdelki(id, sdelki):
    with Session() as session:
        try:
            stmt = update(User).where(User.id == id).values(sdelki=sdelki, time_sdelki=datetime.datetime.now())
            session.execute(stmt)
            session.commit()
        except Exception as e:
            print(e)


def update_user_pay_credit(id, pay_credit):
    with Session() as session:
        try:
            stmt = update(User).where(User.id == id).values(pay_credit=pay_credit, time_pay_credit=datetime.datetime.now())
            session.execute(stmt)
            session.commit()
        except Exception as e:
            print(e)


def update_user_debit(id, debit):
    with Session() as session:
        try:
            stmt = update(User).where(User.id == id).values(debit=debit, time_debit=datetime.datetime.now())
            session.execute(stmt)
            session.commit()
        except Exception as e:
            print(e)


def update_user_phone(id, phone):
    with Session() as session:
        try:
            stmt = update(User).where(User.id == id).values(phone=phone, time_phone=datetime.datetime.now())
            session.execute(stmt)
            session.commit()
        except Exception as e:
            print(e)


def update_user_blocked(id):
    with Session() as session:
        try:
            stmt = update(User).where(User.id == id).values(is_block=True)
            session.execute(stmt)
            session.commit()
        except Exception as e:
            print(e)


def update_user_unblocked(id):
    with Session() as session:
        try:
            stmt = update(User).where(User.id == id).values(is_block=False)
            session.execute(stmt)
            session.commit()
        except Exception as e:
            print(e)


def get_all_users():
    with Session() as session:
        query = select(User)
        users = session.execute(query)
        result = [['id', 'username', 'first_name', 'last_name', 'Время входа в бота',
                      'Сумма кредитов', 'Ипотека', 'Недвижимость', 'Автомобиль',
                   'Сделки за 3 года', 'Ежемесячный кредит', 'Доход', 'Телефон',
                   'Время оформления заявки', 'Блокировка бота']]
        for user in users.scalars():
            start = ''
            join = ''
            if user.time_start:
                start = user.time_start.strftime('%Y-%m-%d   %H:%M:%S')
            if user.time_phone:
                join = user.time_phone.strftime('%Y-%m-%d   %H:%M:%S')
            result.append([user.id, user.username, user.first_name, user.last_name,
                           start, user.credit, user.ipoteka, user.house, user.auto,
                           user.sdelki, user.pay_credit, user.debit, user.phone, join, user.is_block])
    return result


def get_all_users_unblock():
    with Session() as session:
        query = select(User).where(User.is_block == False)
        users = session.execute(query)
        result = []
        for user in users.scalars():
            result.append(user.id)
    return result

