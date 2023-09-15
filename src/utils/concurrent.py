import threading
from typing import Callable


def Thread(job: Callable):
    thread = threading.Thread(target=job)
    thread.start()
    return thread