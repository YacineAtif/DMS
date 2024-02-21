from datetime import datetime


def get_current_timestamp():
    # Format the datetime string to include up to seconds (YYYY-MM-DD HH:MM:SS)
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
