import Call

class LiftQueue:
    def __init__(self):
        self.calls: [Call] = []

    def enqueue(self, call: Call):
        self.calls.append(call)

    def dequeue(self, ignore_weight, is_lift_full):

        if not ignore_weight and is_lift_full:
            #Serve only internal calls
            for call in self.calls:
                if call.isInternal:
                    self.calls.remove(call)
                    return call

        if len(self.calls) > 0:
            call = self.calls[0]
            self.calls.remove(call)
            return call
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

    def size(self):
        return len(self.calls)