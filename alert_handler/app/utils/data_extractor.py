from app.utils.exceptions import UnprocessableEntityException


def format_alert_message(data: dict) -> str:
    try:
        alerts = data.get("alerts", [])
        if not alerts:
            raise UnprocessableEntityException("No alerts found in message")

        alert_name = data.get("commonLabels", {}).get("alertname", "N/A")
        message_lines = [f"ALERT GROUP: {alert_name}"]
        message_lines.append("Details:\n")

        for idx, alert in enumerate(alerts, start=1):
            hostname = alert.get("labels", {}).get("hostname", "Unknown host")
            instance = alert.get("labels", {}).get("instance", "N/A")

            message_lines.append(
                f"Host: {hostname}\n"
                f"Instance: {instance}\n"
            )

        return "\n".join(message_lines)

    except (KeyError, IndexError, TypeError) as e:
        raise UnprocessableEntityException("Error in message parsing")
