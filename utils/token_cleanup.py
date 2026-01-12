from datetime import datetime
from sqlalchemy.orm import Session
from api.auth import token_model

def cleanup_expired_tokens(db: Session):
    """
    Delete all blacklisted tokens from the database that have expired.
    """
    db.query(token_model.BlacklistedToken).filter(
        token_model.BlacklistedToken.expires_at < datetime.utcnow()
    ).delete()
    db.commit()
