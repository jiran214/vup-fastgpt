import threading
from typing import Callable


def start_thread(job: Callable):
    thread = threading.Thread(target=job)
    thread.start()
    return thread