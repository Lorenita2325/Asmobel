from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import os
import mysql.connector
from mysql.connector import Error

load_dotenv()

st.title("Subida de Datos de Asmobel")

uploaded_file_1 = st.file_uploader("Sube el archivo Excel con datos de productores", type=["xls", "xlsx"])
uploaded_file_2 = st.file_uploader("Sube el archivo Excel con datos de ventas", type=["xls", "xlsx"])

def extract_data_from_excel(excel_file):
    """Extrae datos de un archivo Excel y los retorna como DataFrame."""
    try:
        df = pd.read_excel(excel_file, engine="openpyxl")
        st.write(df) 
        return df
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
        return pd.DataFrame() 

def insert_productores_in_bulk_local(df, table_name='productores'):
    """Inserta los datos de productores en la base de datos de forma masiva."""
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            cursor = connection.cursor()

            insert_query = f"""
            INSERT INTO {table_name} (id, nombre, dirección, teléfono, correo, fecha_ingreso, area_cultivo, tipo_cultivo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            productores_data = df.to_records(index=False).tolist()

            cursor.executemany(insert_query, productores_data)
            connection.commit()

            st.success(f"{cursor.rowcount} productores insertados exitosamente.")

    except Error as e:
        st.error(f"Error al insertar productores: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

def get_all_sales():
    """Obtiene todas las ventas desde la base de datos."""
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    sales = []

    if connection.is_connected():
        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    id_venta, 
                    id_productor, 
                    fecha_venta, 
                    cantidad_kilos, 
                    precio_por_kilo, 
                    total_venta 
                FROM ventas;
            """
            cursor.execute(query)
            sales = cursor.fetchall()
            print(sales)
        except Error as e:
            print(f"Error while getting sales from database: {e}")
        finally:
            cursor.close()
            connection.close()
            return sales
        
def extract_producers_from_excel(excel_file):
    try:
        df = pd.read_excel(excel_file, sheet_name='Productores')
    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return []

    st.write("Productores:")
    st.write(df)

def extract_sales_from_excel(excel_file):
    try:
        df = pd.read_excel(excel_file, sheet_name='Ventas')
    except Exception as e:
        st.write(f"Error reading the Excel file: {e}")
        return []
    
    st.write("Ventas:")
    st.write(df)

if uploaded_file_1 is not None:
    st.subheader("Datos de Productores")
    
    producer_data = extract_data_from_excel(uploaded_file_1)
    
    if not producer_data.empty:
        st.success("Datos de productores cargados exitosamente.")
        insert_productores_in_bulk_local(producer_data)
    else:
        st.error("El archivo de productores no contiene datos o no pudo ser leído.")

if uploaded_file_2 is not None:
    st.subheader("Datos de Ventas")
    
    sales_data = extract_data_from_excel(uploaded_file_2)
    
    if not sales_data.empty:
        st.success("Datos de ventas cargados exitosamente.")
    else:
        st.error("El archivo de ventas no contiene datos o no pudo ser leído.")

if uploaded_file_1 is not None and uploaded_file_2 is not None:
    if not producer_data.empty and not sales_data.empty:
        st.subheader("Datos Combinados")
        
        combined_data = pd.merge(sales_data, producer_data, on="id_productor", how="inner")
        
        if not combined_data.empty:
            st.write(combined_data)
            st.success("Datos combinados correctamente.")
        else:
            st.error("No se pudo combinar los datos. Asegúrate de que ambas tablas tienen una columna 'id_productor' en común.")
