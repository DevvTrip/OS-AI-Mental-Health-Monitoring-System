# AI – Powered Mental Health Monitoring System
### Intelligent Operating System Resource Management Framework
**Course:** Operating Systems (CCSE0303A) - Project-Based Learning (PBL)  
**Institution:** Noida Institute of Engineering & Technology (NIET), Greater Noida  
**Department:** Department of Artificial Intelligence  
**Group:** Group 24 | **Semester:** 3rd | **Academic Year:** 2026–2027  
**Faculty Coordinator:** Mr. Manish Choudhary  
**Target SDG:** SDG 3 – Good Health & Well-being  

---

## 👥 Group Members & Roles

| S# | Student Name | College / Univ Roll No. | Assigned Role in Project | Module Responsibility |
| :-: | :--- | :---: | :--- | :--- |
| **1** | **Devvrat Tripathi** *(Team Lead)* | 0251CSAI231 / 2501331520078 | Team Lead & System Analyst | Architecture, PCB Lifecycle & Synthesis |
| **2** | **Manas Srivastava** | 0251CSAI144 | Linux & Scheduling Specialist | Shell Scripts & CPU Scheduling Algorithms |
| **3** | **Pranjal Sharma** | 0251CSAI141 | Performance & Optimization Specialist | Readers-Writers Locks, Paging & LRU Cache |
| **4** | **Hardik Kumar** | 0251CSAI195 | Security & Reliability Specialist | Banker's Algorithm Deadlock & C-LOOK I/O |
| **5** | **Mritunjay Gupta** | 0251CSAI132 | Modern OS & Documentation Specialist | Docker Virtualization, CUDA & Documentation |

---

## 📁 Project File Inventory

| File / Folder Path | Description |
| :--- | :--- |
| `app.py` | Main orchestrator: Multithreading, Writer-Preference RW Locks, Banker's Algorithm deadlock avoidance, and LRU Page Cache with AI sentiment evaluation. |
| `scheduler_benchmark.py` | CPU Scheduling simulation engine evaluating FCFS, SJF, SRTF, Priority, and Round Robin on clinical AI workload. |
| `OS_PBL_REPORT_GROUP_24.docx` | **Official Academic Report** in Microsoft Word format, strictly styled in Times New Roman, 12pt, 1.5 line spacing, 1-inch margins, with all 21 prescribed sections. |
| `OS_PBL_REPORT_GROUP_24.md` | Complete Academic Report in Markdown format. |
| `requirements.txt` | Python package specifications. |
| `generate_report_docx.py` | Generator script that compiles `OS_PBL_REPORT_GROUP_24.docx`. |
| `scripts/user_mgmt.sh` | Linux user & role-based access control (RBAC) script with 770 patient vault isolation. |
| `scripts/process_monitor.sh` | Process health, CPU/memory threshold watchdog, and auto-restart service. |
| `scripts/backup_automation.sh` | Automated encrypted patient DB backup with SHA-256 integrity and 14-day rotation. |
| `scripts/system_health.sh` | Hardware telemetry, kernel version, context switching, and IPC monitoring. |
| `scripts/file_mgmt.sh` | Disk usage report, 5 largest files and cleanup of old `.log` files. |

---

## 🚀 Execution Instructions

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Run Main AI & OS Pipeline
Demonstrates concurrent ingestion, Banker's Algorithm deadlock-free safety sequence validation, and LRU demand-paging cache:
```powershell
python app.py
```

### 3. Run CPU Scheduling Benchmark
Simulates and displays the performance comparison table (Waiting Time, Turnaround Time, and Preemption metrics):
```powershell
python scheduler_benchmark.py
```

### 4. Re-compile Word Document (Optional)
If you make any changes to the report generator, you can re-build the `.docx` file anytime by running:
```powershell
python generate_report_docx.py
```
