import time

def podziel_liste(lista, separator):
    podzielone_listy = []
    aktualna_lista = []

    for element in lista:
        if element == separator:
            if aktualna_lista:
                podzielone_listy.append(aktualna_lista)
            aktualna_lista = []
        else:
            aktualna_lista.append(element)

    if aktualna_lista:
        podzielone_listy.append(aktualna_lista)

    return podzielone_listy

t1 = time.time()

# Odczyt danych z pliku
with open("data80.txt", "r") as file:
    N, M = map(int, file.readline().split())  # Pierwsza linia
    times = list(map(int, file.readline().split()))  # Druga linia

    # Inicjalizacja macierzy zależności X[a][b] z 2 kolumnami i M wierszami
    X = [[0] * 2 for _ in range(M)]  # Macierz zależności z 2 kolumnami i M wierszami

    zaleznosci = list(file.readline().split(" "))
    zaleznosci[-1] = zaleznosci[-1].strip()
    X = podziel_liste(zaleznosci, '')

    for i in range(len(X)):
        for j in range(len(X[i])):
            X[i][j] = int(X[i][j])

#print("N - liczba zadań:", N)
#print("M - liczba połączeń:", M)
#print("Czasy:", times)
#print("Zależności:", X)


# Inicjalizacja zmiennych; zmienne ES,EF,LS,LF; stworzenie list dla tych zmiennych o wielkości N
earlyStart = [0] * N 
earlyFinish = [0] * N
lateStart = [float("inf")] * N
lateFinish = [float("inf")] * N

# Obliczenia
for i in range(N):
    for i in range(N):  # dla kazdego zadania
        maxEarlyStart = 0
        for j in range(M):  # sprawdzane są połączenia
            if X[j][1] == i + 1:    # sprawdzenie czy drugi element macierzy jest równy numerowi zadania +1
                maxEarlyStart = max(maxEarlyStart, earlyFinish[X[j][0] - 1])    # sprawdzenie maksymalnego czasu między zadaniami połączonymi z aktualnie iterowanym zadaniem
        earlyStart[i] = maxEarlyStart   # ES - czas rozpoczecie zadania równy max ES
        earlyFinish[i] = earlyStart[i] + times[i]   # EF to czas rozpoczecia plus czas wykonania zadania

total_time = max(earlyFinish)  # Calkowity czas projektu
for i in range(N):
    for i in range(N - 1, -1, -1):  # pętla od ostatniego zadania
        minLateFinish = total_time
        for j in range(M):
            if X[j][0] == i + 1:
                minLateFinish = min(minLateFinish, lateStart[X[j][1] - 1])
        lateFinish[i] = minLateFinish
        lateStart[i] = lateFinish[i] - times[i]

# Sciezka krytyczna
critical_path = []
for i in range(N):
    if earlyStart[i] == lateStart[i] and earlyFinish[i] == lateFinish[i]:
        critical_path.append((i + 1, earlyStart[i], earlyFinish[i]))

t2 = time.time()

taken_time = t2-t1
print("Czas wykonania programu: ", taken_time)
# Wyświetlenie wyników
#print("Calkowity czas projektu:", total_time)
#print("earlyStart earlyFinish lateStart lateFinish:")
#for i in range(N):
    #print(i + 1, earlyStart[i], earlyFinish[i], lateStart[i], lateFinish[i])
#print("critical path:")
#for task in critical_path:
    #print(task[0], task[1], task[2])



# 0.0019969940185546875