from fastapi import FastAPI
from app.core.utils.database import Base, engine 
from app.core.models import user, member, role, organisation, invites

from app.api import auth, invitations, users, stats, membership

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Elencho",
    description="RBAC API",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(invitations.router)
app.include_router(membership.router)
app.include_router(stats.router)

@app.get("/")
@app.get("/health-check")
def health_check():
    """
    Health check endpoint.
    """
    return {
        "message": "Elencho is up and running!"
        }

