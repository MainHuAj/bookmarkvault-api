from sqlalchemy import create_engine,String
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session


class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "messages"
    id:Mapped[int] = mapped_column(primary_key=True)
    content : Mapped[str] = mapped_column(String(200))

    def __repr__(self) -> str:
        return f"Message (id = {self.id} , content = {self.content!r})"
    
DATABASE_URL = "postgresql+psycopg2://abhinavjain@localhost:5432/bookmarkvault"
engine = create_engine(DATABASE_URL,echo=True)

Base.metadata.create_all(engine)

with Session(engine) as session:
    msg = Message(content="Hello from the ORM")
    session.add(msg)
    session.commit()

    print(f"\n→ After commit, msg has id: {msg.id}\n")

    all_messages = session.query(Message).all()
    for m in all_messages:
        print(f"   {m}")