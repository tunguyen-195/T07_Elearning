import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None

    def on_any_event(self, event):
        if event.is_directory:
            return
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(self.command, shell=True)

if __name__ == "__main__":
    path = "."  # Watch the current directory
    command = "flask run"  # Command to restart the server
    event_handler = ChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()