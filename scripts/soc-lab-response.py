#!/usr/bin/env python3

import json
import sys
from datetime import datetime, timezone

LOG_FILE = "/var/ossec/logs/soc-lab-response.log"
TARGET_RULE = "5712"


def safe_value(value):
    """Remove control characters from logged values."""
    if not isinstance(value, (str, int, float)):
        return "unknown"

    return str(value).replace("\n", "").replace("\r", "").replace("|", "_")


def main():
    try:
        message = json.loads(sys.stdin.readline())

        if not isinstance(message, dict):
            raise ValueError("Invalid response message format")

        if message.get("command") != "add":
            return

        parameters = message.get("parameters", {})
        if not isinstance(parameters, dict):
            raise ValueError("Invalid parameters format")

        alert = parameters.get("alert", {})
        if not isinstance(alert, dict):
            raise ValueError("Invalid alert format")

        rule = alert.get("rule", {})
        data = alert.get("data", {})
        agent = alert.get("agent", {})

        if not all(isinstance(item, dict) for item in (rule, data, agent)):
            raise ValueError("Invalid alert field structure")

        rule_id = safe_value(rule.get("id"))
        source_ip = safe_value(data.get("srcip"))
        endpoint = safe_value(agent.get("name"))

        if rule_id != TARGET_RULE:
            return

        timestamp = datetime.now(timezone.utc).isoformat()

        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(
                f"{timestamp} | SIMULATED_BLOCK | "
                f"source_ip={source_ip} | "
                f"rule_id={rule_id} | "
                f"endpoint={endpoint}\n"
            )

    except (ValueError, TypeError, OSError) as error:
        print(f"Response error: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()
