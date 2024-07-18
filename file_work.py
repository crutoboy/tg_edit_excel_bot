import sqlite3
import openpyxl as xl
from config import EXCEL_PATH, SQL_PATH, SQL_TABLE_NAME


def shielding(string: str) -> str:
    '''функция для добавления двойных 
    кавычек для экранирования строки'''
    string = str(string)
    out = '"' + string + '"'
    return out

def excel_to_sql():
    file = xl.load_workbook(EXCEL_PATH, read_only=True)
    worksheet = file.worksheets[0]

    rows = list(worksheet.rows)
    header = rows[0]
    data = rows[1:]

    conn = sqlite3.connect(SQL_PATH)
    cursor = conn.cursor()

    columns = range(len(header))
    columns_shielding = map(shielding, map(str, columns))
    columns_str = ", ".join(columns_shielding)

    cursor.execute(f'DROP TABLE IF EXISTS {SQL_TABLE_NAME}')
    cursor.execute(f'CREATE TABLE {SQL_TABLE_NAME} (type, {columns_str})')

    header_sql = [cell.value for cell in header]
    header_shielding = map(shielding, header_sql)
    header_str = ", ".join(header_shielding)
    cursor.execute(f'INSERT INTO {SQL_TABLE_NAME} (type, {columns_str}) VALUES ("header", {header_str})')

    for row in data:
        values = [cell.value for cell in row]
        values_shielding = map(shielding, values)
        values_str = ", ".join(values_shielding)
        cursor.execute(f'INSERT INTO {SQL_TABLE_NAME} ({columns_str}) VALUES ({values_str})')

    conn.commit()
    conn.close()

def sql_to_excel():
    conn = sqlite3.connect(SQL_PATH)
    cursor = conn.cursor()

    workbook = xl.Workbook()
    worksheet = workbook.active

    cursor.execute(f'SELECT * FROM {SQL_TABLE_NAME}')
    rows = cursor.fetchall()

    for row in rows:
        worksheet.append(row[1:])

    workbook.save(EXCEL_PATH)
    conn.close()

def get_header():
    conn = sqlite3.connect(SQL_PATH)
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM {SQL_TABLE_NAME} WHERE type = ?', 'header')
    header = cursor.fetchone()

    conn.close()

    return header[1:]

def filters_rows(filters: list):
    conn = sqlite3.connect(SQL_PATH)
    cursor = conn.cursor()

    filters = [filter for filter in filters if filter is not None]
    filters_shielding = map(shielding, filters)
    filters_str = " AND ".join(filters_shielding)

    cursor.execute(f'SELECT * FROM {SQL_TABLE_NAME} WHERE type != ? AND {filters_str}', 'header')
    rows = cursor.fetchall()
    conn.close()

    return rows

def count_select_filter_rows(filters: list) -> int:
    conn = sqlite3.connect(SQL_PATH)
    cursor = conn.cursor()

    filters = [filter for filter in filters if filter is not None]
    filters_shielding = map(shielding, filters)
    filters_str = " AND ".join(filters_shielding)
# всё не правильно. надо через for и enumerate
    cursor.execute(f'SELECT COUNT(*) FROM {SQL_TABLE_NAME} WHERE type != ? AND {filters_str}', 'header')
    count = cursor.fetchone()[0]
    conn.close()

    return int(count)

# excel_to_sql()
# sql_to_excel()