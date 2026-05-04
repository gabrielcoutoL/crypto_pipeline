from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://admin:123@postgres_db:5432/mercado_bitcoin"

engine = create_engine(
    url=DATABASE_URL, pool_size=5, max_overflow=10, pool_pre_ping=True
)
