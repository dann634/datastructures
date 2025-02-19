import Call

class LiftQueue:
    def __init__(self):
        self.calls: [Call] = []

    def enqueue(self, call: Call, _=0):
        self.calls.append(call)


    def dequeue(self, ignore_weight, is_lift_full, current_floor, direction) -> Call:
        if not self.calls:
            return None

        requests_below = []
        requests_above = []
        requests_in_direction = None
        if not ignore_weight:
            if is_lift_full:
                for request in self.calls:
                    if request.requested_floor > current_floor and request.isInternal:
                        requests_above.append(request)
                    elif request.requested_floor < current_floor and request.isInternal:
                        requests_below.append(request)

                # If no requests found get other direction
                if (direction == "up" and len(requests_above) > 0) or len(requests_below) == 0:
                    requests_in_direction = requests_above
                elif (direction == "down" and len(requests_below) > 0) or len(requests_above) == 0:
                    requests_in_direction = requests_below


        else:
            if direction == "up":
                requests_in_direction = [call for call in self.calls if call.requested_floor >= current_floor]
            elif direction == "down":
                requests_in_direction = [call for call in self.calls if call.requested_floor <= current_floor]

        min_distance = float('inf')
        closest_request = None
        for call in requests_in_direction:
            distance = abs(call.requested_floor - current_floor)
            if distance < min_distance:
                min_distance = distance
                closest_request = call

        if closest_request:
            self.calls.remove(closest_request)
            return closest_request
        else:
            direction = "down" if direction == "up" else "up"
            return self.dequeue(ignore_weight, is_lift_full, current_floor, direction)



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