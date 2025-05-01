import time
from csv import reader
from collections import defaultdict

from pathlib import Path


def processing_tempratures(file_path: Path):
    print("Iniciando o processamento do arquivo.")

    start_time = time.time()

    temperature_by_station = defaultdict(list)

    with open(file_path, "r", encoding="utf-8") as file:
        _reader = reader(file, delimiter=";")
        for row in _reader:
            station_name, temperature = str(row[0]), float(row[1])
            temperature_by_station[station_name].append(temperature)

    print("Dados carregados. Calculando estatísticas.")

    results = {}

    for station, temperatures in temperature_by_station.items():
        min_temp = min(temperatures)
        mean_temp = sum(temperatures) / len(temperatures)
        max_temp = max(temperatures)
        results[station] = (min_temp, mean_temp, max_temp)

    print("Estatística calculada. Ordenando...")
    sorted_results = dict(sorted(results.items()))

    formatted_results = {
        station: f"{min_temp:.1f}/{mean_temp:.1f}/{max_temp:.1f}"
        for station, (min_temp, mean_temp, max_temp) in sorted_results.items()
    }

    end_time = time.time()
    print(f"Processanmento concluído em {end_time - start_time:.2f} segundos.")

    return formatted_results


if __name__ == "__main__":
    file_path: Path = Path("./data/measurements.txt")
    result = processing_tempratures(file_path)
