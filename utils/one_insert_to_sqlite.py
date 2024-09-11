import sqlite3
import time
from datetime import datetime
import random

# Configuraciones
db_path = '../Database.db'  # Ruta a la base de datos SQLite
interval = 300  # Intervalo de tiempo en segundos para insertar nuevos registros

# Función para insertar registros en la base de datos SQLite
def insert_query(query):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("Registro insertado correctamente.")
    except sqlite3.Error as e:
        print(f"Ocurrió un error al insertar el registro: {e}")
    finally:
        conn.close()

# Bucle para insertar registros simulados periódicamente
while True:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generar valores aleatorios para las columnas
    latitud = f"{random.randint(44, 90)}°{random.uniform(0, 59.9999):.4f}'' S"
    longitud = f"{random.randint(0, 90)}°{random.uniform(0, 59.9999):.4f}'' W"
    buque_semi_popa = random.randint(0, 1)
    buque_close_popa = random.randint(0, 1)
    buque_semi_proa = random.randint(0, 1)
    buque_close_proa = random.randint(0, 1)
    dosis_popa = random.randint(0, 100)
    dosis_proa = random.randint(0, 100)
    o2_up_proa = round(random.uniform(8.0, 10.0), 1)
    o2_med_proa = round(random.uniform(8.0, 10.0), 1)
    o2_low_proa = round(random.uniform(8.0, 10.0), 1)
    ph_bod_proa = round(random.uniform(6.5, 7.5), 2)
    ph_est_co2_proa = round(random.uniform(6.5, 7.5), 2)
    temp_proa = round(random.uniform(10.0, 12.0), 1)
    flujo_proa = random.randint(0, 100)
    uvt_proa = random.randint(0, 100)
    orp_proa = random.randint(0, 100)
    co2_proa = round(random.uniform(9.0, 10.0), 2)
    rpm_m4 = random.randint(0, 1000)
    rpm_m5 = random.randint(0, 1000)
    rpm_m6 = random.randint(0, 1000)
    presión_aire = round(random.uniform(1.0, 2.0), 2)

    query = f"""
    INSERT INTO DataLogger1 (Time, Latitud, Longitud, Buque_Semi_Popa, Buque_Close_Popa, Buque_Semi_Proa, Buque_Close_Proa, Dosis_Popa, Dosis_Proa, O2_Up_Proa, O2_Med_Proa, O2_Low_Proa, pH_Bod_Proa, pH_Est_CO2_Proa, Temp_Proa, Flujo_Proa, UVT_Proa, ORP_Proa, CO2_Proa, Rpm_M4, Rpm_M5, Rpm_M6, Presión_Aire) 
    VALUES ('{current_time}', '{latitud}', '{longitud}', {buque_semi_popa}, {buque_close_popa}, {buque_semi_proa}, {buque_close_proa}, {dosis_popa}, {dosis_proa}, {o2_up_proa}, {o2_med_proa}, {o2_low_proa}, {ph_bod_proa}, {ph_est_co2_proa}, {temp_proa}, {flujo_proa}, {uvt_proa}, {orp_proa}, {co2_proa}, {rpm_m4}, {rpm_m5}, {rpm_m6}, {presión_aire})
    """

    print(f"Executing query: {query}")
    insert_query(query)
    time.sleep(interval)


