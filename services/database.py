from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Define the MariaDB engine using MariaDB Connector/Python
# https://fastapi.tiangolo.com/pt/tutorial/sql-databases/

SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://tester:123456@localhost:3306/test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
