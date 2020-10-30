import sys
import time
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# NOTE: a special observer is required on a CIFS filesystem

