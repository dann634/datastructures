import Call

class LiftQueue:
    def __init__(self):
        self.calls: [Call] = []

    def enqueue(self, call: Call):
        self.calls.append(call)

    def dequeue(self, ignore_weight, is_lift_full):

        if not ignore_weight and is_lift_full:
            #Serve only internal calls
            call_found = None
            for call in self.calls:
                if call.isInternal:
                    call_found = call
                    break
            if call_found:
                self.calls.remove(call_found)
                return call_found

        if len(self.calls) > 0:
            return self.calls.pop(0)

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