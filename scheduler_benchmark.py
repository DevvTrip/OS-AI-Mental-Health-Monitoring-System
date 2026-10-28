"""
CPU Scheduling Performance Benchmark
Module 2: Process & CPU Scheduling Evaluation
Compares FCFS, SJF (non-preemptive), SRTF, Priority (preemptive) and Round Robin (RR)
Course: Operating Systems (CCSE0303A) | Group 24 | NIET Greater Noida

Metrics measured: Waiting Time, Turnaround Time, Response Time, Throughput
Run: python scheduler_benchmark.py
"""

# Workload taken from the AI mental health monitoring subsystems
# P1: Audio Feature Extraction
# P2: Crisis Keyword Detection (highest urgency)
# P3: Heart Rate Variability (HRV) Spectral Filter
# P4: Deep Transformer Sentiment Classifier
processes = [
    {"pid": "P1", "task": "Audio Feature Extraction",    "burst": 8, "arrival": 0, "priority": 3},
    {"pid": "P2", "task": "Crisis Keyword Detection",    "burst": 4, "arrival": 1, "priority": 1},
    {"pid": "P3", "task": "Heart Rate Spectral Filter",  "burst": 9, "arrival": 2, "priority": 4},
    {"pid": "P4", "task": "Deep Transformer Classifier", "burst": 5, "arrival": 3, "priority": 2},
]


def simulate_fcfs():
    """First Come First Serve - non-preemptive."""
    t = 0
    wt, tat, ct, rt = {}, {}, {}, {}
    for p in sorted(processes, key=lambda x: x["arrival"]):
        if t < p["arrival"]:
            t = p["arrival"]
        wt[p["pid"]] = t - p["arrival"]
        rt[p["pid"]] = wt[p["pid"]]      # no preemption, so first response = waiting time
        t += p["burst"]
        ct[p["pid"]] = t
        tat[p["pid"]] = ct[p["pid"]] - p["arrival"]
    return wt, tat, ct, rt


def simulate_sjf():
    """Shortest Job First - non-preemptive. Chooses the shortest job in the ready queue."""
    t = 0
    wt, tat, ct, rt = {}, {}, {}, {}
    ready, unstarted = [], list(processes)
    completed = 0

    while completed < len(processes):
        for p in unstarted[:]:
            if p["arrival"] <= t:
                ready.append(p)
                unstarted.remove(p)
        if not ready:
            t += 1
            continue
        ready.sort(key=lambda x: x["burst"])
        curr = ready.pop(0)
        wt[curr["pid"]] = t - curr["arrival"]
        rt[curr["pid"]] = wt[curr["pid"]]
        t += curr["burst"]
        ct[curr["pid"]] = t
        tat[curr["pid"]] = ct[curr["pid"]] - curr["arrival"]
        completed += 1

    return wt, tat, ct, rt


def simulate_srtf():
    """Shortest Remaining Time First - preemptive version of SJF."""
    rem_burst = {p["pid"]: p["burst"] for p in processes}
    arrival = {p["pid"]: p["arrival"] for p in processes}
    burst = {p["pid"]: p["burst"] for p in processes}
    t = 0
    completed = 0
    wt, tat, ct, rt = {}, {}, {}, {}

    while completed < len(processes):
        available = [p for p in processes if p["arrival"] <= t and rem_burst[p["pid"]] > 0]
        if not available:
            t += 1
            continue
        available.sort(key=lambda x: rem_burst[x["pid"]])
        curr = available[0]
        rem_burst[curr["pid"]] -= 1
        rt.setdefault(curr["pid"], t - arrival[curr["pid"]])   # first time on CPU
        t += 1

        if rem_burst[curr["pid"]] == 0:
            completed += 1
            ct[curr["pid"]] = t
            tat[curr["pid"]] = ct[curr["pid"]] - arrival[curr["pid"]]
            wt[curr["pid"]] = tat[curr["pid"]] - burst[curr["pid"]]

    return wt, tat, ct, rt


def simulate_priority_preemptive():
    """Preemptive Priority - smaller priority number means more urgent."""
    rem_burst = {p["pid"]: p["burst"] for p in processes}
    arrival = {p["pid"]: p["arrival"] for p in processes}
    burst = {p["pid"]: p["burst"] for p in processes}
    t = 0
    completed = 0
    wt, tat, ct, rt = {}, {}, {}, {}

    while completed < len(processes):
        available = [p for p in processes if p["arrival"] <= t and rem_burst[p["pid"]] > 0]
        if not available:
            t += 1
            continue
        available.sort(key=lambda x: x["priority"])
        curr = available[0]
        rem_burst[curr["pid"]] -= 1
        rt.setdefault(curr["pid"], t - arrival[curr["pid"]])
        t += 1

        if rem_burst[curr["pid"]] == 0:
            completed += 1
            ct[curr["pid"]] = t
            tat[curr["pid"]] = ct[curr["pid"]] - arrival[curr["pid"]]
            wt[curr["pid"]] = tat[curr["pid"]] - burst[curr["pid"]]

    return wt, tat, ct, rt


def simulate_round_robin(quantum=4):
    """Round Robin - each process runs for at most 'quantum' time units."""
    rem_burst = {p["pid"]: p["burst"] for p in processes}
    arrival = {p["pid"]: p["arrival"] for p in processes}
    burst = {p["pid"]: p["burst"] for p in processes}
    t = 0
    completed = 0
    queue, visited = [], set()
    tat, wt, ct, rt = {}, {}, {}, {}

    while completed < len(processes):
        for p in processes:
            if p["arrival"] <= t and p["pid"] not in visited:
                queue.append(p["pid"])
                visited.add(p["pid"])

        if not queue:
            t += 1
            continue

        pid = queue.pop(0)
        rt.setdefault(pid, t - arrival[pid])       # first time on CPU
        exec_time = min(quantum, rem_burst[pid])
        rem_burst[pid] -= exec_time
        t += exec_time

        for p in processes:
            if p["arrival"] <= t and p["pid"] not in visited:
                queue.append(p["pid"])
                visited.add(p["pid"])

        if rem_burst[pid] == 0:
            completed += 1
            ct[pid] = t
            tat[pid] = ct[pid] - arrival[pid]
            wt[pid] = tat[pid] - burst[pid]
        else:
            queue.append(pid)

    return wt, tat, ct, rt


def throughput(ct):
    """Processes completed per unit time (total time = last completion)."""
    return len(ct) / max(ct.values())


def print_table(title, headers, rows):
    print(f"\n=== {title} ===")
    widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))

    separator = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
    header_str = "|" + "|".join([f" {headers[i]:<{widths[i]}} " for i in range(len(headers))]) + "|"
    print(separator)
    print(header_str)
    print(separator)
    for row in rows:
        row_str = "|" + "|".join([f" {str(row[i]):<{widths[i]}} " for i in range(len(row))]) + "|"
        print(row_str)
    print(separator)


def main():
    print("=" * 80)
    print("  CPU SCHEDULING BENCHMARK FOR AI MENTAL HEALTH MONITORING SYSTEM")
    print("  Course: Operating Systems (CCSE0303A) | Group 24 - NIET Greater Noida")
    print("=" * 80)

    proc_rows = [
        [p["pid"], p["task"], p["arrival"], p["burst"], p["priority"]]
        for p in processes
    ]
    print_table("Experimental Task Workload",
                ["PID", "Task Description", "Arrival (ms)", "Burst (ms)", "Priority"],
                proc_rows)

    fcfs = simulate_fcfs()
    sjf = simulate_sjf()
    srtf = simulate_srtf()
    prio = simulate_priority_preemptive()
    rr = simulate_round_robin(quantum=4)

    n = len(processes)
    results = [
        ("First-Come, First-Served (FCFS)", fcfs, "No", "Unacceptable: P2 waits behind P1"),
        ("Shortest Job First (SJF, Non-Preemptive)", sjf, "No", "Poor: long job blocks the queue"),
        ("Shortest Remaining Time First (SRTF)", srtf, "Yes", "Best average waiting time"),
        ("Preemptive Priority Scheduling", prio, "Yes", "Best for crisis alerts (P2 first)"),
        ("Round Robin (RR, Quantum = 4 ms)", rr, "Yes", "Fair, but P2 is delayed"),
    ]

    # Table 1: waiting time and turnaround time
    comp_rows = []
    for name, (wt, tat, ct, rt), preempt, note in results:
        comp_rows.append([
            name,
            f"{sum(wt.values()) / n:.2f}",
            f"{sum(tat.values()) / n:.2f}",
            f"{wt['P2']:.2f}",
            preempt,
            note,
        ])
    print_table(
        "CPU Scheduling Comparative Evaluation (Module 2)",
        ["Algorithm", "Avg WT (ms)", "Avg TAT (ms)", "P2 Crisis WT (ms)", "Preemptive?", "Remarks"],
        comp_rows,
    )

    # Table 2: response time and throughput
    resp_rows = []
    for name, (wt, tat, ct, rt), preempt, note in results:
        resp_rows.append([
            name,
            f"{sum(rt.values()) / n:.2f}",
            f"{rt['P2']:.2f}",
            f"{throughput(ct):.3f}",
            f"{max(ct.values())}",
        ])
    print_table(
        "Response Time and Throughput Analysis",
        ["Algorithm", "Avg RT (ms)", "P2 First Response (ms)", "Throughput (proc/ms)", "Total Time (ms)"],
        resp_rows,
    )

    print("\n[+] CONCLUSION & POLICY RECOMMENDATION:")
    print("    - SRTF and Preemptive Priority give the crisis task P2 a 0.00 ms wait and 0.00 ms response.")
    print("    - FCFS and non-preemptive SJF make P2 wait 7.00 ms behind routine work.")
    print("    - Recommended: 3-tier Multilevel Feedback Queue (MLFQ)")
    print("        Queue 0 -> crisis alerts (preemptive priority)")
    print("        Queue 1 -> interactive chat sessions (Round Robin)")
    print("        Queue 2 -> background batch jobs (FCFS)")
    print("=" * 80)


if __name__ == "__main__":
    main()
