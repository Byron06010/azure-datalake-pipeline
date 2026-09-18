import os
from io import BytesIO
from dotenv import load_dotenv
import pandas as pd
from azure.storage.blob import BlobServiceClient

load_dotenv()
connection_string = os.getenv("AZURE_CONNECTION_STRING")

CONTAINER_SILVER = "silver"
CONTAINER_GOLD = "gold"

def transform_silver_to_gold():
    print("\n--- INICIANDO CAPA GOLD (DATOS COMPLETOS DE AUTOS) ---")
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # 1. Leer desde Silver
        silver_blob_path = "cleaned/car_sales/data.parquet"
        print(f"Leyendo '{silver_blob_path}' desde el contenedor '{CONTAINER_SILVER}'...")
        
        container_client_silver = blob_service_client.get_container_client(CONTAINER_SILVER)
        blob_client = container_client_silver.get_blob_client(silver_blob_path)
        
        stream = blob_client.download_blob()
        df_silver = pd.read_parquet(BytesIO(stream.readall()))
        
        # 2. Enriquecer datos sin perder registros
        print("Procesando dataset completo y calculando métricas de ventas...")
        df_gold = df_silver.copy()
        
        # Asegurar que las columnas numéricas sean realmente números (convirtiendo errores a NaN por si hay letras)
        if "sales_in_thousands" in df_gold.columns:
            df_gold["sales_in_thousands"] = pd.to_numeric(df_gold["sales_in_thousands"], errors="coerce")
            
        if "price_in_thousands" in df_gold.columns:
            df_gold["price_in_thousands"] = pd.to_numeric(df_gold["price_in_thousands"], errors="coerce")

        # Calcular el total de ventas monetarias si ambas columnas existen
        if "sales_in_thousands" in df_gold.columns and "price_in_thousands" in df_gold.columns:
            df_gold["total_revenue_thousands"] = df_gold["sales_in_thousands"] * df_gold["price_in_thousands"]
        
        # Agregar marca de tiempo del reporte
        df_gold["report_generated_at"] = pd.Timestamp.utcnow()

        # 3. Guardar el dataset completo y enriquecido en Gold
        gold_blob_path = "aggregated/car_sales_enriched.csv"
        print(f"Escribiendo dataset completo hacia el contenedor '{CONTAINER_GOLD}/{gold_blob_path}'...")
        
        csv_buffer = BytesIO()
        df_gold.to_csv(csv_buffer, index=False, encoding="utf-8")
        csv_buffer.seek(0)
        
        container_client_gold = blob_service_client.get_container_client(CONTAINER_GOLD)
        if not container_client_gold.exists():
            container_client_gold.create_container()
            
        gold_blob_client = container_client_gold.get_blob_client(gold_blob_path)
        gold_blob_client.upload_blob(csv_buffer, overwrite=True)

        print(f"¡Éxito total! Se guardaron {len(df_gold)} registros completos listos para Power BI en la capa Gold.")

    except Exception as e:
        print(f"Ocurrió un error en la capa Gold: {e}")

if __name__ == "__main__":
    transform_silver_to_gold()