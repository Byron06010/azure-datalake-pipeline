# 🚗 Azure Medallón Data Pipeline & Automotive BI

Pipeline de ingeniería de datos de grado empresarial implementado bajo la **Arquitectura Medallón (Bronze, Silver, Gold)** utilizando **Azure Data Lake Storage Gen2** y **Python**, integrado con un dashboard analítico de nivel ejecutivo en **Power BI**.

---

## 🛠️ Tecnologías y Herramientas Utilizadas

* **Lenguaje:** Python 3.10+
* **Almacenamiento en la Nube:** Azure Data Lake Storage (ADLS) Gen2 (Contenedores: `bronze`, `silver`, `gold`)
* **Librerías de Procesamiento y Azure:** `pandas`, `pyarrow`, `azure-storage-blob`, `python-dotenv`
* **Visualización y BI:** Power BI Desktop (Modelado dimensional, Power Query y diseño de KPIs corporativos)
* **Control de Versiones:** Git y GitHub

---

## 🏗️ Arquitectura del Proyecto (Flujo Medallón)

El flujo de datos está estructurado en tres capas principales para garantizar la calidad, trazabilidad y optimización del negocio:

1. **Capa Bronze (Raw):** Ingesta automática del archivo crudo de ventas de vehículos (`Car_sales.csv`) directamente desde el repositorio fuente hacia el contenedor `bronze` en Azure sin alteraciones estructurales.
2. **Capa Silver (Cleaned):** Lectura de los datos crudos, estandarización y limpieza de nombres de columnas, eliminación de registros vacíos críticos, tipado correcto de datos y almacenamiento optimizado en formato columnar **Parquet** dentro del contenedor `silver`.
3. **Capa Gold (Enriched/Aggregated):** Procesamiento de negocio avanzado, limpieza de anomalías numéricas, cálculo de métricas financieras clave (como ingresos totales por modelo/marca) y persistencia final en formato estructurado listo para consumo analítico en el contenedor `gold`.

---

## ⚙️ Configuración e Inicio del Servidor / Pipeline

Sigue estos pasos para configurar tu entorno local y ejecutar el pipeline completo de extremo a extremo:

### 1. Clonar el repositorio y preparar el entorno virtual
Abre tu terminal (PowerShell o CMD) en la ruta de tu proyecto y ejecuta:

```bash
# Crear entorno virtual
python -m venv venv

# Activar el entorno virtual (Windows)
.\venv\Scripts\Activate

# Instalar dependencias necesarias
pip install pandas pyarrow azure-storage-blob python-dotenv
