import sqlite3
import requests
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Variables del archivo .env
SERVER_URL = os.getenv('SERVER_URL')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
DB_PATH = os.getenv('DB_PATH')
TABLE_NAME = os.getenv('TABLE_NAME')
DATE_COLUMN = os.getenv('DATE_COLUMN')

def get_last_synced_id():
    try:
        with open('last_synced_id.txt', 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0

def update_last_synced_id(last_id):
    with open('last_synced_id.txt', 'w') as f:
        f.write(str(last_id))

def get_records_after_last_id(db_path, table_name, last_synced_id, date_column):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        query = f"SELECT * FROM {table_name} WHERE Id > ? ORDER BY {date_column} ASC"
        cursor.execute(query, (last_synced_id,))
        records = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        records = []
        column_names = []
    finally:
        conn.close()

    return records, column_names

def format_sql_insert_query(table_name, column_names, records):
    if not records:
        return ""

    query = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in column_names])}) VALUES\n"
    values_list = []
    for record in records:
        formatted_values = ', '.join([f"'{str(value).replace('\'', '\'\'')}'" if isinstance(value, str) else 'NULL' if value is None else str(value) for value in record])
        values_list.append(f"({formatted_values})")
    query += ',\n'.join(values_list) + ";"
    return query

def send_to_server(query):
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {'query': query}

    try:
        response = requests.post(SERVER_URL, headers=headers, json=data)
        if response.status_code == 200:
            print("Datos enviados correctamente.")
        else:
            print(f"Error al enviar los datos: {response.status_code} - {response.text}")
    except requests.RequestException as e:
        print(f"Error de conexión: {e}")

def main():
    last_synced_id = get_last_synced_id()

    # Obtener los registros desde SQLite después del último ID sincronizado
    records, column_names = get_records_after_last_id(DB_PATH, TABLE_NAME, last_synced_id, DATE_COLUMN)

    if records:
        query = format_sql_insert_query(TABLE_NAME, column_names, records)
        print(f"Enviando la siguiente consulta: {query}")

        # Enviar la consulta al servidor Laravel
        send_to_server(query)

        # Actualizar el último ID sincronizado
        update_last_synced_id(records[-1][0])

    else:
        print("No hay registros nuevos para procesar.")

if __name__ == "__main__":
    main()


