from sqlalchemy.orm import Session

from app.core.utils.database import SessionLocal

def get_db():
    """
    Get the database session.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_and_refresh(db: Session, obj):
    """
    Add an object to the database, commit the transaction, and refresh the object.

    Args:
        db (Session): The SQLAlchemy session.
        obj: The SQLAlchemy model object to be added to the database.

    Returns:
        The refreshed object.
    """
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
    
    except Exception as e:
        db.rollback()
        raise e
    
    return obj