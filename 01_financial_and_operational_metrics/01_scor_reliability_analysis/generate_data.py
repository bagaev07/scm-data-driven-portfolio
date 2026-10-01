import pandas as pd
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'postgres'
PORT = '5432'
DATABASE = 'scm_portfolio'

engine = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

random.seed(100)
records_count = 500
start_date = datetime(2026,1,1)

data = []
for i in range(1, records_count + 1):
    order_id = f'ORD-2026-{i:04d}'
    order_date = start_date + timedelta(days=random.randint(0, 59))

    is_in_full = 1 if random.random() < 0.92 else 0
    is_in_time = 1 if random.random() < 0.88 else 0
    is_doc_accurate = 1 if random.random() < 0.95 else 0
    is_perfect_condition = 1 if random.random() < 0.96 else 0

    client_segment = random.choice(['Key Account (KA)','Retail Chains', 'Distributors'])

    data.append((
        order_id,
        order_date.strftime('%Y-%m-%d'),
        client_segment,
        is_in_full,
        is_in_time,
        is_doc_accurate,
        is_perfect_condition
    ))

df = pd.DataFrame(data, columns=[
    'order_id', 'order_date', 'client_segment',
    'is_in_full', 'is_on_time','is_doc_accurate', 'is_perfect_condition'
])

table_name = 'scor_orders_log'
df.to_sql(table_name, engine, if_exists='replace', index=False)

print(f'Успех! Таблица {table_name} создана в PostgreSQL и заполнена {records_count} записями.')