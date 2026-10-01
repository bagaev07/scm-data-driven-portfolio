import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Настройки подключения к вашей PostgreSQL (измените под свои данные)
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'postgres' # Укажите ваш пароль
PORT = '5432'
DB_NAME = 'scm_portfolio'

engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

# Генерируем данные по периодам (2025-2026 годы)
periods = pd.date_range(start='2025-01-01', end='2026-06-01', freq='MS').strftime('%Y-%m').tolist()

np.random.seed(42)

# 1. Таблица выручки и себестоимости (Revenue & COGS)
df_finance = pd.DataFrame({
    'period': periods,
    'revenue': np.random.randint(120_000_000, 180_000_000, size=len(periods)),
    'cogs': np.random.randint(80_000_000, 115_000_000, size=len(periods))
})

# 2. Таблица оборотных активов (Current Assets)
df_current_assets = pd.DataFrame({
    'period': np.repeat(periods, 3),
    'asset_type': ['Inventory', 'Accounts Receivable', 'Cash'] * len(periods),
    'value': np.random.randint(15_000_000, 45_000_000, size=len(periods)*3)
})

# 3. Таблица внеоборотных активов цепи поставок (SC Fixed Assets: склады, траки, софт)
df_fixed_assets = pd.DataFrame({
    'period': periods,
    'warehouse_value': np.random.randint(50_000_000, 55_000_000, size=len(periods)),
    'fleet_value': np.random.randint(30_000_000, 35_000_000, size=len(periods)),
    'it_systems_value': np.random.randint(10_000_000, 12_000_000, size=len(periods))
})

# Экспорт в PostgreSQL
df_finance.to_sql('sc_finance_performance', engine, if_exists='replace', index=False)
df_current_assets.to_sql('sc_current_assets', engine, if_exists='replace', index=False)
df_fixed_assets.to_sql('sc_fixed_assets', engine, if_exists='replace', index=False)

print("✅ Тестовый полигон SCOR Asset Management успешно развернут в PostgreSQL!")
