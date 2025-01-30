from LiftSystem import Lift

lift = Lift(10,4)
lift.external_request(3,"up")
lift.internal_request(7)
lift.internal_request(3)
print(lift.get_internal_requests())
print(lift.get_external_requests())

lift.internal_request(4)
lift.external_request(3, "up")

lift.get_external_requests()
lift.get_internal_requests()

lift.clear_request(2)
