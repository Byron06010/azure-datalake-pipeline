import os
from io import BytesIO
from dotenv import load_dotenv
import pandas as pd
from azure.storage.blob import BlobServiceClient

load_dotenv()
connection_string = os.getenv("AZURE_CONNECTION_STRING")

CONTAINER_BRONZE = "bronze"
CONTAINER_SILVER = "silver"

def transform_bronze_to_silver():
    print("\n--- INICIANDO CAPA SILVER (VENTAS DE AUTOS) ---")
    
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # 1. Leer desde Bronze
        bronze_blob_path = "raw/car_sales.csv"
        print(f"Leyendo '{bronze_blob_path}' desde el contenedor '{CONTAINER_BRONZE}'...")
        
        container_client_bronze = blob_service_client.get_container_client(CONTAINER_BRONZE)
        blob_client = container_client_bronze.get_blob_client(bronze_blob_path)
        
        stream = blob_client.download_blob()
        df_bronze = pd.read_csv(BytesIO(stream.readall()))
        
        # 2. Transformar y limpiar datos
        print("Transformando datos (estandarizando columnas y agregando timestamp)...")
        # Estandarizar nombres de columnas a minúsculas y sin espacios para evitar errores
        df_bronze.columns = [col.strip().lower().replace(" ", "_") for col in df_bronze.columns]
        
        df_silver = df_bronze.dropna()
        df_silver["processed_at"] = pd.Timestamp.utcnow()

        # 3. Guardar como Parquet en Silver
        silver_blob_path = "cleaned/car_sales/data.parquet"
        print(f"Escribiendo datos limpios hacia el contenedor '{CONTAINER_SILVER}/{silver_blob_path}'...")
        
        parquet_buffer = BytesIO()
        df_silver.to_parquet(parquet_buffer, engine="pyarrow", index=False)
        parquet_buffer.seek(0)
        
        container_client_silver = blob_service_client.get_container_client(CONTAINER_SILVER)
        if not container_client_silver.exists():
            container_client_silver.create_container()
            
        silver_blob_client = container_client_silver.get_blob_client(silver_blob_path)
        silver_blob_client.upload_blob(parquet_buffer, overwrite=True)

        print("¡Éxito total! Datos de autos procesados y guardados en la capa Silver.")

    except Exception as e:
        print(f"Ocurrió un error en la transformación Silver: {e}")

if __name__ == "__main__":
    transform_bronze_to_silver()