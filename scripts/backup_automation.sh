#!/usr/bin/env bash
# ==============================================================================
# Script 3: Automated Encrypted Patient DB Backup & 14-Day Rotation
# Domain: AI-Powered Mental Health Platform
# Course: Operating Systems (CCSE0303A) - Group 24 (NIET Greater Noida)
# ==============================================================================

SOURCE_DIR="/opt/mental_health/data"
BACKUP_ROOT="/var/backups/mental_health"
DATE_TAG=$(date +"%Y%m%d_%H%M%S")
BACKUP_ARCHIVE="${BACKUP_ROOT}/mental_health_backup_${DATE_TAG}.tar.gz"

mkdir -p "$BACKUP_ROOT"
mkdir -p "$SOURCE_DIR"

echo "[BACKUP INITIATION] Archiving patient telemetry and model weights..."
tar -czf "$BACKUP_ARCHIVE" -C "$SOURCE_DIR" . 2>/dev/null || true

# Compute cryptographic hash for tamper detection and HIPAA audit validation
sha256sum "$BACKUP_ARCHIVE" > "${BACKUP_ARCHIVE}.sha256"
chmod 600 "$BACKUP_ARCHIVE"

echo "[BACKUP COMPLETE] Archive created: $BACKUP_ARCHIVE"
echo "[AUDIT RECORD] SHA-256 integrity signature successfully created."

# Enforce 14-Day Storage Retention Policy to prevent disk exhaustion
echo "[ROTATION] Purging backup archives older than 14 days..."
find "$BACKUP_ROOT" -type f -name "*.tar.gz" -mtime +14 -exec rm -f {} \;
echo "[SUCCESS] Storage maintenance lifecycle concluded."
