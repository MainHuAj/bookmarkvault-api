from sqlalchemy import create_engine,String,DateTime,func,ForeignKey,Table,Column,Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
    relationship,
    selectinload
)
from typing import Optional,List
import datetime

class Base(DeclarativeBase):
    pass

bookmark_tags = Table(
    "bookmark_tags",
    Base.metadata,
    Column("bookmark_id",ForeignKey("bookmarks.id"),primary_key=True),
    Column("tag_id",ForeignKey("tags.id"),primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(String(200),unique=True)
    name : Mapped[str] = mapped_column(String(100))

    bookmarks:Mapped[List["Bookmark"]] = relationship(
        back_populates="user",
        cascade="all , delete-orphan"

    )

    def __repr__(self) -> str:
        return f"User (id = {self.id} , name = {self.name!r} , email = {self.email!r})"

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id:Mapped[int] = mapped_column(primary_key=True)
    url:Mapped[str] = mapped_column(String(500))
    title:Mapped[str] = mapped_column(String(200))
    description:Mapped[Optional[str]] = mapped_column(String(1000))
    created_at:Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"))

    user :Mapped["User"]=relationship(back_populates="bookmarks")

    tags: Mapped[List["Tag"]] = relationship(
    secondary=bookmark_tags,
    back_populates="bookmarks",
)

    def __repr__(self) -> str:
        return f"Bookmark(id={self.id}, title={self.title!r}, user_id={self.user_id})"
    
class Tag(Base):
    __tablename__ = "tags"

    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(50),unique=True)

    bookmarks:Mapped[List[Bookmark]] = relationship(
        secondary=bookmark_tags,
        back_populates="tags"
    )
    def __repr__(self) -> str:
        return f"Tag(id={self.id}, name={self.name!r})"
    
DATABASE_URL = "postgresql+psycopg2://abhinavjain@localhost:5432/bookmarkvault"
engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)


with Session(engine) as session:
    # Create users
    user1 = User(email="aj@example.com", name="AJ")
    user2 = User(email="dev@example.com", name="Dev")

    # Create tags
    tag_python = Tag(name="python")
    tag_ai = Tag(name="ai")
    tag_tools = Tag(name="tools")

    # Create bookmarks with tags
    bookmark1 = Bookmark(
        url="https://anthropic.com",
        title="Anthropic",
        description="AI safety research lab",
        tags=[tag_ai],
    )
    bookmark2 = Bookmark(
        url="https://github.com",
        title="GitHub",
        description="Where code lives",
        tags=[tag_tools],
    )
    bookmark3 = Bookmark(
        url="https://stackoverflow.com",
        title="Stack Overflow",
        description=None,
        tags=[tag_python, tag_tools],
    )

    user1.bookmarks = [bookmark1]
    user2.bookmarks = [bookmark2, bookmark3]

    session.add_all([user1, user2])
    session.commit()

    print("\n=== Users, bookmarks, and tags ===\n")
    all_users = (
        session.query(User)
        .options(selectinload(User.bookmarks).selectinload(Bookmark.tags))
        .all()
    )
    for u in all_users:
        print(f"{u}")
        for b in u.bookmarks:
            tag_names = [t.name for t in b.tags]
            print(f"   └─ {b.title} — tags: {tag_names}")
        print()