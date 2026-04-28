from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from datetime import datetime

engine = create_engine('sqlite+pysqlite:///orders.db')
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    service: Mapped[str] = mapped_column(nullable=False)
    master: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    time: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

def init_db():
    Base.metadata.create_all(engine)