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
df_completo.dropna(subset=['FECHA', 'US$ CIF'], inplace=True)

# --- Análisis Estadístico Conciso ---
stats_buffer = io.StringIO()
stats_buffer.write("--- Resumen Estadístico (Columnas Relevantes) ---\n")
columnas_relevantes = ['US$ CIF', 'CANTIDAD COMERCIAL', 'PESO NETO', 'PESO BRUTO']
df_relevante = df_completo[columnas_relevantes]
stats_buffer.write(df_relevante.describe().to_string())
with open("resumen_estadistico.txt", "w") as f:
    f.write(stats_buffer.getvalue())

# --- Identificar Productos Clave en Temporada de Pesca (por Valor) ---
temporada_pesca = [4, 5, 6, 11, 12]
df_pesca = df_completo[df_completo['FECHA'].dt.month.isin(temporada_pesca)]
productos_top_pesca_valor = df_pesca.groupby('MODELO')['US$ CIF'].sum().nlargest(15)
with open("productos_temporada.txt", "w") as f:
    f.write("--- Top 15 Productos (MODELO) por Valor US$ CIF en Temporada de Pesca ---\n")
    f.write(productos_top_pesca_valor.to_string())

# --- Función para Generar Gráficos por Empresa ---
def generar_graficos_empresa(df_empresa, sufijo_empresa):
    # 1. Gráfico de tendencia mensual por VALOR
    monthly_brand_data = df_empresa.groupby(df_empresa['FECHA'].dt.to_period('M'))['US$ CIF'].sum()
    fig, ax = plt.subplots(figsize=(15, 8))
    monthly_brand_data.plot(kind='line', ax=ax)
    ax.set_title(f'Tendencia Mensual de Importaciones por Valor US$ CIF ({sufijo_empresa})')
    ax.set_ylabel('Valor Total US$ CIF')
    plt.tight_layout()
    plt.savefig(f'tendencia_valor_mensual_{sufijo_empresa}.png')
    plt.close(fig)

    # 2. Histograma por FRECUENCIA
    fig, ax = plt.subplots(figsize=(12, 7))
    top_15_modelos_freq = df_empresa['MODELO'].value_counts().nlargest(15)
    sns.barplot(x=top_15_modelos_freq.values, y=top_15_modelos_freq.index, palette='viridis', ax=ax)
    ax.set_title(f'Top 15 Productos por Frecuencia ({sufijo_empresa})')
    plt.tight_layout()
    plt.savefig(f'frecuencia_productos_{sufijo_empresa}.png')
    plt.close(fig)

    # 3. Histograma por VALOR
    fig, ax = plt.subplots(figsize=(12, 7))
    top_15_modelos_valor = df_empresa.groupby('MODELO')['US$ CIF'].sum().nlargest(15)
    sns.barplot(x=top_15_modelos_valor.values, y=top_15_modelos_valor.index, palette='plasma', ax=ax)
    ax.set_title(f'Top 15 Productos por Valor US$ CIF ({sufijo_empresa})')
    ax.set_xlabel('Valor Total US$ CIF')
    plt.tight_layout()
    plt.savefig(f'valor_productos_{sufijo_empresa}.png')
    plt.close(fig)

    # 4. Mapa de calor por VALOR
    heatmap_data = df_empresa.groupby([df_empresa['FECHA'].dt.month, 'MARCA_NORMALIZADA'])['US$ CIF'].sum().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(18, 10))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f', ax=ax)
    ax.set_title(f'Valor de Importaciones (US$ CIF) por Marca y Mes ({sufijo_empresa})')
    ax.set_ylabel('Mes')
    ax.set_yticks(ticks=range(len(heatmap_data.index)), labels=[pd.to_datetime(m, format='%m').strftime('%b') for m in heatmap_data.index], rotation=0)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'heatmap_valor_marca_mes_{sufijo_empresa}.png')
    plt.close(fig)

    # 5. Gráfico de barras de importaciones mensuales (por VALOR) con temporadas de pesca
    df_mensual = df_empresa.set_index('FECHA').resample('M')['US$ CIF'].sum()
    colores = ['red' if i.month in temporada_pesca else 'blue' for i in df_mensual.index]
    fig, ax = plt.subplots(figsize=(12, 7))
    df_mensual.plot(kind='bar', color=colores, ax=ax)
    ax.set_title(f'Valor de Importaciones (US$ CIF) y Temporadas de Pesca ({sufijo_empresa})')
    ax.set_ylabel('Valor Total US$ CIF')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'valor_importaciones_temporada_{sufijo_empresa}.png')
    plt.close(fig)

# --- Generar Gráficos ---
generar_graficos_empresa(df_jorle, 'Jorle')
generar_graficos_empresa(df_import360, 'IMPORT360')

# Gráfico comparativo entre ambas empresas (por VALOR)
monthly_company_data = df_completo.groupby([df_completo['FECHA'].dt.to_period('M'), 'EMPRESA'])['US$ CIF'].sum().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(12, 7))
monthly_company_data.plot(kind='line', ax=ax)
ax.set_title('Comparativo Mensual de Valor de Importaciones (US$ CIF) entre Empresas')
ax.set_ylabel('Valor Total US$ CIF')
ax.legend(title='Empresa')
plt.tight_layout()
plt.savefig('comparativo_valor_empresas.png')
plt.close(fig)

print("Análisis y visualizaciones basadas en valor US$ CIF generadas y guardadas.")
