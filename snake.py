from etherlight import Etherlight
import time
from random import randint
from threading import Thread

ETHERLIGHTS = ["10.0.10.36", "10.0.10.6"]


class SnakeGame:
    def __init__(self):
        self.FIELD_WIDTH = 24
        self.FIELD_HEIGHT = len(ETHERLIGHTS) * 2
        self.etherlights = [Etherlight(ip) for ip in ETHERLIGHTS]
        self.head = [0, 0]
        self.tail = []
        self.direction = 'R'
        self.fruit = [0, 0]
        self.delay = 0.2
        self.display = self.get_display()
        self.running = False
        self.reset_game()

    def reset_game(self):
        self.head = [0, 0]
        self.tail = []
        self.direction = 'R'
        self.spawn_fruit()
        self.display = self.get_display()
        self.running = False

    def spawn_fruit(self):
        while True:
            fruit = [randint(0, self.FIELD_WIDTH - 1), randint(0, self.FIELD_HEIGHT - 1)]
            if fruit not in self.tail and fruit != self.head:
                self.fruit = fruit
                break

    def get_display(self):
        display = [['x' for _ in range(self.FIELD_WIDTH)] for _ in range(self.FIELD_HEIGHT)]
        display[self.fruit[1]][self.fruit[0]] = 'F'
        for i in self.tail:
            display[i[1]][i[0]] = self.tail.index(i) + 1
        display[self.head[1]][self.head[0]] = 'H'
        return display

    def move(self):
        self.tail.insert(0, self.head.copy())
        old_head = self.head
        # Update head position based on direction
        self.head[0] += {"R": 1, "L": -1, "U": 0, "D": 0}[self.direction]
        self.head[1] += {"R": 0, "L": 0, "U": -1, "D": 1}[self.direction]

        # Check for eating fruit
        if self.head == self.fruit:
            print("Eating")
            self.spawn_fruit()
        else:
            self.tail.pop()

        # Check for collision or out of bounds
        if (self.head in self.tail or
                0 > self.head[0] or self.head[0] >= self.FIELD_WIDTH or
                0 > self.head[1] or self.head[1] >= self.FIELD_HEIGHT):
            print("Collision" if self.head in self.tail else "Out of bounds")
            return False

        return True

    def draw(self):
        self.display = self.get_display()
        print(f"=== dir {self.direction}; head {self.head}; fruit {self.fruit}; tail {self.tail} ===")
        for line in self.display:
            print("".join(line))
        self.update_etherlight()
        print("===")

    def update_etherlight(self):
        for y in range(self.FIELD_HEIGHT):
            for x in range(self.FIELD_WIDTH):
                if self.display[y][x] != 'x':
                    etherlight = self.etherlights[int(y / 2)]
                    led = (x * 2) + (y % 2)
                    color = {
                        'x': [0, 0, 0],
                        'T': [0, 255, 0],
                        'H': [0, 0, 255],
                        'F': [255, 0, 0],
                    }.get(self.display[y][x], [0, min(255, (self.display[y][x] - 2) * 10), 155 - (self.display[y][x] - 2) * 5])
                    etherlight.set_led_color(led, color)
        
