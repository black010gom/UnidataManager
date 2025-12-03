import pandas as pd
import sqlite3

def convert_csv_to_xlsx(csv_file, xlsx_file):
    df = pd.read_csv(csv_file)
    df.to_excel(xlsx_file, index=False)

def convert_xlsx_to_json(xlsx_file, json_file):
    df = pd.read_excel(xlsx_file)
    df.to_json(json_file, orient="records")

def convert_json_to_sqlite(json_file, sqlite_file, table_name="table1"):
    df = pd.read_json(json_file)
    conn = sqlite3.connect(sqlite_file)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def convert_sqlite_to_csv(sqlite_file, table_name, csv_file):
    conn = sqlite3.connect(sqlite_file)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    df.to_csv(csv_file, index=False)
    conn.close()

# 통합 변환 함수
def convert_file(input_file, output_file, table_name=None):
    input_ext = input_file.split(".")[-1].lower()
    output_ext = output_file.split(".")[-1].lower()

    if input_ext == "csv" and output_ext == "xlsx":
        convert_csv_to_xlsx(input_file, output_file)
    elif input_ext == "xlsx" and output_ext == "json":
        convert_xlsx_to_json(input_file, output_file)
    elif input_ext == "json" and output_ext == "sqlite":
        convert_json_to_sqlite(input_file, output_file)
    elif input_ext == "sqlite" and output_ext == "csv":
        if table_name is None:
            raise ValueError("table_name must be provided for SQLite to CSV conversion")
        convert_sqlite_to_csv(input_file, table_name, output_file)
    else:
        raise ValueError("Unsupported conversion types")
    
# 예시 사용법
# convert_file("data.csv", "data.xlsx").astype(int).tolist()
# arr = (ctypes.c_int * len(scores))(*scores)