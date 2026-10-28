"""
AI-Powered Mental Health Monitoring System
Course : Operating Systems (CCSE0303A) - Project Based Learning
Group  : 24 | NIET Greater Noida

OS concepts demonstrated:
  Module 2 & 3 -> threads, priority queue (crisis packets first), readers-writers lock
  Module 3     -> Banker's Algorithm (deadlock avoidance)
  Module 4     -> LRU page replacement (virtual memory / demand paging)

Run: python app.py
"""

import queue
import sys
import threading
import time
from dataclasses import dataclass
from typing import List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# =====================================================================
# MODULE 3: READERS-WRITERS LOCK (writer priority)
# Many threads can read patient records, but only one can write.
# =====================================================================

class ReadWriteLock:
    def __init__(self):
        self._readers = 0
        self._writers = 0
        self._lock = threading.Lock()
        self._ok_to_read = threading.Condition(self._lock)
        self._ok_to_write = threading.Condition(self._lock)

    def acquire_read(self):
        with self._lock:
            while self._writers > 0:
                self._ok_to_read.wait()
            self._readers += 1

    def release_read(self):
        with self._lock:
            self._readers -= 1
            if self._readers == 0:
                self._ok_to_write.notify()

    def acquire_write(self):
        with self._lock:
            self._writers += 1
            while self._readers > 0:
                self._ok_to_write.wait()

    def release_write(self):
        with self._lock:
            self._writers -= 1
            self._ok_to_write.notify()
            self._ok_to_read.notify_all()


# =====================================================================
# MODULE 3: BANKER'S ALGORITHM (deadlock avoidance)
# Resources: R0 = GPU cores, R1 = audio DMA buffers, R2 = shared memory
# =====================================================================

class BankersAlgorithm:
    def __init__(self, available: List[int], max_matrix: List[List[int]],
                 allocation_matrix: List[List[int]]):
        self.available = list(available)
        self.max = max_matrix
        self.allocation = allocation_matrix
        self.num_processes = len(max_matrix)
        self.num_resources = len(available)
        self.need = [
            [self.max[i][j] - self.allocation[i][j] for j in range(self.num_resources)]
            for i in range(self.num_processes)
        ]

    def is_safe_state(self) -> Tuple[bool, List[str]]:
        work = list(self.available)
        finish = [False] * self.num_processes
        safe_sequence = []

        while len(safe_sequence) < self.num_processes:
            found = False
            for p in range(self.num_processes):
                if not finish[p] and all(self.need[p][j] <= work[j]
                                         for j in range(self.num_resources)):
                    for j in range(self.num_resources):
                        work[j] += self.allocation[p][j]
                    finish[p] = True
                    safe_sequence.append(f"P{p}")
                    found = True
                    break
            if not found:
                return False, []
        return True, safe_sequence

    def request_resources(self, pid: int, request: List[int]) -> bool:
        for j in range(self.num_resources):
            if request[j] > self.need[pid][j]:
                raise ValueError("Process asked for more than its declared maximum.")
            if request[j] > self.available[j]:
                return False  # not enough resources right now, process must wait

        # Pretend to allocate, then check if the state is still safe
        for j in range(self.num_resources):
            self.available[j] -= request[j]
            self.allocation[pid][j] += request[j]
            self.need[pid][j] -= request[j]

        safe, _ = self.is_safe_state()
        if safe:
            return True

        # Not safe -> rollback the request
        for j in range(self.num_resources):
            self.available[j] += request[j]
            self.allocation[pid][j] -= request[j]
            self.need[pid][j] += request[j]
        return False


# =====================================================================
# MODULE 4: LRU PAGE REPLACEMENT (virtual memory)
# =====================================================================

class LRUPageCache:
    def __init__(self, capacity: int = 3):
        self.capacity = capacity
        self.cache = {}
        self.order = []
        self.page_faults = 0
        self.hits = 0

    def access_page(self, patient_id: int, payload: str) -> str:
        if patient_id in self.cache:
            self.hits += 1
            self.order.remove(patient_id)
            self.order.append(patient_id)
            return "CACHE_HIT"

        self.page_faults += 1
        evicted = None
        if len(self.cache) >= self.capacity:
            evicted = self.order.pop(0)
            del self.cache[evicted]

        self.cache[patient_id] = payload
        self.order.append(patient_id)
        if evicted is None:
            return "PAGE_FAULT (Allocated Free Frame)"
        return f"PAGE_FAULT (Evicted P{evicted})"


# =====================================================================
# MODULE 2 & 3: MULTI-THREADED PIPELINE
# =====================================================================

@dataclass
class HealthTelemetryPacket:
    packet_id: int
    patient_id: int
    text_input: str
    heart_rate: int
    priority: int  # 1 = crisis, 2 = anxiety, 3 = normal
    timestamp: float


# (patient id, text, heart rate) - fixed data so every run gives the same output
SAMPLE_TELEMETRY = [
    (202, "I feel completely overwhelmed and hopeless tonight", 138),
    (201, "Just resting after my evening walk", 76),
    (205, "Having acute chest pain and intense panic episode", 144),
    (202, "I cannot go on any longer, feeling severe urges to harm myself", 148),
    (204, "Work was exhausting today, feeling a bit stressed", 102),
    (201, "Feeling a bit anxious before my exam tomorrow", 112),
]


class AIMentalHealthPipeline:
    def __init__(self):
        self.crisis_queue = queue.PriorityQueue()
        self.rw_lock = ReadWriteLock()
        self.shared_clinical_db = {}
        self.lru_memory = LRUPageCache(capacity=3)

        self.crisis_keywords = ["suicide", "hopeless", "panic", "can't breathe",
                                "harm", "kill myself", "end it all"]
        self.anxiety_keywords = ["anxious", "stressed", "nervous", "overwhelmed",
                                 "insomnia", "dread"]

    def classify(self, text: str, heart_rate: int) -> Tuple[str, int]:
        """Simple keyword + heart-rate based urgency classifier."""
        text = text.lower()
        if any(k in text for k in self.crisis_keywords) or heart_rate > 130:
            return "CRITICAL_CRISIS", 1
        if any(k in text for k in self.anxiety_keywords) or heart_rate > 105:
            return "ELEVATED_ANXIETY", 2
        return "NORMAL_AFFECT", 3

    def producer_telemetry_sensor(self):
        """Sensor thread: reads patient data and puts packets into the queue."""
        for i, (patient_id, text, heart_rate) in enumerate(SAMPLE_TELEMETRY, start=101):
            label, priority = self.classify(text, heart_rate)
            packet = HealthTelemetryPacket(
                packet_id=i,
                patient_id=patient_id,
                text_input=text,
                heart_rate=heart_rate,
                priority=priority,
                timestamp=time.time(),
            )
            # smaller number = higher priority, so crisis is handled first
            self.crisis_queue.put((priority, packet))
            print(f"[Sensor Thread] Ingested Packet #{i} | Patient {patient_id} | "
                  f"Urgency: Priority {priority} ({label})")
            time.sleep(0.35)

        # one empty packet per worker tells it there is no more work
        for _ in range(2):
            self.crisis_queue.put((99, None))

    def consumer_ai_worker(self, worker_id: int):
        """Worker thread: runs the AI model on one packet at a time."""
        while True:
            priority, packet = self.crisis_queue.get()
            if packet is None:
                self.crisis_queue.task_done()
                break

            print(f" -> [Worker Thread-{worker_id}] Executing Packet #{packet.packet_id} "
                  f"(Priority {priority})")

            status = self.lru_memory.access_page(
                packet.patient_id, f"ContextVector_P{packet.patient_id}")
            print(f"    [Memory] Patient {packet.patient_id}: {status}")

            # writing to the shared database needs an exclusive lock
            self.rw_lock.acquire_write()
            self.shared_clinical_db[packet.patient_id] = {
                "last_hr": packet.heart_rate,
                "text": packet.text_input,
                "urgency_level": priority,
                "updated_at": packet.timestamp,
            }
            self.rw_lock.release_write()

            # crisis packets are processed faster
            time.sleep(0.12 if priority == 1 else 0.30)

            if priority == 1:
                print(f"    [!] >>> CRITICAL ALERT DISPATCHED: Emergency notification "
                      f"sent for Patient {packet.patient_id}!")

            self.crisis_queue.task_done()


def test_bankers_scenario():
    print("\n" + "=" * 75)
    print("  MODULE 3 DEMO: BANKER'S ALGORITHM DEADLOCK AVOIDANCE")
    print("=" * 75)

    available = [3, 3, 2]
    max_claims = [
        [7, 5, 3],  # P0: audio stream worker
        [3, 2, 2],  # P1: real-time inference engine
        [9, 0, 2],  # P2: emergency dispatch service
        [2, 2, 2],  # P3: wearable sensor parser
        [4, 3, 3],  # P4: database archiver
    ]
    allocated = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2],
    ]

    banker = BankersAlgorithm(available, max_claims, allocated)
    safe, sequence = banker.is_safe_state()
    print(f"[*] Initial System State Safe: {safe}")
    print(f"[*] Validated Deadlock-Free Execution Sequence: {' -> '.join(sequence)}")

    request = [1, 0, 2]
    print(f"[*] Process P1 requests resources: {request}")
    print(f"[+] Request Granted safely without deadlock risk: "
          f"{banker.request_resources(1, request)}")
    print("=" * 75 + "\n")


def main():
    print("=" * 75)
    print("   AI-POWERED MENTAL HEALTH MONITORING SYSTEM - OS INFRASTRUCTURE")
    print("   NIET Greater Noida | Department of Artificial Intelligence")
    print("   Group 24 | Course: Operating Systems (CCSE0303A)")
    print("=" * 75)

    test_bankers_scenario()

    print("=" * 75)
    print("  MODULE 2 & 3 DEMO: THREADS, SYNCHRONIZATION AND LRU PAGING")
    print("=" * 75)

    pipeline = AIMentalHealthPipeline()

    sensor_thread = threading.Thread(target=pipeline.producer_telemetry_sensor,
                                     name="SensorProducer")
    worker_threads = [
        threading.Thread(target=pipeline.consumer_ai_worker, args=(i,),
                         name=f"AIWorker-{i}")
        for i in range(2)
    ]

    sensor_thread.start()
    for worker in worker_threads:
        worker.start()

    sensor_thread.join()
    for worker in worker_threads:
        worker.join()

    memory = pipeline.lru_memory
    references = memory.page_faults + memory.hits
    print("\n" + "=" * 75)
    print("  SYSTEM RUNTIME SUMMARY")
    print("=" * 75)
    print(f"Total Memory References: {references} | "
          f"Page Faults (Demand Paged): {memory.page_faults} | Cache Hits: {memory.hits}")
    print(f"Active Profiles in RAM: {list(memory.cache)} | "
          f"Clinical Vault Records: {len(pipeline.shared_clinical_db)} verified.")
    print("=" * 75)


if __name__ == "__main__":
    main()
