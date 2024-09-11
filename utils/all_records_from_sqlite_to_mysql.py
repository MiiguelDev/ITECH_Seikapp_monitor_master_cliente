import sqlite3
import os

# Ruta de la base de datos SQLite y archivo de salida
DB_PATH = '../Database.db'
OUTPUT_SQL_FILE = 'output_mysql.sql'

# Función para obtener todas las tablas de la base de datos SQLite
def get_tables(db_path):
    if not os.path.exists(db_path):
        print(f"Error: No se encontró el archivo de la base de datos en {db_path}")
        return []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al leer la base de datos: {e}")
        tables = []
    finally:
        conn.close()

    return [table[0] for table in tables]

# Función para leer la estructura y datos de una tabla
def read_table(db_path, table_name):
    if not os.path.exists(db_path):
        print(f"Error: No se encontró el archivo de la base de datos en {db_path}")
        return None, []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns_info = cursor.fetchall()

        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al leer la tabla {table_name}: {e}")
        columns_info = []
        records = []
    finally:
        conn.close()

    return columns_info, records

# Función para formatear la estructura de la tabla en MySQL
def format_create_table(table_name, columns_info):
    if not columns_info:
        return ""

    create_query = "CREATE TABLE IF NOT EXISTS `{}` (\n".format(table_name)
    columns_definitions = []

    for column in columns_info:
        col_name = column[1]
        col_type = column[2].upper().replace("NVARCHAR", "VARCHAR").replace("INTEGER", "INT")
        col_notnull = " NOT NULL" if column[3] else ""
        col_primary = " PRIMARY KEY" if column[5] else ""
        columns_definitions.append("`{}` {}{}{}".format(col_name, col_type, col_notnull, col_primary))

    create_query += ",\n".join(columns_definitions) + "\n);"
    return create_query

# Función para formatear los valores de inserción en MySQL
def format_insert_records(table_name, columns_info, records):
    if not records:
        return ""

    column_names = [col[1] for col in columns_info]
    insert_query = "INSERT INTO `{}` ({}) VALUES\n".format(
        table_name, ', '.join("`{}`".format(col) for col in column_names)
    )
    values_list = []

    for record in records:
        formatted_values = ', '.join(
            "'{}'".format(str(value).replace("'", "''")) if isinstance(value, str) else "NULL" if value is None else str(value)
            for value in record
        )
        values_list.append("({})".format(formatted_values))
    
    insert_query += ',\n'.join(values_list) + ";"
    return insert_query

# Función para guardar la consulta SQL en un archivo
def save_to_sql(output_file, sql_content):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sql_content)
        print(f"Archivo SQL guardado en {output_file}")
    except IOError as e:
        print(f"Error al guardar el archivo SQL: {e}")

# Función principal que coordina la lectura y conversión de la base de datos
def main():
    tables = get_tables(DB_PATH)
    sql_content = "BEGIN TRANSACTION;\n"

    for table in tables:
        columns_info, records = read_table(DB_PATH, table)
        create_table_query = format_create_table(table, columns_info)
        insert_records_query = format_insert_records(table, columns_info, records)

        sql_content += f"{create_table_query}\n\n"
        if insert_records_query:
            sql_content += f"{insert_records_query}\n\n"

    sql_content += "COMMIT;\n"
    save_to_sql(OUTPUT_SQL_FILE, sql_content)

if __name__ == "__main__":
    main()
