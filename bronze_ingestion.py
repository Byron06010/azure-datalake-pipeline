import os
import requests
from io import BytesIO
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()
connection_string = os.getenv("AZURE_CONNECTION_STRING")

CONTAINER_BRONZE = "bronze"

def ingest_to_bronze():
    print("\n--- INICIANDO CAPA BRONZE (CAR SALES DESDE GITHUB) ---")
    
    # URL en formato raw para descargar el CSV directamente
    url = "https://raw.githubusercontent.com/Byron06010/csv.example/main/Car_sales.csv"
    
    try:
        print(f"Descargando archivo desde {url}...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Conectar a Azure Blob Storage
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(CONTAINER_BRONZE)
        
        # Crear contenedor bronze si no existe
        if not container_client.exists():
            container_client.create_container()
            print(f"Contenedor '{CONTAINER_BRONZE}' creado en Azure.")
            
        # Subir archivo
        blob_path = "raw/car_sales.csv"
        blob_client = container_client.get_blob_client(blob_path)
        
        print(f"Subiendo archivo a la capa Bronze: {CONTAINER_BRONZE}/{blob_path}")
        blob_client.upload_blob(BytesIO(response.content), overwrite=True)
        
        print("¡Éxito! Archivo de ventas de autos subido correctamente a la capa Bronze.")

    except Exception as e:
        print(f"Ocurrió un error en la capa Bronze: {e}")

if __name__ == "__main__":
    ingest_to_bronze()