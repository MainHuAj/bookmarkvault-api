from sqlalchemy import create_engine,String,func,DateTime
from sqlalchemy.orm import DeclarativeBase , Mapped,mapped_column,Session
from typing import Optional
import datetime

class Base(DeclarativeBase):
    pass

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id : Mapped[int] = mapped_column(primary_key=True)
    url : Mapped[str] = mapped_column(String(500),nullable=False)
    title : Mapped[str] = mapped_column(String(200),nullable=False)
    description : Mapped[Optional[str]] = mapped_column(String(1000),nullable=True)
    created_at : Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone = True),                  
        server_default=func.now(),
        nullable=False
        )

    def __repr__(self) -> str:
        return f"Bookmark (id = {self.id}) ,(title = {self.title}) , (description = {self.description}) , (url = {self.url}) , (created_at = {self.created_at})"
    
DATABASE_URL = "postgresql+psycopg2://abhinavjain@localhost:5432/bookmarkvault"
engine = create_engine(DATABASE_URL,echo=True)

Base.metadata.create_all(engine)

with Session(engine) as session:
    bookmark1 = Bookmark(url = "http://michael_jordan.com",title = "The legend of Michael Jordan",description = "How Michael became one of the best sportsman")


    bookmark2 = Bookmark(url = "http://apple.com",title = "The rise of Apple",description = "How Apple became one of the best companies in the world")


    bookmark3 = Bookmark(url = "http://anthropic.com",title = "A Legend born ",description = "Mythos is a miracle")
    session.add_all([bookmark1,bookmark2,bookmark3])

    session.commit()

    all_bookmarks = session.query(Bookmark).all()
    all_bookmarks_count = session.query(Bookmark).count()

    print(f"Total Number of bookmarks is {all_bookmarks_count}")

    for b in all_bookmarks:
        print(f"   {b}")
