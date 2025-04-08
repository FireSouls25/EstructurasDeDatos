import time

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None

    def initialize(self, limit):
        prev_node = None
        for i in range(limit):
            node = Node(i)
            if not self.head:
                self.head = node
            else:
                node.prev = prev_node
                prev_node.next = node
            prev_node = node
        # cerrar la lista
        self.head.prev = prev_node
        prev_node.next = self.head

class Hand:
    def __init__(self, limit):
        self.list = CircularDoublyLinkedList()
        self.list.initialize(limit)
        self.current = self.list.head

    def tick(self):
        self.current = self.current.next

    def value(self):
        return self.current.value

class Clock:
    def __init__(self):
        self.second_hand = Hand(60)
        self.minute_hand = Hand(60)
        self.hour_hand = Hand(12)
        self.second_ticks = 0

    def tick(self):
        self.second_hand.tick()
        self.second_ticks += 1

        if self.second_ticks % 60 == 0:
            self.minute_hand.tick()
            if self.minute_hand.value() % 5 == 0:
                self.hour_hand.tick()

    def display(self):
        h = self.hour_hand.value()
        m = self.minute_hand.value()
        s = self.second_hand.value()
        return f"{h:02}:{m:02}:{s:02}"

if __name__ == '__main__':
    clock = Clock()
    while True:
        print(clock.display())
        clock.tick()
        time.sleep(1)
