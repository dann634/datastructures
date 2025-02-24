"""
Request object used by LiftManager
"""
class Call:
    def __init__(self, requested_floor : int, isInternal : bool):
        self.requested_floor : int = requested_floor
        self.isInternal : bool = isInternal