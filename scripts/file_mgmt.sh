#!/usr/bin/env bash
# ==============================================================================
# Script 5: File Management - disk usage, large files and old log cleanup
# Course: Operating Systems (CCSE0303A) - Group 24 (NIET Greater Noida)
# Usage : ./file_mgmt.sh [directory] [days]
# Example: ./file_mgmt.sh /var/log/mental_health 7
# ==============================================================================
set -euo pipefail

TARGET_DIR="${1:-/var/log}"
OLD_DAYS="${2:-7}"

echo "=========================================================="
echo " FILE MANAGEMENT REPORT: $TARGET_DIR"
echo "=========================================================="

if [ ! -d "$TARGET_DIR" ]; then
    echo "[!] Directory '$TARGET_DIR' not found."
    echo "    Usage: $0 [directory] [days]"
    exit 1
fi

echo "--- Disk usage of this filesystem ---"
df -h "$TARGET_DIR"

echo ""
echo "--- 5 largest files ---"
find "$TARGET_DIR" -type f -printf '%s %p\n' 2>/dev/null | sort -rn | head -5 \
    | awk '{ size = $1/1048576; sub(/^[0-9]+ /, ""); printf "%8.2f MB  %s\n", size, $0 }' || true

echo ""
echo "--- Files older than $OLD_DAYS days ---"
find "$TARGET_DIR" -type f -mtime +"$OLD_DAYS" -print 2>/dev/null | head -20 || true

echo ""
echo "--- Deleting .log files older than $OLD_DAYS days ---"
COUNT=$(find "$TARGET_DIR" -type f -name "*.log" -mtime +"$OLD_DAYS" 2>/dev/null | wc -l)
find "$TARGET_DIR" -type f -name "*.log" -mtime +"$OLD_DAYS" -delete 2>/dev/null || true
echo "[+] Removed $COUNT old log file(s)."

echo ""
echo "--- Permissions of the directory ---"
ls -ld "$TARGET_DIR"
echo "=========================================================="
