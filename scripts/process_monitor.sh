#!/usr/bin/env bash
# ==============================================================================
# Script 2: Process & Resource Health Watchdog
# Domain: AI-Powered Mental Health Platform
# Course: Operating Systems (CCSE0303A) - Group 24 (NIET Greater Noida)
# ==============================================================================

LOG_FILE="/var/log/mental_health_os_monitor.log"
CPU_THRESHOLD=80
MEM_THRESHOLD=85

echo "=== Mental Health AI Process Health Inspection: $(date) ===" | tee -a "$LOG_FILE"

# 1. Inspect AI Inference Service Status
if pgrep -f "app.py" > /dev/null; then
    PID=$(pgrep -f "app.py" | head -n 1)
    CPU_USAGE=$(ps -p "$PID" -o %cpu= | awk '{print int($1)}')
    MEM_USAGE=$(ps -p "$PID" -o %mem= | awk '{print int($1)}')
    echo "[ONLINE] AI Pipeline (PID: $PID) - CPU: ${CPU_USAGE}% | Memory: ${MEM_USAGE}%" | tee -a "$LOG_FILE"

    if [ "$CPU_USAGE" -gt "$CPU_THRESHOLD" ]; then
        echo "[WARNING] High CPU consumption detected on AI Inference Process!" | tee -a "$LOG_FILE"
    fi
else
    echo "[CRITICAL ALERT] AI Mental Health Application is OFFLINE! Launching auto-restart..." | tee -a "$LOG_FILE"
    nohup python3 /opt/mental_health/app.py >> /var/log/ai_pipeline.log 2>&1 &
fi

# 2. Defunct / Zombie Process Detection
ZOMBIE_COUNT=$(ps aux | awk '{if ($8 ~ "Z") print $0}' | wc -l)
echo "[ZOMBIE PROCESS CHECK] Active Zombie/Defunct processes: $ZOMBIE_COUNT" | tee -a "$LOG_FILE"

# 3. Kernel Memory and Swap Statistics
echo "--- Memory & Swap Allocation ---" | tee -a "$LOG_FILE"
free -h | tee -a "$LOG_FILE"
