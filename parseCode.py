import json
import os

def parse_codee_output(output):
    results = {}

    data = json.loads(output)

    # Procesar las secciones de evaluación
    for section in data.get("Evaluation", []):
        for entry in section:
            if "Target" in entry:
                filename = os.path.basename(entry["Target"])
                results[filename] = {
                    "# checks": int(entry.get("# checks", 0)),
                    "Cost": float(entry.get("Cost", 0).replace("€", "")),
                    "Lines of code": int(entry.get("Lines of code", 0)),
                    "Optimizable lines": int(entry.get("Optimizable lines", 0))
                }

    # Procesar las secciones de ranking de checkers
    checkers = []
    for section in data.get("Ranking of Checkers", []):
        for entry in section:
            checkers.append((entry["Checker"], int(entry["#"])))

    # Sumar el número total de checks
    total_checks = sum(count for _, count in checkers)
    results["Total"] = {"# checks": total_checks}

    # Agregar los checks individuales a los resultados
    results["Checks"] = checkers

    return results
    

def main():
    codee_output = """
    {
        "Evaluation": [
            [
                {
                    "Target": "/home/manuamest/Descargas/SO-shell-master/P1/commands.c",
                    "Lines of code": 491,
                    "Optimizable lines": 47,
                    "Analysis time": "78 ms",
                    "# checks": 13,
                    "Effort": "50 h",
                    "Cost": "1636€",
                    "Profiling": "  n/a"
                },
                {
                    "Target": "/home/manuamest/Descargas/SO-shell-master/P1/list.c",
                    "Lines of code": 83,
                    "Optimizable lines": 0,
                    "Analysis time": "14 ms",
                    "# checks": 5,
                    "Effort": "24 h",
                    "Cost": "785€",
                    "Profiling": "  n/a"
                },
                {
                    "Target": "/home/manuamest/Descargas/SO-shell-master/P1/p2.c",
                    "Lines of code": 37,
                    "Optimizable lines": 0,
                    "Analysis time": "15 ms",
                    "# checks": 1,
                    "Effort": "8 h",
                    "Cost": "261€",
                    "Profiling": "  n/a"
                },
                {
                    "Target": "Total",
                    "Lines of code": 611,
                    "Optimizable lines": 47,
                    "Analysis time": "107 ms",
                    "# checks": 19,
                    "Effort": "82 h",
                    "Cost": "2683€",
                    "Profiling": "  n/a"
                }
            ]
        ],
        "Ranking of Checkers": [
            [
                {
                    "Checker": "RMK015",
                    "Level": "L1",
                    "Priority": "P27",
                    "#": 3,
                    "Title": "Tune compiler optimization flags to increase the speed of the code"
                },
                {
                    "Checker": "PWR054",
                    "Level": "L1",
                    "Priority": "P12",
                    "#": 1,
                    "Title": "Consider applying vectorization to scalar reduction loop"
                },
                {
                    "Checker": "PWR024",
                    "Level": "L2",
                    "Priority": "P8",
                    "#": 1,
                    "Title": "Loop can be rewritten in OpenMP canonical form"
                },
                {
                    "Checker": "PWR018",
                    "Level": "L2",
                    "Priority": "P6",
                    "#": 5,
                    "Title": "Call to recursive function within a loop inhibits vectorization"
                },
                {
                    "Checker": "PWR001",
                    "Level": "L3",
                    "Priority": "P3",
                    "#": 2,
                    "Title": "Declare global variables as function parameters"
                },
                {
                    "Checker": "PWR029",
                    "Level": "L3",
                    "Priority": "P3",
                    "#": 1,
                    "Title": "Remove integer increment preventing performance optimization"
                },
                {
                    "Checker": "PWR012",
                    "Level": "L3",
                    "Priority": "P2",
                    "#": 4,
                    "Title": "Pass only required fields from derived type as parameters"
                },
                {
                    "Checker": "PWR016",
                    "Level": "L3",
                    "Priority": "P2",
                    "#": 2,
                    "Title": "Use separate arrays instead of an Array-of-Structs"
                }
            ]
        ]
    }
    """

    metrics = parse_codee_output(codee_output)
    print(metrics)

if __name__ == "__main__":
    main()
