import heapq
from collections import namedtuple

AssignedJob = namedtuple("AssignedJob", ["worker", "started_at"])


def assign_jobs(n_workers, jobs):
    # Crear un heap con los hilos disponibles
    heap = [(0, i) for i in range(n_workers)]  # (next_free_time, worker_index)
    heapq.heapify(heap)

    result = []

    for job in jobs:
        # Obtener el hilo con el tiempo de finalización más temprano
        next_free_time, worker = heapq.heappop(heap)
        result.append(AssignedJob(worker, next_free_time))

        # Actualizar el tiempo de finalización del hilo y devolverlo al heap
        heapq.heappush(heap, (next_free_time + job, worker))

    return result


def main():
    n_workers, n_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))
    assert len(jobs) == n_jobs

    assigned_jobs = assign_jobs(n_workers, jobs)

    for job in assigned_jobs:
        print(job.worker, job.started_at)


if __name__ == "__main__":
    main()
