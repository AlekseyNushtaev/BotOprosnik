from sqlalchemy import BigInteger, create_engine, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker
import atexit
import datetime


con_string = 'sqlite:///db/database.db'

engine = create_engine(con_string)
Session = sessionmaker(bind=engine, expire_on_commit=False)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    time_start: Mapped[datetime.datetime] = mapped_column(nullable=True)
    credit: Mapped[str] = mapped_column(nullable=True)
    time_credit: Mapped[datetime.datetime] = mapped_column(nullable=True)
    ipoteka: Mapped[str] = mapped_column(nullable=True)
    time_ipoteka: Mapped[datetime.datetime] = mapped_column(nullable=True)
    house: Mapped[str] = mapped_column(nullable=True)
    time_house: Mapped[datetime.datetime] = mapped_column(nullable=True)
    auto: Mapped[str] = mapped_column(nullable=True)
    time_auto: Mapped[datetime.datetime] = mapped_column(nullable=True)
    sdelki: Mapped[str] = mapped_column(nullable=True)
    time_sdelki: Mapped[datetime.datetime] = mapped_column(nullable=True)
    pay_credit: Mapped[str] = mapped_column(nullable=True)
    time_pay_credit: Mapped[datetime.datetime] = mapped_column(nullable=True)
    debit: Mapped[str] = mapped_column(nullable=True)
    time_debit: Mapped[datetime.datetime] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)
    time_phone: Mapped[datetime.datetime] = mapped_column(nullable=True)
    is_block: Mapped[bool] = mapped_column(default=False)
    time_block: Mapped[datetime.datetime] = mapped_column(nullable=True)
    time_unblock: Mapped[datetime.datetime] = mapped_column(nullable=True)


def create_tables():
    Base.metadata.create_all(engine)
