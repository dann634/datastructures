import Call

class LiftPriorityQueue:
    def __init__(self):
        self.calls : [Call] = []

    def enqueue(self, call : Call):
        pass
        # Add call to the queue

    def dequeue(self, current_direction : str, current_floor : int):
        # Sort array and find floor with the highest priority (Internal over External)
        # Remove floor from the queue
        return # Floor with the highest priority