import random
import multiprocessing
from itertools import combinations
from pprint import pprint

def generate_set(max_size, value_range):
    """Генерирует случайные множества."""
    size = random.randint(1, max_size)
    return set(random.sample(range(value_range[0], value_range[1] + 1), size))

def are_disjoint(sets):
    """Проверяет, являются ли множества попарно непересекающимися."""
    for a, b in combinations(sets, 2):
        if not a.isdisjoint(b):
            return False
    return True

def check_disjoint_sets(sets, K):
    """Проверяет наличие K непересекающихся множеств."""
    for comb in combinations(sets, K):
        if are_disjoint(comb):
            return True
    return False

def worker(task_queue, result_queue, sets, K):
    """Рабочий процесс для проверки подпоследовательностей."""
    while not task_queue.empty():
        try:
            start_idx = task_queue.get_nowait()
        except queue.Empty:
            break
        
        end_idx = min(start_idx + 100, len(sets) - K + 1)
        for i in range(start_idx, end_idx):
            if check_disjoint_sets(sets[i:i+K], K):
                result_queue.put(True)
                return
        result_queue.put(False)

def main(N, K, max_size, value_range):
    # Генерация множества
    sets = [generate_set(max_size, value_range) for _ in range(N)]
    pprint(sets[0:100]) if len(sets) >= 100 else pprint(set)
    print("Генерация завершена")

    # Создание очередей задач и результатов
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    # Заполнение очереди задач
    for i in range(0, len(sets) - K + 1, 100):
        task_queue.put(i)

    # Создание и запуск процессов
    processes = []
    for i in range(multiprocessing.cpu_count()-1):
        p = multiprocessing.Process(target=worker, args=(task_queue, result_queue, sets, K))
        p.start()
        processes.append(p)
        print("Запущен процесс #", i+1)

    # Ожидание завершения процессов
    for p in processes:
        p.join()

    # Проверка результатов
    while not result_queue.empty():
        if result_queue.get():
            return True

    return False

if __name__ == "__main__":
    N = 1000  # Количество множеств
    K = 10     # Количество непересекающихся множеств
    max_size = 10  # Максимальный размер каждого множества
    value_range = (1, 100)  # Диапазон значений элементов в множествах
    
    result = main(N, K, max_size, value_range)
    print("Результат:", result)
