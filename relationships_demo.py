from sqlalchemy import create_engine
from sqlalchemy.orm import Session, selectinload

from models import Base, User, Bookmark, Tag


DATABASE_URL = "postgresql+psycopg2://abhinavjain@localhost:5432/bookmarkvault"
engine = create_engine(DATABASE_URL, echo=True)


def main():

    with Session(engine) as session:
        user1 = User(email="aj@example.com", name="AJ")
        user2 = User(email="dev@example.com", name="Dev")

        tag_python = Tag(name="python")
        tag_ai = Tag(name="ai")
        tag_tools = Tag(name="tools")

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


if __name__ == "__main__":
    main()