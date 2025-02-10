import Call

class LiftQueue:
    def __init__(self):
        self.calls: [Call] = []

    def enqueue(self, call: Call):
        if self.contains(call.requested_floor):
            return
        self.calls.append(call)

    def dequeue(self):
        if len(self.calls) > 0:
            return self.calls.pop()
        return None

    def peek(self):
        return self.calls[0] if self.calls else None


    def contains(self, floor):
        for call in self.calls:
            if call.requested_floor == floor:
                return True
        return False


    def isEmpty(self):
        return len(self.calls) == 0

    def print_calls(self):
        list = []
        for call in self.calls:
            list.append(call.requested_floor)

        print(list)