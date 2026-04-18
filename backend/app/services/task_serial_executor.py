import threading
from typing import Any, Callable


class SerialTaskExecutor:
    """串行任务执行器，用锁保证同时只有一个任务在执行。"""

    def __init__(self):
        self._lock = threading.Lock()

    def run(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        with self._lock:
            return fn(*args, **kwargs)

    def shutdown(self, wait: bool = True):
        pass


task_serial_executor = SerialTaskExecutor()
