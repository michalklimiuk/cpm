import networkx as nx
import time

t1 = time.time()
# odczyt danych z pliku
with open("data80.txt", "r") as file:
    num_tasks, num_dependencies = map(int, file.readline().split())  # Pierwsza linia
    task_durations = list(map(int, file.readline().split()))  # Druga linia

    # stworzenie macierzy zależności Dependencies[a][b] z 2 kolumnami i num_dependencies wierszami
    dependencies = [[0] * 2 for _ in range(num_dependencies)]

    dependency_data = list(map(int, file.readline().split()))  # odczytanie zależności jako listy int
    for i in range(0, len(dependency_data), 2):
        task_a, task_b = dependency_data[i], dependency_data[i + 1]
        dependencies[i // 2][0] = task_a
        dependencies[i // 2][1] = task_b

# stworzenie grafu skierowanego zależności z wykorzystaniem NetworkX - grafu dla par zbiorów
dependency_graph = nx.DiGraph()
for i in range(num_dependencies):
    dependency_graph.add_edge(dependencies[i][0], dependencies[i][1])

# stworzenie list ES, EF, LS, LF
earliest_start_times = [0] * num_tasks
earliest_finish_times = [0] * num_tasks
latest_start_times = [float("inf")] * num_tasks
latest_finish_times = [float("inf")] * num_tasks

task_durations_list = task_durations

# obliczanie ES, EF
for task_node in nx.topological_sort(dependency_graph): # sortowanie topologiczne dla zbioru zależności
    predecessors = list(dependency_graph.predecessors(task_node))   # stworzenie listy poprzedników
    if not predecessors:    # jeśli nie ma poprzedników dla danej operacji to czas nie zmienia się
        earliest_start_times[task_node - 1] = 0
    else:
        earliest_start_times[task_node - 1] = max(earliest_finish_times[p - 1] for p in predecessors)
    earliest_finish_times[task_node - 1] = earliest_start_times[task_node - 1] + task_durations_list[task_node - 1]

# obliczanie LS, LF
max_earliest_finish_time = max(earliest_finish_times)
for task_node in reversed(list(nx.topological_sort(dependency_graph))): # odwrotna kolejność w pętli - od końca

    successors = list(dependency_graph.successors(task_node))   # stworzenie listy następców
    if not successors:  # jeśli nie ma następców dla danej iteracji
        latest_finish_times[task_node - 1] = max_earliest_finish_time
    else:
        latest_finish_times[task_node - 1] = min(latest_start_times[s - 1] for s in successors)
    latest_start_times[task_node - 1] = latest_finish_times[task_node - 1] - task_durations_list[task_node - 1]

# ścieżka krytyczna
critical_path = []
for i in range(num_tasks):
    if earliest_start_times[i] == latest_start_times[i] and earliest_finish_times[i] == latest_finish_times[i]:
        critical_path.append((i + 1, earliest_start_times[i], earliest_finish_times[i]))

# obliczanie całkowitego czasu projektu
total_project_time = max(earliest_finish_times)
t2 = time.time()
taken_time = t2 - t1
print("Czas działania programu:", taken_time)
# Wyświetlenie wyników
#print("process time:")
#print(total_project_time)
#print("earlyStart earlyFinish lateStart lateFinish:")
#for i in range(num_tasks):
#    print(i + 1, earliest_start_times[i], earliest_finish_times[i], latest_start_times[i], latest_finish_times[i])
#print("critical path:")
#for task in critical_path:
#    print(task[0], task[1], task[2])

