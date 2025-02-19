import Call

class LiftQueue:
    def __init__(self):
        self.calls: [Call] = []

    def enqueue(self, call: Call, _=0):
        self.calls.append(call)

    def dequeue(self, ignore_weight, is_lift_full) -> Call:
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

    def dequeue_look(self, ignore_weight, is_lift_full, current_floor, direction) -> Call:
        if not ignore_weight and is_lift_full:
            # Serve only internal calls

            call_found = None
            for call in self.calls:
                if call.isInternal:
                    call_found = call
                    if current_floor < call.requested_floor and direction == "up":
                        break
                    elif current_floor < call.requested_floor and direction == "down":
                        break
            if call_found:
                self.calls.remove(call_found)
                return call_found

        if len(self.calls) > 0:
            return self.calls.pop(0)

        return None




    def peek(self):
        return self.calls[0] if self.calls else None

    def dequeue_index(self, index):
        if len(self.calls) > 0:
            return self.calls.pop(index)

    def peek_index(self, index):
        return self.calls[index] if self.calls else None

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