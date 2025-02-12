import Call


class LiftQueue:
    def __init__(self):
        self.calls: [Call] = []
        self.frontPointer = 0
        self.rearPointer = -1

    def enqueue(self, call: Call):
        self.rearPointer += 1
        self.calls.append(call)

    def dequeue(self):
        if self.rearPointer < self.frontPointer:
            return None
        call = self.calls[self.frontPointer]
        self.frontPointer += 1
        return call

    def contains(self, floor):
        for call in self.calls:
            if call.requested_floor == floor:
                return True
        return False

    def isEmpty(self):
        return len(self.calls) == 0
