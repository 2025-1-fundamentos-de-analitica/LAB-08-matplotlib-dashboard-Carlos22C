import os
import pandas as pd
import matplotlib.pyplot as plt

def cargar_datos_envios():
    """
    Carga los datos desde el archivo CSV.
    """
    return pd.read_csv('files/input/shipping-data.csv')


def grafico_envios_por_bodega(df):
    """
    Genera un gráfico de barras de envíos por bloque de bodega.
    """
    conteo = df['Warehouse_block'].value_counts()
    fig, ax = plt.subplots()
    conteo.plot.bar(
        ax=ax,
        title='Shipping per Warehouse',
        xlabel='Warehouse block',
        ylabel='Record Count',
        color='tab:blue',
        fontsize=8,
    )
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.savefig('docs/shipping_per_warehouse.png')


def grafico_modo_envio(df):
    """
    Genera un gráfico de pastel con los modos de envío.
    """
    fig, ax = plt.subplots()
    df['Mode_of_Shipment'].value_counts().plot.pie(
        ax=ax,
        title='Mode of Shipment',
        ylabel='',
        wedgeprops={'width': 0.35},
        colors=['tab:blue', 'tab:orange', 'tab:green'],
    )
    fig.savefig('docs/mode_of_shipment.png')


def grafico_calificacion_clientes(df):
    """
    Crea un gráfico de barras horizontales con calificaciones promedio por modo de envío.
    """
    resumen = df[['Mode_of_Shipment', 'Customer_rating']].groupby('Mode_of_Shipment').describe()
    resumen.columns = resumen.columns.droplevel()
    resumen = resumen[['mean', 'min', 'max']]

    fig, ax = plt.subplots()
    ax.barh(
        resumen.index,
        resumen['max'] - 1,
        left=resumen['min'],
        color='lightgray',
        alpha=0.8,
        height=0.9
    )

    colores = ['tab:green' if val >= 3.0 else 'tab:orange' for val in resumen['mean']]
    ax.barh(
        resumen.index,
        resumen['mean'] - 1,
        left=resumen['min'],
        color=colores,
        alpha=1,
        height=0.5
    )

    ax.set_title('Average Customer Rating')
    ax.spines['left'].set_color('gray')
    ax.spines['bottom'].set_color('gray')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.savefig('docs/average_customer_rating.png')


def grafico_distribucion_peso(df):
    """
    Dibuja un histograma con la distribución de pesos enviados.
    """
    fig, ax = plt.subplots()
    df['Weight_in_gms'].plot.hist(
        ax=ax,
        title='Shipped Weight Distribution',
        color='tab:orange',
        edgecolor='white'
    )
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.savefig('docs/weight_distribution.png')


def pregunta_01():
    """
    Función principal que orquesta la generación de gráficos y del HTML resumen.
    """
    os.makedirs('docs', exist_ok=True)

    datos = cargar_datos_envios()
    grafico_envios_por_bodega(datos)
    grafico_modo_envio(datos)
    grafico_calificacion_clientes(datos)
    grafico_distribucion_peso(datos)

    contenido_html = """
    <!DOCTYPE html>
    <html>
        <head><meta charset="utf-8"></head>
        <body>
            <h1>Shipping Dashboard Example</h1>
            <div style="width:45%; float:left">
                <img src="shipping_per_warehouse.png" alt="Warehouse Shipments">
                <img src="mode_of_shipment.png" alt="Mode of Shipment">
            </div>
            <div style="width:45%; float:left">
                <img src="average_customer_rating.png" alt="Customer Ratings">
                <img src="weight_distribution.png" alt="Weight Distribution">
            </div>
        </body>
    </html>
    """
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(contenido_html)


# Ejecutar la función si se desea como script
pregunta_01()
