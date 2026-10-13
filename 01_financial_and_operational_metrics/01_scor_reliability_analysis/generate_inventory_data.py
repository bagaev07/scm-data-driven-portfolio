import pandas as pd
import numpy as np
import random
from sqlalchemy import create_engine

# НАСТРОЙКА ПОДКЛЮЧЕНИЯ К POSTGRESQL (Укажи свой пароль)
engine = create_engine("postgresql+psycopg2://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/scm_portfolio")

random.seed(42)
np.random.seed(42)
records_count = 1000

# Структура сырья Mars Казахстан (Нормативный Lead Time, изменчивость и средний спрос)
materials = {
    'RM-001-Cocoa': {'vendor': 'Ghana Cocoa Corp', 'target_lt': 45, 'std_lt': 7, 'demand_mu': 200},
    'RM-002-Sugar': {'vendor': 'CentralAsia Sugar', 'target_lt': 12, 'std_lt': 2, 'demand_mu': 650},
    'PM-003-Film': {'vendor': 'China Pack Ltd', 'target_lt': 25, 'std_lt': 5, 'demand_mu': 120},
    'RM-004-Milk': {'vendor': 'Almaty Dairy LLC', 'target_lt': 4, 'std_lt': 1, 'demand_mu': 800}
}

data = []
for i in range(1, records_count + 1):
    sku = random.choice(list(materials.keys()))
    vendor = materials[sku]['vendor']
    target_lt = materials[sku]['target_lt']
    std_lt = materials[sku]['std_lt']
    demand_mu = materials[sku]['demand_mu']
    
    # Симулируем случайные колебания Lead Time и спроса (нормальное распределение)
    actual_lt = max(1, int(np.random.normal(target_lt, std_lt)))
    actual_demand = max(10, int(np.random.normal(demand_mu, demand_mu * 0.1)))
    
    data.append((f"PO-{i:05d}", sku, vendor, actual_lt, actual_demand))

# Загрузка сырых транзакций в Postgres
df = pd.DataFrame(data, columns=['po_id', 'sku_name', 'vendor_name', 'actual_lead_time', 'average_daily_demand'])
df.to_sql('mars_raw_materials_orders', engine, if_exists='replace', index=False)

# Сразу агрегируем данные и выгружаем чистый CSV для твоей работы в Excel
df_agg = df.groupby(['sku_name', 'vendor_name']).agg(
    total_orders=('po_id', 'count'),
    avg_lead_time=('actual_lead_time', 'mean'),
    avg_demand=('average_daily_demand', 'mean'),
    std_dev_lead_time=('actual_lead_time', 'std')
).reset_index()

df_agg.to_csv('mars_aggregated_data.csv', index=False)
print("Успех! База данных в Postgres обновлена. Файл 'mars_aggregated_data.csv' успешно создан для Excel.")
