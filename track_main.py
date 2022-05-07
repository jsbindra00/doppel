from InputTracker import InputTracker
from documentutil import writeFile

tracker = InputTracker()
tracker.startTracking(writeFile,track_mouse=True, track_keyboard=True, print_events=True)
tracker.Join()
