from Call import Call


class MinHeap:
    def __init__(self):
        self.__heap : [(Call, int)] = []

    """
    Returns number of elements in the heap
    """
    def size(self) -> int:
        return len(self.__heap)

    """
    Returns index of parent node, given an index
    """
    def __get_parent_index(self, index : int) -> int:
        return (index - 1) // 2

    """
    Returns index of left child node
    """
    def __get_left_child_index(self, index : int) -> int:
        return 2 * index + 1

    """
    Returns index of right child node
    """
    def __get_right_child_index(self, index : int) -> int:
        return 2 * index + 2

    """
    Returns if a node has a parent
    """
    def __has_parent(self, index : int) -> bool:
        return self.__get_parent_index(index) >= 0

    """
    Returns if a node has a child on its left
    """
    def __has_left_child(self, index : int) -> bool:
        return self.__get_left_child_index(index) < len(self.__heap)


    """
    Returns if a node has a child on its right
    """
    def __has_right_child(self, index : int) -> bool:
        return self.__get_right_child_index(index) < len(self.__heap)


    """
    Returns the parent node of the node at index
    """
    def __parent(self, index : int) -> (Call, int):
        return self.__heap[self.__get_parent_index(index)]

    """
    Returns the left child node of the node at index
    """
    def __left_child(self, index : int) -> (Call, int):
        return self.__heap[self.__get_left_child_index(index)]


    """
    Returns the right child node of the node at index
    """
    def __right_child(self, index : int) -> (Call, int):
        return self.__heap[self.__get_right_child_index(index)]

    """
    Swaps two elements in the heap
    """
    def __swap(self, element1 : int, element2 : int):
        self.__heap[element1], self.__heap[element2] = self.__heap[element2], self.__heap[element1]

    """
    Adds a new element into the heap
    """
    def __insert(self, item : (Call, int)):
        self.__heap.append(item)
        self.__heapify_up()

    """
    Restores min-heap property
    Used after insertion
    """
    def __heapify_up(self):
        index = len(self.__heap) - 1
        while self.__has_parent(index) and self.__parent(index)[0] > self.__heap[index][0]:
            self.__swap(self.__get_parent_index(index), index)
            index = self.__get_parent_index(index)

    """
    Removes and returns the smallest element in the heap
    """
    def __remove_min(self):
        if not self.__heap:
            return None
        min_item = self.__heap[0]
        self.__heap[0] = self.__heap[len(self.__heap) - 1]
        self.__heap.pop()
        self.__heapify_down(0)
        return min_item


    """
    Moves the root element into the correct location
    
    Args:
        index (int): index of element
    """
    def __heapify_down(self, index : int):
        smallest = index
        if self.__has_left_child(index) and self.__heap[smallest][0] > self.__left_child(index)[0]:
            smallest = self.__get_left_child_index(index)
        if self.__has_right_child(index) and self.__heap[smallest][0] > self.__right_child(index)[0]:
            smallest = self.__get_right_child_index(index)
        if smallest != index:
            self.__swap(index, smallest)
            self.__heapify_down(smallest)


    """
    Adds a new call to the heap
    
    Args:
        request (Call): the call to be added to the heap
        current_floor (int): the current floor of the lift
    """
    def enqueue(self, request : Call, current_floor : int = 0):
        target_floor = request.requested_floor
        distance = abs(target_floor - current_floor)
        self.__insert((distance, request))


    """
    Returns the next best call from the heap
    
    Args:
        current_floor (int): the current floor of the lift
        
    Returns:
        Call: the next call
    """
    def dequeue(self, current_floor : int) -> int:
        if self.size() == 0:
            return -1

        distance, next_request = self.__remove_min()
        next_floor = next_request.requested_floor

        # Move towards the next request's floor
        direction = 1 if next_floor > current_floor else -1
        while current_floor != next_floor:
            current_floor += direction

        # Instead of clearing the __heap, update the distances directly
        for i in range(self.size()):
            distance, request = self.__heap[i]
            updated_distance = abs(request.requested_floor - current_floor)
            self.__heap[i] = (updated_distance, request)

        # Restore __heap order efficiently
        self.__heapify_down(0)

        return next_floor
