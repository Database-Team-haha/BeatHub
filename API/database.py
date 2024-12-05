from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")

# Database configuration
DATABASE_URL = f"postgresql://{os.getenv('USER_DB')}:{os.getenv('PASSWORD_DB')}@{os.getenv('HOST_DB')}:{os.getenv('PORT_DB')}/{os.getenv('NAME_DB')}"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a base class for declarative models
Base = declarative_base()

# Sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Metadata instance for tables
metadata = MetaData()

# Create tables in the database
Base.metadata.create_all(bind=engine)
