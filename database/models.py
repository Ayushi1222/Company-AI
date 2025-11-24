from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    persona = Column(String(50))
    message_count = Column(Integer, default=0)
    companies_researched = Column(JSON)
    history = Column(JSON)


class AccountPlan(Base):
    __tablename__ = 'account_plans'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    plan_data = Column(JSON)
    research_data = Column(JSON)
    exported_count = Column(Integer, default=0)
    last_exported = Column(DateTime)


class Analytics(Base):
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True)
    event_type = Column(String(100), nullable=False)
    event_data = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(100))


def init_database(database_url: str = "sqlite:///./account_plans.db"):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
