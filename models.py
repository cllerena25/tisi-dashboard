from sqlalchemy import Column, Integer, String, Date, DECIMAL, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship

# Base para todos los modelos
Base = declarative_base()

# Tabla de usuarios
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("admin", "staff", "client"), default="client")
    created_at = Column(TIMESTAMP)

    # Relación con auditoría
    audit_logs = relationship("AuditLog", back_populates="user")

# Tabla de clientes
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    address = Column(String(255))
    created_at = Column(TIMESTAMP)

    # Relación con facturas
    invoices = relationship("Invoice", back_populates="client")

# Tabla de facturas
class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    invoice_date = Column(Date, nullable=False)
    total = Column(DECIMAL(10,2), nullable=False)
    status = Column(Enum("pending", "paid", "cancelled"), default="pending")

    # Relaciones
    client = relationship("Client", back_populates="invoices")
    payments = relationship("Payment", back_populates="invoice")

# Tabla de pagos
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    payment_date = Column(Date, nullable=False)
    amount = Column(DECIMAL(10,2), nullable=False)
    method = Column(Enum("cash", "card", "transfer"), default="cash")

    # Relación con facturas
    invoice = relationship("Invoice", back_populates="payments")

# Tabla de auditoría
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(255), nullable=False)
    log_date = Column(TIMESTAMP)

    # Relación con usuarios
    user = relationship("User", back_populates="audit_logs")
