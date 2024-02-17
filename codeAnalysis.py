import subprocess
import os
import re
import matplotlib.pyplot as plt
import pandas as pd
from parseCode import parse_codee_output
from generateReport import generate_report

def run_codee_analysis(path):
    try:
        result = subprocess.run(['/home/manuamest/Descargas/codee-2024.1.1-HackUDC/codee-2024.1.1-linux-x86_64/bin/pwreport', path], capture_output=True, text=True, check=True)
        # Combinar la salida estándar y de error en un solo string
        output = result.stdout + result.stderr
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error running Codee: {e}")
        return None

def main():
    path = input("Introduce la ruta del directorio o archivo.c a analizar: ")
    codee_output = run_codee_analysis(path)
    if codee_output:
        metrics = parse_codee_output(codee_output)
        if metrics:
            html_report = generate_report(metrics)
            with open("codee_report.html", "w") as f:
                f.write(html_report)
            print("Informe generado exitosamente en codee_report.html")
        else:
            print("No se pudieron analizar las métricas de Codee.")
    else:
        print("No se pudo ejecutar el análisis de Codee.")

if __name__ == "__main__":
    main()
