import Call

class LiftQueue:
    def __init__(self):
        self.calls: [Call] = []

    def enqueue(self, call: Call):
        self.calls.append(call)

    def dequeue(self):
        if self.calls:
            return self.calls.pop(0)
        return None

    def peek(self):
        return self.calls[0] if self.calls else None