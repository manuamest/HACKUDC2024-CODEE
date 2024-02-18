<!--
SPDX-FileCopyrightText: 2024 Manu Amestoy

SPDX-License-Identifier: MIT
-->

# CodeeHACK

### Resultados de un analisis de muchos archivos
![BigAnalysis](https://github.com/manuamest/HACKUDC2024-CODEE/blob/bd3bd5047a04387a9e9c8f8703604a2adcb0dcf4/images/BigAnalysis.png)
### Resultados de un analisis de pocos archivos
![SmallAnalysis](https://github.com/manuamest/HACKUDC2024-CODEE/blob/bd3bd5047a04387a9e9c8f8703604a2adcb0dcf4/images/SmallAnalysis.png)
### Correo con el informe del analisis
![mail](https://github.com/manuamest/HACKUDC2024-CODEE/blob/bd3bd5047a04387a9e9c8f8703604a2adcb0dcf4/images/mail.png)

## Información del Script

Este script está diseñado para realizar análisis de código utilizando la herramienta Codee. Genera un informe en formato HTML que incluye gráficos y estadísticas sobre las métricas de calidad del código analizado.

## Dependencias

El script depende de las siguientes bibliotecas de Python:

- `matplotlib`
- `pandas`
- `seaborn`

Asegúrate de tener estas bibliotecas instaladas en tu entorno Python antes de ejecutar el script.

## Capacidades

El script tiene las siguientes capacidades:

- Analiza archivos de código fuente utilizando la herramienta Codee.
- Genera un informe HTML que incluye:
  - Un resumen de datos que muestra el número de checks, costo, líneas de código y líneas optimizables para cada archivo analizado.
  - Gráficos que visualizan diferentes aspectos del análisis, incluyendo tipos de checks, mapa de calor de checks por archivo, costo de reparación por archivo y complejidad por archivo.

## Limitaciones y Otros

- Este script asume que la herramienta Codee está instalada y accesible a través de la ruta especificada en la función `run_codee_analysis()`.
- El análisis se realiza en archivos con extensión ".c", por lo que puede no ser adecuado para otros tipos de archivos de código fuente.
- El script está diseñado para sistemas Linux y puede requerir ajustes para ejecutarse en otros sistemas operativos.

## Uso

Para ejecutar el script, simplemente ejecuta el archivo Python `codeAnalysis.py`. Asegúrate de proporcionar la ruta correcta al directorio o archivo `.c` que deseas analizar cuando se te solicite.

```bash
python codeAnalysis.py
```

