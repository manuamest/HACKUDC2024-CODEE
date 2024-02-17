import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64


#TODO: Añadir grafico de barras por coste de dinero de cada archivo
#TODO: Añadir grafico de complejidad
#TODO: Añadir tabla con los resultados
def generate_report(metrics):
    # Obtener los datos de checks
    checks_data = metrics[0]['Checks']

    # Crear listas separadas para los tipos de checks y sus cantidades
    check_types = [check[0] for check in checks_data]
    check_counts = [check[1] for check in checks_data]

    # Crear un gráfico circular
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.pie(check_counts, labels=check_types, autopct='%1.1f%%', startangle=140)
    plt.title('Tipos de Checks Totales')

    # Convertir el gráfico en una imagen para incrustar en HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen en base64
    img_str_1 = "data:image/png;base64," + base64.b64encode(image_png).decode()

    # Crear un mapa de calor para mostrar qué archivos generan más checks
    files = list(metrics[0].keys())
    files.remove('Total')
    files.remove('Checks')
    file_checks = [metrics[0][file]['# checks'] for file in files]

    plt.figure(figsize=(8, 6))
    sns.heatmap([file_checks], annot=True, xticklabels=files, yticklabels=False, cmap="YlGnBu")
    plt.title('Mapa de Calor de Checks por Archivo')
    plt.xticks(rotation=45, ha='right')

    # Convertir el mapa de calor en una imagen para incrustar en HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen en base64
    img_str_2 = "data:image/png;base64," + base64.b64encode(image_png).decode()

    # Generar el código HTML con los gráficos incrustados
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gráfico Circular y Mapa de Calor</title>
    </head>
    <body>
        <h1>Gráfico Circular y Mapa de Calor</h1>
        <div style="display:flex; justify-content:space-around;">
            <div>
                <h2>Gráfico Circular</h2>
                <img src="{img_str_1}" alt="Gráfico Circular">
            </div>
            <div>
                <h2>Mapa de Calor</h2>
                <img src="{img_str_2}" alt="Mapa de Calor">
            </div>
        </div>
    </body>
    </html>
    """

    # Escribir el código HTML en un archivo
    with open("report.html", "w") as f:
        f.write(html)

def main():
    # Ejemplo de uso
    metrics = [
        {'commands.c': {'# checks': 13},
        'list.c': {'# checks': 5},
        'p2.c': {'# checks': 1}, 'Total': {'# checks': 19},
        'Checks': [('RMK015', 3), ('PWR054', 1), ('PWR024', 1), ('PWR018', 5), ('PWR001', 2), ('PWR029', 1), ('PWR012', 4), ('PWR016', 2)]}
    ]

    generate_report(metrics)

if __name__ == "__main__":
    main()
