"""Task Scheduler Module.

This module provides utilities for scheduling and
running periodic automation tasks.
"""

import schedule
import time
from typing import Callable, Any


class TaskScheduler:
    """Handles scheduling and execution of tasks."""

    def __init__(self):
        """Initialize the TaskScheduler."""
        self.tasks: list[dict[str, Any]] = []
        self.running = False

    def add_task(
        self,
        func: Callable,
        interval: int,
        unit: str = "seconds"
    ) -> None:
        """Add a task to the schedule.

        Args:
            func: Function to run.
            interval: Interval between runs.
            unit: Time unit (seconds, minutes, hours, days).
        """
        if unit == "seconds":
            schedule.every(interval).seconds.do(func)
        elif unit == "minutes":
            schedule.every(interval).minutes.do(func)
        elif unit == "hours":
            schedule.every(interval).hours.do(func)
        elif unit == "days":
            schedule.every(interval).days.do(func)

        self.tasks.append({
            "func": func,
            "interval": interval,
            "unit": unit
        })

    def run_pending(self) -> None:
        """Run all pending tasks."""
        schedule.run_pending()

    def start(self, blocking: bool = True) -> None:
        """Start the scheduler.

        Args:
            blocking: Block main thread.
        """
        self.running = True

        if blocking:
            while self.running:
                self.run_pending()
                time.sleep(1)

    def stop(self) -> None:
        """Stop the scheduler."""
        self.running = False
        schedule.clear()

    def clear_tasks(self) -> None:
        """Clear all scheduled tasks."""
        schedule.clear()
        self.tasks.clear()


def run_once(func: Callable) -> None:
    """Run a function once immediately.

    Args:
        func: Function to run.
    """
    func()
