import json
import os
import re

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
                    results[filename][key] = int(value.split()[0])
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
    
def main():
    codee_output = """
    {
     "Evaluation": [
     [
      {
       "Target": "/home/manuamest/Descargas/SO-shell-master/P1/commands.c",
       "Lines of code": "491",
       "Optimizable lines": "47",
       "Analysis time": "90 ms",
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
       "Analysis time": "16 ms",
       "# checks": "1",
       "Effort": "8 h",
       "Cost": "261€",
       "Profiling": "  n/a"
      },
      {
       "Target": "Total",
       "Lines of code": "611",
       "Optimizable lines": "47",
       "Analysis time": "120 ms",
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
    }
    """

    metrics = parse_codee_output(codee_output)
    print(metrics)

if __name__ == "__main__":
    main()
