## Welcome to the Elenchos Docs!

Elenchos is an authentication system for multi-tenant SaaS powered with FastAPI, PostgreSQL, and JWT. It is designed to be used as a base for any SaaS project, and can be easily integrated with any frontend framework.

## Contents

- [Tech Stack, Tools and Libraries](#tech-stack-tools-and-libraries)
- [DB and Design](#db-and-design)
- [API Documentation](#api-documentation)
- [Setup & Environment](#setup)
- [Mailing system](#mailing-system)
- [Invitation](#invitation)
- [Statistics](#statistics)
- [Thank you!](#thank-you-you-can-check-out-my-other-projects)

## Tech Stack, Tools and Libraries

### Backend

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [JWT](https://jwt.io/)
- [smtplib](https://docs.python.org/3/library/smtplib.html)


### Frontend

- [Jinja2](https://jinja.palletsprojects.com/)

### Others

- [Visual Studio Code](https://code.visualstudio.com/)
- [Postman](https://www.postman.com/)
- [Git](https://git-scm.com/)


## DB, and Design

### Database

Postgresql is used as the primary database. The database schema is designed to be normalized and flexible, and can be easily extended to add more entities, and relationships.

### ORM - SQLAlchemy

SQLAlchemy is used as the ORM for the project. It is a powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a full suite of well-known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.


### User Schema (Example)

```python
class User(Base):
    """
    Model for user table.

    Attributes:
    id (int) : Unique identifier for user.
    email (str) : Email address of user.
    password (str) : Password of user.
    profile (dict) : Profile details of user.
    status (int) : Status of user.
    settings (dict) : Settings of user.
    created_at (int) : Created timestamp of user.
    updated_at (int) : Updated timestamp of user.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    profile = Column(JSON, default={}, nullable=False)
    status = Column(Integer, default=0, nullable=False)
    settings = Column(JSON, default={}, nullable=True)
    created_at = Column(BigInteger, nullable=True)
    updated_at = Column(BigInteger, nullable=True)

    memberships = relationship('Member', back_populates='user')
    organisations = relationship('Organisation', secondary='member', back_populates='users')
```

## API Documentation

Swagger UI can be used to test the API. It is available at `http://localhost:8000/docs`.
Additionally, check the [API Postman Documentation](/docs_assets/postman_collection.json) with examples, and sample requests.


## Setup

To set the project up locally, we'll be using venvs.

- Create a virtual environment

```bash
pip install virtualenv
virtualenv venv
```

- Activate the virtual environment

```bash
.\venv\Scripts\activate
```

- Install the dependencies

```bash
pip install -r requirements.txt
```

- Run the project

```bash
uvicorn main:app --reload --port 8000
```

## Mailing system

The in-house mailing system is developed from scratch through `smtplib` and `email` libraries. The system is designed to be flexible and can be easily extended to add more email templates, and configurations.

Also, to trigger the mailing system, `BackgroundTasks` are used in FastAPI. The system is designed to be asynchronous and non-blocking, and can be easily integrated with any other background task system.

### Email triggered on sign-in

![Sign-in Email](/docs_assets/login.png)

### Email triggered on password reset

![Password Reset Email](/docs_assets/reset.png)

## Invitation

The users can also invite other users to join their organisation. The invitation system is designed to be secure and flexible, and can be easily extended to add more features, and configurations.

### Email triggered on member invitation

![Invitation Email](/docs_assets/invite.png)

## Statistics

The users can also view statistics of their organisation. It includes role details, organisation member details and organisation grouped by role details. The statistics system is designed to be flexible and can be easily extended to add more features, and configurations.



## Thank you! You can check out my other projects!
