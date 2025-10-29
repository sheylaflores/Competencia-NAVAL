# Análisis Avanzado de Importaciones para el Sector Pesquero: Jorle vs. IMPORT360

## 1. Resumen del Proyecto

Este proyecto realiza un análisis avanzado sobre las importaciones de **Jorle** e **IMPORT360**, utilizando los datos más recientes para identificar patrones de compra y productos estacionales vinculados a las **temporadas de pesca en Perú** (Abril-Junio y Noviembre-Enero).

Se ha implementado un **algoritmo de detección de estacionalidad** para identificar con mayor precisión los productos cuya demanda aumenta significativamente durante la temporada de pesca.

**Estructura del Repositorio:**
- **/data**: Contiene los archivos Excel actualizados.
- **/src**: Contiene el script de análisis `analisis.py`.
- **/output**: Contiene todos los resultados generados.

## 2. Análisis Individual: Jorle

### 2.1. Valor de Importación (US$ CIF) por Marca

![Marcas por Valor - Jorle](output/Jorle_marcas_por_valor.png)
*   **Análisis:** Con los datos actualizados, **SAI** mantiene su liderazgo absoluto en el valor de las importaciones, reforzando la idea de una fuerte especialización. **PULLMASTER** y **CHAR-LYNN** le siguen como marcas secundarias clave.

### 2.2. Cantidad Comercial y Temporadas de Pesca

![Cantidad y Temporada - Jorle](output/Jorle_cantidad_temporada.png)
*   **Análisis:** El comportamiento cíclico se mantiene. Los picos de compra de **cantidad comercial** siguen alineados con las temporadas de pesca, validando que la estrategia de compra de Jorle está directamente impulsada por la demanda del sector.

### 2.3. Mapa de Calor de Cantidad Comercial por Marca y Mes

![Heatmap Cantidad - Jorle](output/Jorle_heatmap_cantidad.png)
*   **Análisis:** El mapa de calor refuerza el patrón estacional. Marcas como **SAI** y **VELJAN** muestran una concentración de importaciones en los meses previos o durante las temporadas de pesca.

### 2.4. Productos con Mayor Estacionalidad (Detectados por Algoritmo)

La siguiente tabla muestra los productos con un alto **índice de estacionalidad**, es decir, aquellos cuya importación es significativamente mayor durante la temporada de pesca.

| MODELO | MARCA | MERCANCÍA | INDICE DE ESTACIONALIDAD |
| :--- | :--- | :--- | :--- |
| 'K190000250 | SAI | "DISCO DE BRONCE, SAI, K190000250" | 3.33 |
| 0154427212 | SAI | "KIT DE GUARNIZION, SAI, 0154427212"| 3.33 |
| S24-10219-0| DENISON | "KIT DE SELLOS, DENISON, S24-10219-0"| 3.33 |
| 15373 5066 | DENISON | "JUEGO DE SELLOS, DENISON, 15373 5066"| 2.50 |
| JH MMDBR STD-A1| HATTELAND | "SOPORTE PARA PANTALLA, HATTELAND, JH MMDBR STD-A1" | 2.50 |

### 2.5. Productos Importados en los Últimos 3 Meses

| FECHA | MARCA | MODELO | MERCANCÍA |
| :--- | :--- | :--- | :--- |
| 2025-09-15 | VELJAN | VM4C-043-002 | "MOTOR HIDRAULICO, VELJAN, VM4C-043-002" |
| 2025-09-15 | VELJAN | V034-67030 | "ANILLO, VELJAN, V034-67030" |
| 2025-08-27 | CHAR-LYNN | 119-1043-003| "MOTOR HYDRAULICO, CHAR-LYNN, 119-1043-003" |
| 2025-08-20 | SAI | 54100031 | "MOTOR HIDRAULICO, SAI, 54100031" |

## 3. Análisis Individual: IMPORT360

### 3.1. Valor de Importación (US$ CIF) por Marca

![Marcas por Valor - IMPORT360](output/IMPORT360_marcas_por_valor.png)
*   **Análisis:** La diversificación sigue siendo la estrategia de IMPORT360. **VELJAN**, **VULKAN**, y **SAI** se reparten el liderazgo en valor, mostrando un portafolio de proveedores más equilibrado que el de Jorle.

### 3.2. Cantidad Comercial y Temporadas de Pesca

![Cantidad y Temporada - IMPORT360](output/IMPORT360_cantidad_temporada.png)
*   **Análisis:** El patrón de compra anticipada se confirma. IMPORT360 aumenta sus importaciones en los meses **previos** al inicio de la temporada alta, lo que podría permitirles asegurar stock y negociar mejores precios.

### 3.3. Mapa de Calor de Cantidad Comercial por Marca y Mes

![Heatmap Cantidad - IMPORT360](output/IMPORT360_heatmap_cantidad.png)
*   **Análisis:** El mapa de calor muestra que marcas como **VELJAN** y **VULKAN** son importadas consistentemente durante los meses previos a la temporada alta.

### 3.4. Productos con Mayor Estacionalidad (Detectados por Algoritmo)

| MODELO | MARCA | MERCANCÍA | INDICE DE ESTACIONALIDAD |
| :--- | :--- | :--- | :--- |
| 7033614000 | VULKAN | "ARANDELAS, VULKAN, S/M" | 5.33 |
| S24-40383-0| METARIS | "CARTUCHO, METARIS, S24-40383-0" | 4.33 |
| S24-10219-0| METARIS | "SELLOS, METARIS, S24-10219-0" | 4.00 |
| 923157 | METARIS | "SELLOS, METARIS, 923157" | 3.33 |
| VS14-29879 | VELJAN | "KIT DE SELLOS, VELJAN, VS14-29879" | 2.67 |

### 3.5. Productos Importados en los Últimos 3 Meses

| FECHA | MARCA | MODELO | MERCANCÍA |
| :--- | :--- | :--- | :--- |
| 2025-10-23 | VELJAN | VS24-40383 | "CARTUCHO, VELJAN, VS24-40383" |
| 2025-10-23 | VELJAN | VS14-29879-0| "KIT DE SELLOS, VELJAN, VS14-29879-0"|
| 2025-10-10 | KOCSIS | DV-206676 | "PINON DE ARRCADOR. KOCSIS. DV-206676" |
| 2025-09-08 | SAI | GM4 1000 | "MOTORES OLEOHIDRAULICOS, SAI, GM4 1000" |

## 4. Conclusiones y Sugerencias Estratégicas

*   **Estrategias de Aprovisionamiento Opuestas:** Los datos confirman que **Jorle** opera con una estrategia reactiva o *Just-in-Time*, mientras que **IMPORT360** es proactiva y se anticipa a la demanda. La estrategia de IMPORT360 parece más robusta ante posibles retrasos en la cadena de suministro.
*   **Inteligencia de Mercado:** El algoritmo de estacionalidad ha identificado productos clave que no son obvios a simple vista. Por ejemplo, el modelo **'K190000250' de SAI** es crucial para Jorle, mientras que las **arandelas VULKAN** lo son para IMPORT360.
*   **Sugerencia Estratégica:**
    *   **Para Jorle:** Deberían considerar diversificar su cartera de proveedores para reducir la dependencia de **SAI**. Analizar los productos estacionales de **METARIS** y **VULKAN**, que son clave para IMPORT360, podría abrir nuevas líneas de negocio.
    *   **Para IMPORT360:** Podrían optimizar su inventario analizando los productos de alta frecuencia de Jorle. Si bien su estrategia de anticipación es buena, podrían estar perdiendo oportunidades en productos de rotación más rápida durante la temporada alta.

Este análisis avanzado proporciona una base sólida para la toma de decisiones estratégicas, permitiendo a ambas empresas optimizar sus compras, diversificar su oferta y responder mejor a la demanda del sector pesquero.
