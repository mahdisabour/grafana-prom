from app.utils.exceptions import UnprocessableEntityException


def format_alert_message(data: str):
    try:
        alert = data["alerts"][0]
        alert_name = alert["labels"].get("alertname", "N/A")
        hostname = alert["labels"].get("hostname", "Unknown host")

        return f"{alert_name}\nhostname: {hostname}"
    except (KeyError, IndexError, TypeError) as e:
        raise UnprocessableEntityException("Error in message parsing")