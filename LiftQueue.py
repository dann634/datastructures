import Call

"""
A queue implementation that deals with internal and external requests
"""
class LiftQueue:
    def __init__(self):
        self.__calls: [Call] = []

    """
    Add a request to the queue
    
    Args:
        call (Call): the request to add
        _ (int): value not used here but in MinHeap.enqueue()
    """
    def enqueue(self, call: Call, _ : int = 0):
        self.__calls.append(call)

    """
    Removes the request from the front of the queue that has the highest priority
    
    Args:
        ignore_weight (bool): flag for whether to ignore weight or not
        is_lift_full (bool): flag for whether the lift is full or not
        current_floor (int): the current floor of the lift
        direction (str): the current direction of the lift
        
    Returns:
        Call: the next request
    """
    def dequeue(self, ignore_weight : bool, is_lift_full : bool, current_floor : int , direction : str) -> Call:

        # Null check
        if not self.__calls:
            return None

        # get all requests in the current direction
        if not ignore_weight and is_lift_full:
            # All these requests must be internal (priority call)
            if direction == "up":
                requests_in_direction = [call for call in self.__calls if call.requested_floor >= current_floor and call.isInternal]
            elif direction == "down":
                requests_in_direction = [call for call in self.__calls if call.requested_floor <= current_floor and call.isInternal]

        else:
            # All these requests can be either internal or external
            if direction == "up":
                requests_in_direction = [call for call in self.__calls if call.requested_floor >= current_floor]
            elif direction == "down":
                requests_in_direction = [call for call in self.__calls if call.requested_floor <= current_floor]

        # get the closest call
        min_distance = float('inf')
        closest_request = None
        for call in requests_in_direction:
            distance = abs(call.requested_floor - current_floor)
            if distance < min_distance:
                min_distance = distance
                closest_request = call

        # if a call has been found remove it from the internal list and remove it
        if closest_request:
            self.__calls.remove(closest_request)
            return closest_request
        else:
            direction = "down" if direction == "up" else "up"
            return self.dequeue(ignore_weight, is_lift_full, current_floor, direction)


    """
    Returns the length of the internal list
    """
    def size(self) -> int:
        return len(self.__calls)