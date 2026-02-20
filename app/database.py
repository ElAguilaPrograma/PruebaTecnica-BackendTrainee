from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ExpectedPayment(Base):
    __tablename__ = "expected_payments"
    id = Column(Integer, primary_key=True)
    batch = Column(String)
    customer_name = Column(String)
    amount = Column(Float)
    expected_date = Column(Date)

    received_payments = relationship("ReceivedPayment", back_populates="expected_payment")
class ReceivedPayment(Base):
    __tablename__ = "received_payments"
    id = Column(Integer, primary_key=True)
    expec_pay_id = Column(Integer, ForeignKey("expected_payments.id"))
    batch = Column(String)
    amount = Column(Float)
    received_date = Column(Date)

    expected_payment = relationship("ExpectedPayment", back_populates="received_payments")

