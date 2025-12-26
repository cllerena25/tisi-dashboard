from sqlalchemy import create_engine
from models import Base

# Conexión a MySQL
engine = create_engine(
    "mysql+pymysql://tisi_app:TisiApp2025!@localhost:3307/tisi_facturas",
    pool_pre_ping=True
)

# Crear todas las tablas definidas en los modelos
Base.metadata.create_all(engine)

print("✅ Tablas creadas correctamente en la base tisi_facturas")
