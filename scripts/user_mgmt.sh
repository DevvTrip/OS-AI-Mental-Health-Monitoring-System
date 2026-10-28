#!/usr/bin/env bash
# ==============================================================================
# Script 1: User & Role-Based Access Control (RBAC) Management
# Domain: AI-Powered Mental Health Platform
# Course: Operating Systems (CCSE0303A) - Group 24 (NIET Greater Noida)
# ==============================================================================

set -euo pipefail

echo "=========================================================="
echo " [MENTAL-HEALTH-OS] Configuring Clinical Roles & Access    "
echo "=========================================================="

# 1. Define and create system groups for strict principle of least privilege
GROUPS=("neuro_admins" "ai_engineers" "clinical_staff" "audit_sec")
for grp in "${GROUPS[@]}"; do
    if getent group "$grp" >/dev/null 2>&1; then
        echo "[+] Group '$grp' already exists."
    else
        groupadd "$grp"
        echo "[+] Created system group: $grp"
    fi
done

# 2. Provision clinical user accounts with restricted home directory permissions
create_user_account() {
    local username="$1"
    local group="$2"
    if id "$username" >/dev/null 2>&1; then
        echo "[*] User '$username' already exists."
    else
        useradd -m -g "$group" -s /bin/bash "$username"
        echo "[+] Created user: $username (Assigned group: $group)"
    fi
}

create_user_account "dr_tripathi" "clinical_staff"
create_user_account "ai_dev_manas" "ai_engineers"
create_user_account "auditor_hardik" "audit_sec"

# 3. Create isolated HIPAA-compliant clinical vault directory
VAULT_DIR="/opt/mental_health/patient_vault"
mkdir -p "$VAULT_DIR"
chown root:clinical_staff "$VAULT_DIR"
chmod 770 "$VAULT_DIR"

echo "[+] Secured Directory: $VAULT_DIR with mode 770 (Isolated to clinical staff only)."
echo "[SUCCESS] Clinical user and permission hierarchy provisioned successfully."
