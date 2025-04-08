from Reloj import Clock

class ClockController:
    def __init__(self, reloj: Clock):
        self.clock = reloj

    def set_time(self, hour: int, minute: int, second: int):
        while self.clock.hour_hand.value() != hour % 12:
            self.clock.hour_hand.tick()
        while self.clock.minute_hand.value() != minute % 60:
            self.clock.minute_hand.tick()
        while self.clock.second_hand.value() != second % 60:
            self.clock.second_hand.tick()

    def set_by_angle(self, hand_type: str, angle: float):
        if hand_type == "hour":
            target = int((angle % 360) / 30)
            while self.clock.hour_hand.value() != target:
                self.clock.hour_hand.tick()
        elif hand_type == "minute":
            target = int((angle % 360) / 6)
            while self.clock.minute_hand.value() != target:
                self.clock.minute_hand.tick()
        elif hand_type == "second":
            target = int((angle % 360) / 6)
            while self.clock.second_hand.value() != target:
                self.clock.second_hand.tick()
