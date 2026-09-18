import os
from azure.storage.filedatalake import DataLakeServiceClient

# Reemplaza esto con tu cadena de conexión o guárdala de forma segura
# (Puedes obtenerla en Azure Portal > Tu cuenta de almacenamiento > Claves de acceso)
CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = "bronze"

def test_azure_connection():
    try:
        # Crear el cliente del servicio Data Lake
        service_client = DataLakeServiceClient.from_connection_string(CONNECTION_STRING)
        
        # Obtener el cliente del contenedor 'bronze' usando el método correcto para Data Lake Gen2
        container_client = service_client.get_file_system_client(CONTAINER_NAME)
        
        print(f"¡Conexión exitosa a Azure Data Lake!")
        print(f"Contenedor '{CONTAINER_NAME}' verificado correctamente.")
        
    except Exception as e:
        print(f"Ocurrió un error al conectar con Azure: {e}")
if __name__ == "__main__":
    test_azure_connection()