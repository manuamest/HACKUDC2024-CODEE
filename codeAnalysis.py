# SPDX-FileCopyrightText: 2024 Manu Amestoy
#
# SPDX-License-Identifier: MIT

import subprocess
import os
import re
import json
import io
import base64
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

def parse_codee_output(output):
    results = {}

    data = json.loads(output)

    # Procesar las secciones de evaluación
    for evaluation_section in data.get("Evaluation", []):
        for entry in evaluation_section:
            filename = os.path.basename(entry["Target"])
            if filename not in results:
                results[filename] = {}

            # Eliminar o reemplazar "n/a" por 0 antes de convertir
            for key, value in entry.items():
                if key != "Target" and key != "Analysis time" and key != "Effort":
                    value = value.strip()
                    if value.lower() == "n/a":
                        value = 0
                    else:
                        value = int(value) if value.isdigit() else float(value.replace("€", ""))
                    results[filename][key] = value
                elif key == "Analysis time":
                    results[filename][key] = float(value.split()[0])
                elif key == "Effort":
                    results[filename][key] = int(re.search(r'\d+', value).group())

    # Procesar las secciones de ranking de checkers
    checkers = []
    for ranking_section in data.get("Ranking of Checkers", []):
        for entry in ranking_section:
            checkers.append((entry["Checker"], int(entry["#"])))

    # Sumar el número total de checks
    total_checks = sum(count for _, count in checkers)
    results["Total"] = {"# checks": total_checks}

    # Agregar los checks individuales a los resultados
    results["Checks"] = checkers

    return results

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

    # Crear un mapa de colores personalizado
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

    # Convertir la imagen en base64
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
                <div class="text-wrapper">Gráfico de complejidad:</div>
                <img class="img" src="{img_str_4}" alt="Gráfico de Complejidad"/>
            </div>
            </div>
            <div class="resumen-datos">
            <div class="text-wrapper">Resumen de datos:</div>
            <div class="datos-datos-datos">
                {summary_html}
            </div>
            </div>
        </div>
        <div class="barra-lateral"></div>
        </div>
    </body>
    </html>
    """

    # GUARDAR EN LOCAL
    #os.chdir("/home/manuamest/Documentos/HACKATON/HACKUDCCODEE")

    # GUARDAR EN GITHUB
    os.chdir("..")

    # Escribir el código HTML en un archivo
    with open("index.html", "w") as f:
        f.write(html)

def run_codee_analysis():
    try:
        # Cambiar al directorio donde se encuentra el proyecto mbedtls

        # EN LOCAL
        #os.chdir("/home/manuamest/Descargas/mbedtls-development")

        # EN GITHUB
        os.chdir("./mbedtls")
        
        # Ejecutar los comandos previos
        # LOCAL
        #subprocess.run(["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS=On", "."])
        #GITHUB
        subprocess.run(["cmake", "-DCMAKE_EXPORT_COMPILE_COMMANDS=On", "/home/runner/work/HACKUDC2024-CODEE/HACKUDC2024-CODEE/mbedtls"])
        subprocess.run(["make", "-j8"])

        # EJECUCION LOCAL
        #output = subprocess.check_output("/home/manuamest/Documentos/HACKATON/codee-2024.1.1-linux-x86_64/bin/pwreport --config compile_commands.json library/*.c --json", shell=True)
        #output = subprocess.check_output("/home/manuamest/Documentos/HACKATON/codee-2024.1.1-linux-x86_64/bin/pwreport --config compile_commands.json tests/*.c --json", shell=True)
        #output = subprocess.check_output("/home/manuamest/Documentos/HACKATON/codee-2024.1.1-linux-x86_64/bin/pwreport --config compile_commands.json programs/fuzz/*.c --json", shell=True)

        # EJECUCION EN GITHUB
        #output = subprocess.check_output("./codee-2024.1.1-linux-x86_64/bin/pwreport --config compile_commands.json library/*.c --json", shell=True)
        output = subprocess.check_output("./codee-2024.1.1-linux-x86_64/bin/pwreport --config compile_commands.json tests/*.c --json", shell=True)
        #output = subprocess.check_output("../codee-2024.1.1-linux-x86_64/bin/pwreport --accept-eula --config compile_commands.json programs/fuzz/*.c --json", shell=True)

        output_variable = output.decode("utf-8")
        return output_variable
    except subprocess.CalledProcessError as e:
        print(f"Error running Codee: {e}")
        return None

def main():
    codee_output = run_codee_analysis()
    if codee_output:
        metrics = [parse_codee_output(codee_output)]    
        if metrics:
            generate_report(metrics)
            print("Informe generado exitosamente en index.html")
        else:
            print("No se pudieron analizar las métricas de Codee.")
    else:
        print("No se pudo ejecutar el análisis de Codee.")

if __name__ == "__main__":
    main()

#cd /home/manuamest/Descargas/mbedtls-development 
#cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=On .
#make -j8
#/home/manuamest/Documentos/HACKATON/codee-2024.1.1-linux-x86_64/bin/pwreport --config compile_commands.json 
