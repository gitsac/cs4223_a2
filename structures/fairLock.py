import threading
from collections import deque

class FCFSLock:
    def __init__(self):
        self._queue = deque()
        self._lock = threading.Lock()
        self._current_holder = None
    
    def acquire(self):
        thread_id = threading.get_ident()
        event = threading.Event()
        
        with self._lock:
            if self._current_holder is None and not self._queue:
                self._current_holder = thread_id
                return
            self._queue.append((thread_id, event))
        
        event.wait()
    
    def release(self):
        with self._lock:
            self._current_holder = None
            if self._queue:
                next_thread_id, next_event = self._queue.popleft()
                self._current_holder = next_thread_id
                next_event.set()