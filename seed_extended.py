from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Client, Invoice, Payment, AuditLog
import random
import datetime

# Conexión a MySQL
engine = create_engine("mysql+pymysql://tisi_app:TisiApp2025!@localhost:3307/tisi_facturas")
Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------
# Usuarios de prueba (solo se crean si no existen)
# -----------------------------
usuarios_existentes = session.query(User).all()
if not usuarios_existentes:
    usuarios = [
        User(username="admin", password_hash="hash_admin", role="admin"),
        User(username="staff1", password_hash="hash_staff1", role="staff"),
        User(username="staff2", password_hash="hash_staff2", role="staff"),
        User(username="client1", password_hash="hash_client1", role="client"),
        User(username="client2", password_hash="hash_client2", role="client"),
    ]
    session.add_all(usuarios)
    session.commit()
    print("✅ Usuarios iniciales insertados")
else:
    usuarios = usuarios_existentes
    print("⚠️ Usuarios ya existen, no se insertaron duplicados")

# -----------------------------
# Clientes de prueba (se agregan nuevos cada ejecución)
# -----------------------------
clientes = session.query(Client).all()
cantidad_actual = len(clientes)
nuevos_clientes = []

for i in range(cantidad_actual + 1, cantidad_actual + 6):  # agrega 5 clientes nuevos cada vez
    cliente = Client(
        name=f"Cliente {i}",
        email=f"cliente{i}@mail.com",
        phone=f"99999{i:03}",
        address=f"Calle {i} - Lima"
    )
    nuevos_clientes.append(cliente)

session.add_all(nuevos_clientes)
session.commit()
print(f"✅ {len(nuevos_clientes)} clientes nuevos insertados")

# -----------------------------
# Facturas y pagos de prueba (se agregan nuevas cada ejecución)
# -----------------------------
estados = ["pending", "paid", "cancelled"]
metodos_pago = ["cash", "card", "transfer"]

clientes = session.query(Client).all()
facturas_nuevas = []
pagos_nuevos = []

for i in range(1, 11):  # agrega 10 facturas nuevas cada vez
    cliente = random.choice(clientes)
    estado = random.choice(estados)
    factura = Invoice(
        client_id=cliente.id,
        invoice_date=datetime.date.today() - datetime.timedelta(days=random.randint(0, 30)),
        total=round(random.uniform(100, 5000), 2),
        status=estado
    )
    facturas_nuevas.append(factura)
    session.add(factura)
    session.flush()

    if estado == "paid":
        pago = Payment(
            invoice_id=factura.id,
            payment_date=factura.invoice_date,
            amount=factura.total,
            method=random.choice(metodos_pago)
        )
        pagos_nuevos.append(pago)
        session.add(pago)

session.commit()
print(f"✅ {len(facturas_nuevas)} facturas nuevas y {len(pagos_nuevos)} pagos insertados")

# -----------------------------
# Auditoría de prueba (se agregan nuevas cada ejecución)
# -----------------------------
acciones = [
    "Creación de factura",
    "Actualización de estado",
    "Registro de pago",
    "Cancelación de factura",
    "Consulta de reporte"
]

logs_nuevos = []
for i in range(1, 6):  # agrega 5 registros de auditoría cada vez
    log = AuditLog(
        user_id=random.choice(usuarios).id,
        action=random.choice(acciones),
        log_date=datetime.datetime.now()
    )
    logs_nuevos.append(log)

session.add_all(logs_nuevos)
session.commit()
print(f"✅ {len(logs_nuevos)} registros de auditoría nuevos insertados")