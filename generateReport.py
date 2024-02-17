import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
import io
import base64

def generate_report(metrics):
    # Crear el resumen de datos
    summary_html = "<ul>"
    for file, data in metrics[0].items():
        if file not in ['Total', 'Checks']:
            summary_html += f"<li><b>{file}:</b> {data['# checks']} checks, Costo: {data['Cost']}, Líneas de Código: {data['Lines of code']}, Líneas Optimizables: {data['Optimizable lines']}</li>"
    summary_html += "</ul>"

    # Obtener los datos de checks
    checks_data = metrics[0]['Checks']

    # Crear listas separadas para los tipos de checks y sus cantidades
    check_types = [check[0] for check in checks_data]
    check_counts = [check[1] for check in checks_data]

    # Crear un gráfico circular
    plt.figure(figsize=(12, 12))
    plt.pie(check_counts, labels=check_types, autopct='%1.1f%%', startangle=140, textprops={'color': 'white'})
    plt.title('Tipos de Checks Totales', color='white')

    # Cambiar el color del fondo de los ejes
    plt.gca().set_facecolor('#2E2E2E')  # Puedes especificar el color usando códigos hexadecimales, RGB, o nombres de colores

    # Cambiar el color de los ejes (líneas que rodean el área de trazado)
    plt.gca().spines['bottom'].set_color('white')
    plt.gca().spines['top'].set_color('white')
    plt.gca().spines['left'].set_color('white')
    plt.gca().spines['right'].set_color('white')

    # Cambiar el color de los números en los ejes
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')

    # Cambiar el color del fondo de la figura (el área fuera del gráfico)
    fig = plt.gcf()
    fig.patch.set_facecolor('#2E2E2E')  # Puedes especificar el color usando códigos hexadecimales, RGB, o nombres de colores

    # Convertir el gráfico en una imagen para incrustar en HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen en base64
    img_str_1 = "data:image/png;base64," + base64.b64encode(image_png).decode()

    # Crear un mapa de colores personalizado--------------------------------------------------------------------------------------
    colors = ['#FF47FF', '#9747FF']  # Morado a rosa
    cmap = LinearSegmentedColormap.from_list('custom', colors)

    # Crear un mapa de calor para mostrar qué archivos generan más checks
    files = list(metrics[0].keys())
    files.remove('Total')
    files.remove('Checks')
    file_checks = [metrics[0][file]['# checks'] for file in files]

    plt.figure(figsize=(8, 6))
    sns.heatmap([file_checks], annot=True, xticklabels=files, yticklabels=False, cmap=cmap, annot_kws={"color": "white"})

    # Cambiar el color del fondo de los ejes
    plt.gca().set_facecolor('#2E2E2E')

    # Cambiar el color de los ejes
    for spine in plt.gca().spines.values():
        spine.set_color('white')

    # Cambiar el color de los números en los ejes
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')

    # Cambiar el color del fondo de la figura
    fig = plt.gcf()
    fig.patch.set_facecolor('#2E2E2E')

    plt.title('Mapa de Calor de Checks por Archivo', color='white')
    plt.xticks(rotation=45, ha='right', color='white')

    # Convertir el mapa de calor en una imagen para incrustar en HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen en base64-----------------------------------------------------------------------------------------------
    img_str_2 = "data:image/png;base64," + base64.b64encode(image_png).decode()

    # Obtener los datos de checks y costos
    checks_data = metrics[0]

    # Crear listas separadas para los nombres de archivos y sus costos
    files = [file for file in checks_data.keys() if file != 'Total' and file != 'Checks']
    costs = [checks_data[file]['Cost'] for file in files]

    # Crear un gráfico de barras
    plt.figure(figsize=(10, 6))
    sns.barplot(x=files, y=costs)

    # Cambiar el color del fondo de los ejes
    plt.gca().set_facecolor('#2E2E2E')  # Puedes especificar el color usando códigos hexadecimales, RGB, o nombres de colores

    # Cambiar el color de los ejes (líneas que rodean el área de trazado)
    plt.gca().spines['bottom'].set_color('white')
    plt.gca().spines['top'].set_color('white')
    plt.gca().spines['left'].set_color('white')
    plt.gca().spines['right'].set_color('white')

    # Cambiar el color de los números en los ejes
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')

    # Cambiar el color del fondo de la figura (el área fuera del gráfico)
    fig = plt.gcf()
    fig.patch.set_facecolor('#2E2E2E')  # Puedes especificar el color usando códigos hexadecimales, RGB, o nombres de colores

    plt.title('Costo de Reparación por Archivo', color='white')
    plt.xlabel('Archivo', color='white')
    plt.ylabel('Costo', color='white')

    # Convertir el gráfico en una imagen para incrustar en HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen en base64
    img_str_3 = "data:image/png;base64," + base64.b64encode(image_png).decode()

    # Obtener los datos de checks y costos
    checks_data = metrics[0]

    # Crear listas separadas para los nombres de archivos y sus costos
    files = [file for file in checks_data.keys() if file != 'Total' and file != 'Checks']
    lines_of_code = [checks_data[file]['Lines of code'] for file in files]
    optimizable_lines = [checks_data[file]['Optimizable lines'] for file in files]

    # Crear un gráfico de líneas para la complejidad por archivo
    plt.figure(figsize=(10, 6))
    plt.plot(files, lines_of_code, marker='o', label='Líneas de Código')
    plt.plot(files, optimizable_lines, marker='o', label='Líneas Optimizables')

    # Cambiar el color del fondo de los ejes
    plt.gca().set_facecolor('#2E2E2E')  # Puedes especificar el color usando códigos hexadecimales, RGB, o nombres de colores

    # Cambiar el color de los ejes (líneas que rodean el área de trazado)
    plt.gca().spines['bottom'].set_color('white')
    plt.gca().spines['top'].set_color('white')
    plt.gca().spines['left'].set_color('white')
    plt.gca().spines['right'].set_color('white')

    # Cambiar el color de los números en los ejes
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')

    # Cambiar el color del fondo de la figura (el área fuera del gráfico)
    fig = plt.gcf()
    fig.patch.set_facecolor('#2E2E2E')  # Puedes especificar el color usando códigos hexadecimales, RGB, o nombres de colores

    plt.title('Complejidad por Archivo', color='white')
    plt.xlabel('Archivo', color='white')
    plt.ylabel('Número de Líneas', color='white')
    plt.legend()
    plt.xticks(rotation=45, ha='right')

    # Convertir el gráfico en una imagen para incrustar en HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Convertir la imagen en base64
    img_str_4 = "data:image/png;base64," + base64.b64encode(image_png).decode()


    # Generar el código HTML con los gráficos incrustados
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <link rel="stylesheet" href="globals.css" />
        <link rel="stylesheet" href="styleguide.css" />
        <link rel="stylesheet" href="style.css" />
    </head>
    <body>
        <div class="desktop-singin">
        <div class="body">
            <p class="titulo">HackUDC</p>
            <div class="resumen-datos">
            <div class="text-wrapper">Resumen de datos:</div>
            <div class="datos-datos-datos">
                {summary_html}
            </div>
            </div>
            <br>
            <div class="graficos">
            <div class="div">
                <div class="text-wrapper">Gráfico circular:</div>
                <img class="img" src="{img_str_1}" alt="Gráfico Circular">
            </div>
            <div class="div">
                <div class="text-wrapper">Mapa de calor:</div>
                <img class="img" src="{img_str_2}" alt="Mapa de Calor"/>
            </div>
            <div class="div">
                <div class="text-wrapper">Gráfico de barras:</div>
                <img class="img" src="{img_str_3}" alt="Gráfico de Barras"/>
            </div>
            <div class="div">
                <div class="text-wrapper">Mapa de calor:</div>
                <img class="img" src="{img_str_4}" alt="Gráfico de Complejidad"/>
            </div>
            </div>
        </div>
        <div class="barra-lateral"></div>
        </div>
    </body>
    </html>
    """

    # Escribir el código HTML en un archivo
    with open("index.html", "w") as f:
        f.write(html)


def main():
    # Ejemplo de uso
    metrics = [
        {'commands.c': {'# checks': 13, 'Cost': 1636.0, 'Lines of code': 491, 'Optimizable lines': 47}, 
        'list.c': {'# checks': 5, 'Cost': 785.0, 'Lines of code': 83, 'Optimizable lines': 0}, 
        'p2.c': {'# checks': 1, 'Cost': 261.0, 'Lines of code': 37, 'Optimizable lines': 0}, 
        'Total': {'# checks': 19}, 
        'Checks': [('RMK015', 3), ('PWR054', 1), ('PWR024', 1), ('PWR018', 5), ('PWR001', 2), ('PWR029', 1), ('PWR012', 4), ('PWR016', 2)]}
    ]
    generate_report(metrics)

if __name__ == "__main__":
    main()

