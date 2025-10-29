import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# --- Configuración Inicial ---
# Definir rutas de carpetas
data_dir = Path('data')
output_dir = Path('output')
output_dir.mkdir(exist_ok=True) # Asegurarse de que el directorio de salida exista

# Definir las marcas de interés para cada empresa
marcas_jorle = [
    'DENISON', 'EATON', 'CHAR-LYNN', 'BRAND', 'GRESEN', 'SUN', 'HIDRAULIC',
    'PULLMASTER', 'SAI', 'CHAR LYNN', 'EATON VICKERS', 'DELTA', 'KOBELT TECHNOLOGIES',
    'EATON CHAR LYNN', 'HATTELAND', 'KOCSIS', 'PARKER VICKERS', 'MARCO', 'MARION',
    'KYB', 'VICKERS/DANFOS', 'BRAND HYDRAULICS', 'VELJAN'
]
marcas_import360 = [
    'VELJAN', 'REXNORD', 'CHARLYN', 'REINTJES', 'SAI', 'Pullmaster', 'TULSA',
    'METARIS', 'VULKAN', 'INTERMOT', 'CHAR LYNN', 'CHARLYNN', 'DANFOSS',
    'REXROTH', 'KOCSIS'
]
# Temporada de pesca actualizada: Nov-Ene y Abr-Jun
temporada_pesca_meses = [11, 12, 1, 4, 5, 6]

# --- Función Principal de Análisis por Empresa ---
def analizar_empresa(archivo_excel, marcas, nombre_empresa):
    """
    Realiza un análisis completo para una empresa: carga datos, genera resúmenes,
    tablas y visualizaciones.
    """
    # 1. Cargar y limpiar datos
    df = pd.read_excel(data_dir / archivo_excel)
    df['FECHA'] = pd.to_datetime(df['AÑO'].astype(str) + '-' + df['MES'].astype(str) + '-' + df['DIA'].astype(str), errors='coerce')
    df.dropna(subset=['FECHA', 'MARCA', 'MODELO', 'US$ CIF', 'CANTIDAD COMERCIAL'], inplace=True)
    df_filtrado = df[df['MARCA'].str.upper().isin([m.upper() for m in marcas])].copy()

    # 2. Crear y guardar el resumen agregado mensual
    df_filtrado['month_year'] = df_filtrado['FECHA'].dt.to_period('M')
    columnas_agg = ['month_year', 'MARCA', 'MODELO', 'MERCANCÍA', 'UNIDAD COMERCIAL']
    df_agg = df_filtrado.groupby(columnas_agg).agg({
        'US$ CIF': 'sum',
        'CANTIDAD COMERCIAL': 'sum'
    }).reset_index()
    df_agg.to_csv(output_dir / f'{nombre_empresa}_resumen_mensual.csv', index=False)

    # 3. Generar Nuevos Gráficos
    # Gráfico de barras de Marcas por Valor CIF
    plt.figure(figsize=(12, 8))
    df_filtrado.groupby('MARCA')['US$ CIF'].sum().sort_values(ascending=False).plot(kind='bar', color='skyblue')
    plt.title(f'Valor Total de Importación (US$ CIF) por Marca - {nombre_empresa}')
    plt.ylabel('Total US$ CIF')
    plt.xlabel('Marca')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_dir / f'{nombre_empresa}_marcas_por_valor.png')
    plt.close()

    # Gráfico de Temporadas de Pesca por Cantidad Comercial
    df_temporal = df_filtrado.groupby('month_year')['CANTIDAD COMERCIAL'].sum()
    df_temporal.index = df_temporal.index.strftime('%Y-%m')
    colores = ['red' if pd.to_datetime(i).month in temporada_pesca_meses else 'blue' for i in df_temporal.index]
    plt.figure(figsize=(15, 7))
    df_temporal.plot(kind='bar', color=colores)
    plt.title(f'Cantidad Comercial Mensual y Temporadas de Pesca - {nombre_empresa}')
    plt.ylabel('Total Cantidad Comercial')
    plt.xlabel('Mes-Año')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_dir / f'{nombre_empresa}_cantidad_temporada.png')
    plt.close()

    # Mapa de Calor por Cantidad Comercial
    heatmap_data = df_filtrado.groupby([df_filtrado['FECHA'].dt.month, 'MARCA'])['CANTIDAD COMERCIAL'].sum().unstack(fill_value=0)
    plt.figure(figsize=(18, 10))
    sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt='.0f')
    plt.title(f'Cantidad Comercial por Marca y Mes - {nombre_empresa}')
    plt.ylabel('Mes')
    plt.xlabel('Marca')
    plt.tight_layout()
    plt.savefig(output_dir / f'{nombre_empresa}_heatmap_cantidad.png')
    plt.close()

    # 4. Generar Tablas de Análisis
    # Tabla de productos con estacionalidad
    df_pesca = df_filtrado[df_filtrado['FECHA'].dt.month.isin(temporada_pesca_meses)]
    productos_estacionales = df_pesca.groupby('MODELO').agg({
        'CANTIDAD COMERCIAL': 'sum',
        'US$ CIF': 'sum'
    }).sort_values(by='CANTIDAD COMERCIAL', ascending=False).head(15)
    productos_estacionales.to_csv(output_dir / f'{nombre_empresa}_productos_estacionales.csv')

    # Tabla de productos importados en los últimos 3 meses
    fecha_maxima = df_filtrado['FECHA'].max()
    tres_meses_atras = fecha_maxima - pd.DateOffset(months=3)
    df_recientes = df_filtrado[df_filtrado['FECHA'] >= tres_meses_atras]
    columnas_recientes = ['FECHA', 'MARCA', 'MODELO', 'MERCANCÍA', 'US$ CIF', 'CANTIDAD COMERCIAL', 'UNIDAD COMERCIAL']
    df_recientes[columnas_recientes].sort_values(by='FECHA', ascending=False).to_csv(output_dir / f'{nombre_empresa}_productos_recientes.csv', index=False)

    print(f"Análisis para {nombre_empresa} completado.")

# --- Ejecución del Análisis ---
analizar_empresa('jorle.xlsx', marcas_jorle, 'Jorle')
analizar_empresa('IMPORT360.xlsx', marcas_import360, 'IMPORT360')

print("Todos los análisis han sido generados en la carpeta 'output'.")
