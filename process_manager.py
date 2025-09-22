import random
import time

class Process:
    def __init__(self, pid, memory_required):
        self.pid = pid
        self.memory_required = memory_required
        self.created_time = time.strftime('%H:%M:%S')

    def __repr__(self):
        return f"Process(pid={self.pid}, memory={self.memory_required}, created={self.created_time})"

class ProcessManager:
    def __init__(self):
        self.process_list = []

    def create_process(self):
        pid = len(self.process_list) + 1
        memory_required = random.randint(1, 5)
        process = Process(pid, memory_required)
        self.process_list.append(process)
        return process

    def get_processes(self):
        return [{
            "PID": p.pid,
            "Memory Required": p.memory_required,
            "Created": p.created_time
        } for p in self.process_list]

    def remove_last_process(self):
        if self.process_list:
            self.process_list.pop()

    def clear_processes(self):
        self.process_list = []

    def __str__(self):
        return "\n".join(str(p) for p in self.process_list)
