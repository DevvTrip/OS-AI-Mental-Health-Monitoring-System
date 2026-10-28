#!/usr/bin/env bash
# ==============================================================================
# Script 4: Hardware, Kernel & IPC Telemetry Diagnostic
# Domain: AI-Powered Mental Health Platform
# Course: Operating Systems (CCSE0303A) - Group 24 (NIET Greater Noida)
# ==============================================================================

echo "=========================================================="
echo "    CLINICAL OS INFRASTRUCTURE HEALTH & IPC DIAGNOSTICS   "
echo "=========================================================="
echo "Host Kernel Version: $(uname -r)"
echo "Machine Architecture: $(uname -m)"
echo "Host Uptime:         $(uptime -p)"
echo ""

echo "--- Physical Storage Mounts & Inode Allocation ---"
df -h --output=source,fstype,size,used,avail,pcent,target -x tmpfs -x devtmpfs

echo ""
echo "--- Context Switching & Interrupt Latency (vmstat) ---"
vmstat 1 2

echo ""
echo "--- Inter-Process Communication (Shared Memory & Semaphores) ---"
ipcs -m -s || true

echo "=========================================================="
