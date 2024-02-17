import re

def parse_codee_output(output):
    # Inicializar un diccionario para almacenar los resultados
    results = {}

    # Usar expresiones regulares para extraer los resultados de cada sección
    evaluation_sections = re.findall(r'"Evaluation": \[(.*?)\]', output, re.DOTALL)
    ranking_sections = re.findall(r'"Ranking of Checkers": \[(.*?)\]', output, re.DOTALL)

    # Procesar las secciones de evaluación
    for section in evaluation_sections:
        targets = re.findall(r'"Target": "(.*?)",', section)
        metrics = re.findall(r'"# checks": "(.*?)",', section)
        for target, metric in zip(targets, metrics):
            results[target] = {"# checks": int(metric)}

    # Procesar las secciones de ranking de checkers
    checkers = []
    for section in ranking_sections:
        checkers_info = re.findall(r'"Checker": "(.*?)",.*?"#": "(.*?)"', section, re.DOTALL)
        for checker, count in checkers_info:
            checkers.append((checker, int(count)))

    # Sumar el número total de checks
    total_checks = sum(count for _, count in checkers)
    results["Total"] = {"# checks": total_checks}

    # Agregar los checks individuales a los resultados
    results["Checks"] = checkers

    return results
    

def main():

    # Uso del parser
    codee_output = """
        {
    "Evaluation": [
    [
    {
    "Target": "/home/manuamest/Descargas/SO-shell-master/P1/commands.c",
    "Lines of code": "491",
    "Optimizable lines": "47",
    "Analysis time": "78 ms",
    "# checks": "13",
    "Effort": "50 h",
    "Cost": "1636€",
    "Profiling": "  n/a"
    },
    {
    "Target": "/home/manuamest/Descargas/SO-shell-master/P1/list.c",
    "Lines of code": "83",
    "Optimizable lines": "0",
    "Analysis time": "14 ms",
    "# checks": "5",
    "Effort": "24 h",
    "Cost": "785€",
    "Profiling": "  n/a"
    },
    {
    "Target": "/home/manuamest/Descargas/SO-shell-master/P1/p2.c",
    "Lines of code": "37",
    "Optimizable lines": "0",
    "Analysis time": "15 ms",
    "# checks": "1",
    "Effort": "8 h",
    "Cost": "261€",
    "Profiling": "  n/a"
    },
    {
    "Target": "Total",
    "Lines of code": "611",
    "Optimizable lines": "47",
    "Analysis time": "107 ms",
    "# checks": "19",
    "Effort": "82 h",
    "Cost": "2683€",
    "Profiling": "  n/a"
    }
    ],
    [
    {
    "Target": "/home/manuamest/Descargas/SO-shell-master/P1/commands.c",
    "Scalar": "0",
    "Control": "5",
    "Memory": "0",
    "Vector": "2",
    "Multi": "n/a",
    "Offload": "n/a",
    "Quality": "6",
    "L1": "2",
    "L2": "6",
    "L3": "5"
    },
    {
    "Target": "/home/manuamest/Descargas/SO-shell-master/P1/list.c",
    "Scalar": "0",
    "Control": "0",
    "Memory": "0",
    "Vector": "1",
    "Multi": "n/a",
    "Offload": "n/a",
    "Quality": "4",
    "L1": "1",
    "L2": "0",
    "L3": "4"
    },
    {
    "Target": "/home/manuamest/Descargas/SO-shell-master/P1/p2.c",
    "Scalar": "0",
    "Control": "0",
    "Memory": "0",
    "Vector": "1",
    "Multi": "n/a",
    "Offload": "n/a",
    "Quality": "0",
    "L1": "1",
    "L2": "0",
    "L3": "0"
    },
    {
    "Target": "Total",
    "Scalar": "0",
    "Control": "5",
    "Memory": "0",
    "Vector": "4",
    "Multi": "n/a",
    "Offload": "n/a",
    "Quality": "10",
    "L1": "4",
    "L2": "6",
    "L3": "9"
    }
    ]
    ],
    "Ranking of Checkers": [
    [
    {
    "Checker": "RMK015",
    "Level": "L1",
    "Priority": "P27",
    "#": "3",
    "Title": "Tune compiler optimization flags to increase the speed of the code"
    },
    {
    "Checker": "PWR054",
    "Level": "L1",
    "Priority": "P12",
    "#": "1",
    "Title": "Consider applying vectorization to scalar reduction loop"
    },
    {
    "Checker": "PWR024",
    "Level": "L2",
    "Priority": "P8",
    "#": "1",
    "Title": "Loop can be rewritten in OpenMP canonical form"
    },
    {
    "Checker": "PWR018",
    "Level": "L2",
    "Priority": "P6",
    "#": "5",
    "Title": "Call to recursive function within a loop inhibits vectorization"
    },
    {
    "Checker": "PWR001",
    "Level": "L3",
    "Priority": "P3",
    "#": "2",
    "Title": "Declare global variables as function parameters"
    },
    {
    "Checker": "PWR029",
    "Level": "L3",
    "Priority": "P3",
    "#": "1",
    "Title": "Remove integer increment preventing performance optimization"
    },
    {
    "Checker": "PWR012",
    "Level": "L3",
    "Priority": "P2",
    "#": "4",
    "Title": "Pass only required fields from derived type as parameters"
    },
    {
    "Checker": "PWR016",
    "Level": "L3",
    "Priority": "P2",
    "#": "2",
    "Title": "Use separate arrays instead of an Array-of-Structs"
    }
    ]
    ]
    ]
    """

    # Llamamos a la función para parsear la salida de Codee
    metrics = parse_codee_output(codee_output)
    print(metrics)

if __name__ == "__main__":
    main()
