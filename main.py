from bronze_ingestion import ingest_to_bronze
from silver_transformation import transform_bronze_to_silver
from gold_aggregation import transform_silver_to_gold

if __name__ == "__main__":
    print("=== INICIANDO PIPELINE COMPLETO MEDALLÓN ===")
    
    # Paso 1: Ingesta (Crudos)
    ingest_to_bronze()
    
    # Paso 2: Transformación (Limpieza)
    transform_bronze_to_silver()
    
    # Paso 3: Agregación (Negocio / Reportes)
    transform_silver_to_gold()
    
    print("=== PIPELINE FINALIZADO CON ÉXITO ===")