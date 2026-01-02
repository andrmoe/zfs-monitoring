import configparser
from typing import Tuple, Optional
from pathlib import Path
import caldav
from datetime import datetime, timezone
import uuid

def load_config() -> Optional[Tuple[str, str, str, str]]:
    """Reads CalDAV credentials and calendar name from config.ini."""
    config = configparser.ConfigParser()
    config.read(Path.home() / "zfs-monitoring" / "config.ini")
    url = config["caldav"]["url"]
    username = config["caldav"]["username"]
    password = config["caldav"]["password"]
    calendar_name = config["caldav"]["calendar_name"]
    return url, username, password, calendar_name


def send_todo(todo_str: str):
    url, username, password, calendar_name = load_config()
    with caldav.DAVClient(
        url=url, username=username, password=password
    ) as client:
        principal = client.principal()
        
        # Find the specific calendar by its display name
        target_calendar = None
        for cal in principal.calendars():
            if cal.name == calendar_name:
                target_calendar = cal
                break
        
        if not target_calendar:
            raise EnvironmentError(f"Error: Calendar '{calendar_name}' not found.")

        target_calendar.add_todo(f"BEGIN:VTODO\n"+
                                 f"UID:"+str(uuid.uuid4())+"@zfs-monitoring\n"+
                                 f"DTSTAMP:"+str(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))+"\n"+
                                 f"SUMMARY:{todo_str}\n"+
                                 f"END:VTODO")
