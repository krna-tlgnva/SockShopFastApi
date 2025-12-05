from sqlmodel import SQLModel, create_engine, Session as SQLSession
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=SQLSession
)

def init_db():
    import app.models.user  # noqa
    import app.models.product  # noqa
    import app.models.cart  # noqa
    import app.models.purchase 
    SQLModel.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
