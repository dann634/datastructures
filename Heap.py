class MinHeap:
    def __init__(self):
        self.heap = []

    def size(self):
        return len(self.heap)

    def getParentIndex(self, index):
        return (index - 1) // 2

    def getLeftChildIndex(self, index):
        return 2 * index + 1

    def getRightChildIndex(self, index):
        return 2 * index + 2

    def hasParent(self, index):
        return self.getParentIndex(index) >= 0

    def hasLeftChild(self, index):
        return self.getLeftChildIndex(index) < len(self.heap)

    def hasRightChild(self, index):
        return self.getRightChildIndex(index) < len(self.heap)

    def parent(self, index):
        return self.heap[self.getParentIndex(index)]

    def leftChild(self, index):
        return self.heap[self.getLeftChildIndex(index)]

    def rightChild(self, index):
        return self.heap[self.getRightChildIndex(index)]

    def swap(self, element1, element2):
        self.heap[element1], self.heap[element2] = self.heap[element2], self.heap[element1]

    def insert(self, item):
        self.heap.append(item)
        self.heapify_up()

    def heapify_up(self):
        index = len(self.heap) - 1
        while (self.hasParent(index) and self.parent(index) > self.heap[index]):
            self.swap(self.getParentIndex(index), index)
            index = self.getParentIndex(index)

    def remove_min(self):
        if not self.heap:
            return ("empty heap")
        minItem = self.heap[0]
        self.heap[0] = self.heap[len(self.heap) - 1]
        self.heap.pop()
        self.heapify_down(0)
        return minItem

    def heapify_down(self, index):
        smallest = index
        if (self.hasLeftChild(index) and self.heap[smallest] > self.leftChild(index)):
            smallest = self.getLeftChildIndex(index)
        if (self.hasRightChild(index) and self.heap[smallest] > self.rightChild(index)):
            smallest = self.getRightChildIndex(index)
        if (smallest != index):
            self.swap(index, smallest)
            self.heapify_down(smallest)

def dequeue_heap():
    heap = MinHeap()
    direction = 1
    current_floor = 0
    requests = []

    for requestFloor in requests:
        distance = abs(requestFloor - current_floor)
        heap.insert((distance, requestFloor))

    distance, next_floor = heap.remove_min()
    next_floor = int(next_floor)

    if next_floor > current_floor:
        direction = 1
    else:
        direction = -1
    while current_floor != next_floor:
        current_floor += direction

    if heap.size() > 0:
        refreshing_requests = []
        while heap.size() > 0:
            distance, req_floor = heap.remove_min()
            req_floor = int(req_floor)
            refreshing_requests.append(req_floor)
        for req_floor in refreshing_requests:
            updated_dist = abs(req_floor - current_floor)
            heap.insert((updated_dist, req_floor))

    return next_floor