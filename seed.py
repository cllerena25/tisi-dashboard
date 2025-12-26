from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Client, Invoice, Payment, AuditLog
import random
import datetime

# Conexión a MySQL
engine = create_engine("mysql+pymysql://tisi_app:TisiApp2025!@localhost:3307/tisi_facturas")
Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------
# Usuarios de prueba (solo si no existen)
# -----------------------------
if session.query(User).count() == 0:
    usuarios = [
        User(username="admin", password_hash="hash_admin", role="admin"),
        User(username="staff1", password_hash="hash_staff1", role="staff"),
        User(username="staff2", password_hash="hash_staff2", role="staff"),
        User(username="client1", password_hash="hash_client1", role="client"),
        User(username="client2", password_hash="hash_client2", role="client"),
    ]
    session.add_all(usuarios)
    session.commit()
    print("✅ Usuarios insertados")
else:
    usuarios = session.query(User).all()
    print("⚠️ Usuarios ya existen, no se insertaron duplicados")

# -----------------------------
# Clientes de prueba (solo si no existen)
# -----------------------------
if session.query(Client).count() == 0:
    clientes = []
    for i in range(1, 21):  # 20 clientes
        cliente = Client(
            name=f"Cliente {i}",
            email=f"cliente{i}@mail.com",
            phone=f"99999{i:03}",
            address=f"Calle {i} - Lima"
        )
        clientes.append(cliente)

    session.add_all(clientes)
    session.commit()
    print("✅ 20 clientes insertados")
else:
    clientes = session.query(Client).all()
    print("⚠️ Clientes ya existen, no se insertaron duplicados")

# -----------------------------
# Facturas y pagos de prueba (solo si no existen)
# -----------------------------
if session.query(Invoice).count() == 0:
    estados = ["pending", "paid", "cancelled"]
    metodos_pago = ["cash", "card", "transfer"]

    facturas = []
    pagos = []

    for i in range(1, 51):  # 50 facturas
        cliente = random.choice(clientes)
        estado = random.choice(estados)
        factura = Invoice(
            client_id=cliente.id,
            invoice_date=datetime.date(2025, random.randint(1, 12), random.randint(1, 28)),
            total=round(random.uniform(100, 5000), 2),
            status=estado
        )
        facturas.append(factura)
        session.add(factura)
        session.flush()  # asegura que tenga ID

        # Si la factura está pagada, crear pago
        if estado == "paid":
            pago = Payment(
                invoice_id=factura.id,
                payment_date=factura.invoice_date,
                amount=factura.total,
                method=random.choice(metodos_pago)
            )
            pagos.append(pago)
            session.add(pago)

    session.commit()
    print("✅ 50 facturas y pagos insertados")
else:
    print("⚠️ Facturas ya existen, no se insertaron duplicados")

# -----------------------------
# Auditoría de prueba (solo si no existen)
# -----------------------------
if session.query(AuditLog).count() == 0:
    acciones = [
        "Creación de factura",
        "Actualización de estado",
        "Registro de pago",
        "Cancelación de factura",
        "Consulta de reporte"
    ]

    logs = []
    for i in range(1, 31):  # 30 registros de auditoría
        log = AuditLog(
            user_id=random.choice(usuarios).id,
            action=random.choice(acciones),
            log_date=datetime.datetime.now()
        )
        logs.append(log)

    session.add_all(logs)
    session.commit()
    print("✅ 30 registros de auditoría insertados")
else:
    print("⚠️ Auditoría ya existe, no se insertaron duplicados")