# SOC Incident Investigation: SSH Brute-Force Detection

## 1. Incident Summary

**Incident Type:** Simulated SSH brute-force activity  
**Environment:** Wazuh 4.14.10 SOC Lab  
**Affected Endpoint:** soc-ubuntu-01 (Ubuntu 24.04)  
**Source IP:** 192.0.2.51 (documentation/test address)  
**Detection Rule:** 5712  
**Alert Severity:** Level 10  
**Incident Date:** November 19, 2026  
**Status:** Detection and simulated response verified

### Executive Summary

A controlled SSH brute-force simulation was conducted against
a monitored Ubuntu endpoint by injecting synthetic SSH
authentication failures into a designated test log.

The Wazuh agent collected the events and forwarded them to the
Wazuh Manager for analysis.

Wazuh correlated repeated failed authentication attempts and
generated a Level 10 alert using Rule 5712.

The alert automatically triggered a custom Python active
response script, which recorded a simulated containment action.

No actual SSH attack or network-level blocking occurred.

## 2. Lab Environment

- Host operating system: Bazzite Linux
- Container platform: Rootless Podman
- Security monitoring platform: Wazuh 4.14.10
- Monitored endpoint: Ubuntu 24.04 container
- Agent: Wazuh Agent 4.14.10
- Log source: /var/log/soc-lab.log
- Detection engine: Wazuh Manager
- Response mechanism: Custom Python active response script

## 3. Detection Evidence

### Initial Authentication Detection

Wazuh Rule 5710 detected individual failed SSH authentication
attempts involving a nonexistent user.

- Rule ID: 5710
- Severity: Level 5
- Description: Attempt to login using a non-existent user

### Correlated Brute-Force Detection

Repeated authentication failures triggered Wazuh Rule 5712.

- Rule ID: 5712
- Severity: Level 10
- Description: sshd: brute force trying to get access to the system. Non existent user.
- Source IP: 192.0.2.51
- Endpoint: soc-ubuntu-01
- Alert timestamp: 2026-11-19T03:59:00.540+0000

## 4. MITRE ATT&CK Mapping

**T1110 — Brute Force**

Repeated authentication failures are consistent with
brute-force password guessing behavior.

**T1110.001 — Password Guessing**

The individual SSH authentication events represent simulated
password-guessing attempts against a nonexistent user.

These mappings describe the simulated technique and do not
establish that an actual adversary was present.

## 5. Investigation Timeline

| Time (UTC) | Event |
|---|---|
| 03:32:50–03:33:02 | Initial simulated SSH authentication failures detected |
| 03:32:56 | Initial Rule 5712 brute-force alert generated |
| 03:52:33 | Custom response script manually validated |
| 03:59:00.540 | New Rule 5712 alert generated for 192.0.2.51 |
| 03:59:00.554 | Automated simulated containment recorded |

## 6. Automated Incident Response

A custom Python script named `soc-lab-response.py` was
registered as a Wazuh active response command.

The script executes on the Wazuh Manager when Rule 5712
triggers.

It extracts the rule ID, source IP, and endpoint name from
the alert payload and records a simulated containment action.

### Verified Response Evidence

```text
2026-11-19T03:59:00.554849+00:00 | SIMULATED_BLOCK | source_ip=192.0.2.51 | rule_id=5712 | endpoint=soc-ubuntu-01
```

The response was triggered automatically following the
Rule 5712 alert.

**Important:** The script does not change firewall rules,
terminate connections, or block the source IP.

## 7. Investigation Findings

1. The Ubuntu agent successfully collected simulated SSH events.
2. Wazuh detected individual authentication failures.
3. Repeated failures triggered a correlated Level 10 alert.
4. The custom active response executed automatically.
5. The response log recorded the relevant source IP and endpoint.
6. No evidence of actual unauthorized access was established.

## 8. Recommended Remediation

For a real SSH brute-force incident, recommended actions include:

- Verify whether any authentication attempts succeeded.
- Review affected user accounts and authentication logs.
- Investigate the source IP and related activity.
- Enforce SSH key-based authentication where appropriate.
- Disable password authentication when operationally feasible.
- Apply rate limiting or temporary IP blocking after validation.
- Review exposed SSH services and access-control policies.
- Continue monitoring for repeated authentication attempts.

## 9. Outcome

The lab successfully demonstrated a detection-to-response
workflow involving endpoint log collection, alert correlation,
MITRE ATT&CK mapping, and automated simulated containment.

The exercise validates the configured Wazuh detection and
response workflow in a controlled environment.

## 10. Active Response Troubleshooting and Final Validation

During a subsequent validation test, Wazuh successfully generated a Rule 5712 brute-force alert, but the updated Python active response script did not record a new simulated containment event.

### Root Cause

The deployed Python script contained a leading newline before its shebang (`#!/usr/bin/env python3`).

Although the script passed Python syntax validation, direct execution failed with an `Exec format error` because the shebang was not located at the beginning of the file.

### Remediation

- Inspected the script's initial bytes using `od`.
- Identified the leading newline (`0a`) before the shebang.
- Removed the newline in VS Code.
- Redeployed the corrected script to the Wazuh Manager.
- Restored file ownership and executable permissions.
- Successfully validated direct execution.

### Final Automated Response Validation

A new controlled SSH brute-force simulation was generated using documentation IP address `192.0.2.54`.

The Wazuh environment subsequently recorded the following simulated containment action:

```text
2026-11-19T04:37:02.698587+00:00 | SIMULATED_BLOCK | source_ip=192.0.2.54 | rule_id=5712 | endpoint=soc-ubuntu-01
```

This confirmed that the corrected Python script could execute as part of the Wazuh active response workflow.

### Lessons Learned

Python syntax validation alone does not guarantee that a script can execute directly on Linux. Executable permissions, interpreter availability, and correct shebang placement must also be verified.

The investigation reinforced the importance of validating the complete security automation workflow after making code changes.

**Final outcome:** The lab successfully demonstrated simulated SSH brute-force detection and automated simulated incident response. No actual network containment was performed.