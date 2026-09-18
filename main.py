import os
import requests
from dotenv import load_dotenv
from azure.storage.filedatalake import DataLakeServiceClient

# Cargar las variables de entorno desde el archivo .env local
load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = "bronze"

def ingest_file_to_bronze():
    try:
        # 1. URL de un archivo CSV público de ejemplo (puedes cambiarlo por el que prefieras)
        file_url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
        local_file_name = "iris.csv"
        
        print(f"Descargando archivo desde {file_url}...")
        response = requests.get(file_url)
        response.raise_for_status() # Lanza un error si falla la descarga
        
        # Guardar temporalmente el archivo de forma local
        with open(local_file_name, "wb") as f:
            f.write(response.content)
        print(f"Archivo guardado localmente como '{local_file_name}'.")

        # 2. Conectar a Azure Data Lake
        service_client = DataLakeServiceClient.from_connection_string(CONNECTION_STRING)
        file_system_client = service_client.get_file_system_client(CONTAINER_NAME)
        
        # 3. Definir la ruta donde se guardará dentro del Data Lake (Capa Bronze)
        remote_file_path = "raw/iris.csv"
        file_client = file_system_client.get_file_client(remote_file_path)
        
        # 4. Subir el archivo a Azure
        with open(local_file_name, "rb") as local_file:
            file_client.upload_data(local_file.read(), overwrite=True)
            
        print(f"¡Éxito! Archivo subido correctamente a Azure en: {CONTAINER_NAME}/{remote_file_path}")

    except Exception as e:
        print(f"Ocurrió un error en el proceso de ingesta: {e}")

if __name__ == "__main__":
    ingest_file_to_bronze()