import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

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

# Función para cargar y limpiar los datos
def cargar_y_limpiar(archivo, marcas, nombre_empresa):
    df = pd.read_excel(archivo)
    df['FECHA'] = pd.to_datetime(df['AÑO'].astype(str) + '-' + df['MES'].astype(str) + '-' + df['DIA'].astype(str), errors='coerce')
    df_filtrado = df[df['MARCA'].notna() & df['MARCA'].str.upper().isin([m.upper() for m in marcas])].copy()
    df_filtrado['MARCA_NORMALIZADA'] = df_filtrado['MARCA'].str.upper().replace('-', '', regex=False).replace(' ', '', regex=False)
    df_filtrado['EMPRESA'] = nombre_empresa
    return df_filtrado

df_jorle = cargar_y_limpiar('jorle.xlsx', marcas_jorle, 'Jorle')
df_import360 = cargar_y_limpiar('IMPORT360.xlsx', marcas_import360, 'IMPORT360')
df_completo = pd.concat([df_jorle, df_import360], ignore_index=True)
df_completo.dropna(subset=['FECHA'], inplace=True)

# --- Análisis Estadístico Conciso ---
stats_buffer = io.StringIO()
stats_buffer.write("--- Resumen Estadístico (Columnas Relevantes) ---\n")
columnas_relevantes = ['US$ FOB', 'US$ FLETE', 'US$ SEGURO', 'US$ CIF', 'PESO NETO', 'PESO BRUTO', 'CANTIDAD']
df_relevante = df_completo[columnas_relevantes]
stats_buffer.write(df_relevante.describe().to_string())
with open("resumen_estadistico.txt", "w") as f:
    f.write(stats_buffer.getvalue())

# --- Identificar Productos Clave en Temporada de Pesca ---
temporada_pesca = [4, 5, 6, 11, 12]
df_pesca = df_completo[df_completo['FECHA'].dt.month.isin(temporada_pesca)]
productos_top_pesca = df_pesca['MODELO'].value_counts().nlargest(15)
with open("productos_temporada.txt", "w") as f:
    f.write("--- Top 15 Productos (MODELO) en Temporada de Pesca ---\n")
    f.write(productos_top_pesca.to_string())

# --- Función para Generar Gráficos por Empresa ---
def generar_graficos_empresa(df_empresa, sufijo_empresa):
    # 1. Gráfico de tendencia mensual de importaciones por marca
    monthly_brand_data = df_empresa.groupby([df_empresa['FECHA'].dt.to_period('M'), 'MARCA_NORMALIZADA']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(15, 8))
    monthly_brand_data.plot(kind='line', ax=ax)
    ax.set_title(f'Tendencia Mensual de Importaciones por Marca ({sufijo_empresa})')
    ax.legend(title='Marca', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(f'tendencia_mensual_marca_{sufijo_empresa}.png')
    plt.close(fig)

    # 2. Histograma de frecuencia de los 15 productos más importados
    fig, ax = plt.subplots(figsize=(12, 7))
    top_15_modelos = df_empresa['MODELO'].value_counts().nlargest(15)
    sns.barplot(x=top_15_modelos.values, y=top_15_modelos.index, palette='viridis', ax=ax)
    ax.set_title(f'Top 15 Productos (MODELO) Más Importados ({sufijo_empresa})')
    plt.tight_layout()
    plt.savefig(f'frecuencia_productos_{sufijo_empresa}.png')
    plt.close(fig)

    # 3. Mapa de calor de importaciones por marca y mes
    heatmap_data = df_empresa.groupby([df_empresa['FECHA'].dt.month, 'MARCA_NORMALIZADA']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(18, 10))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d', ax=ax)
    ax.set_title(f'Concentración de Importaciones por Marca y Mes ({sufijo_empresa})')
    ax.set_ylabel('Mes')
    ax.set_yticks(ticks=range(len(heatmap_data.index)), labels=[pd.to_datetime(m, format='%m').strftime('%b') for m in heatmap_data.index], rotation=0)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'heatmap_marca_mes_{sufijo_empresa}.png')
    plt.close(fig)

    # 4. Gráfico de barras de importaciones mensuales con temporadas de pesca
    df_mensual = df_empresa.set_index('FECHA').resample('M').size()
    colores = ['red' if i.month in temporada_pesca else 'blue' for i in df_mensual.index]
    fig, ax = plt.subplots(figsize=(12, 7))
    df_mensual.plot(kind='bar', color=colores, ax=ax)
    ax.set_title(f'Importaciones Mensuales y Temporadas de Pesca ({sufijo_empresa})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'importaciones_temporada_pesca_{sufijo_empresa}.png')
    plt.close(fig)

# --- Generar Gráficos ---
# Gráficos individuales por empresa
generar_graficos_empresa(df_jorle, 'Jorle')
generar_graficos_empresa(df_import360, 'IMPORT360')

# Gráfico comparativo entre ambas empresas (se mantiene)
monthly_company_data = df_completo.groupby([df_completo['FECHA'].dt.to_period('M'), 'EMPRESA']).size().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(12, 7))
monthly_company_data.plot(kind='line', ax=ax)
ax.set_title('Comparativo Mensual de Importaciones entre Empresas')
ax.legend(title='Empresa')
plt.tight_layout()
plt.savefig('comparativo_empresas.png')
plt.close(fig)

print("Análisis y visualizaciones generadas y guardadas.")
