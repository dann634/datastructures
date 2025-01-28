from math import floor
from sys import float_repr_style

import pygame
import random

rand = random.Random()

floor_people = [] #2D list
floors = 5
image_sprites = []

pygame.init()
screen_width = 1000
screen_height_offset = 50
screen_height = screen_height_offset + (floors * 100)
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

tower_width = 600
floor_spacing = 100
tower_start_x = (screen_width / 2) - (tower_width / 2)
max_number_waiting = 10
lift_width = 100
lift_x = (screen_width / 2) - (lift_width / 2)
floors_available = []
person_spacing = 10
spawn_rate = 0.01
lift_capacity = 4

def draw_tower():
    for i in range(floors + 1):  # +1 to include the top floor line
        y = i * floor_spacing
        pygame.draw.line(screen, (0, 0, 0), (tower_start_x, y), (tower_start_x + tower_width, y), 2)  # Horizontal line
        # Draw the vertical edges
    pygame.draw.line(screen, (0, 0, 0), (tower_start_x, 0), (tower_start_x, floors * floor_spacing), 2)  # Left edge
    pygame.draw.line(screen, (0, 0, 0), (tower_start_x + tower_width, 0), (tower_start_x + tower_width, floors * floor_spacing),2)  # Right edge


def initialise_floors():
    global floor_people
    global floors_available
    for n in range(floors):
        floor_people.append([])
        floors_available.append(n)


def add_random_person():
    global floor_people
    person = Person()
    floor_people[person.starting_floor].append(person)
    image_sprites.append(person.get_sprite())


class Lift:
    def __init__(self):
        self.width = lift_width
        self.height = floor_spacing
        self.x = lift_x
        self.y = floors * floor_spacing - self.height  # Start at the bottom floor
        self.target_y = self.y  # Target position for smooth movement
        self.speed = 2  # Speed of lift movement
        self.is_stopped = False
        self.current_floor = 0
        self.people = []
        self.hasMovedPeople = False

    def draw(self):
        # Draw the lift as a rectangle
        pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, self.width, self.height))

    def move_to_floor(self, floor):
        # Set the target position based on the floor number
        self.target_y = floor * floor_spacing + (floor_spacing - self.height) / 2
        self.current_floor = floor

    def update(self):
        # Smooth movement towards the target_y
        if self.y < self.target_y:
            self.y = min(self.y + self.speed, self.target_y)
        elif self.y > self.target_y:
            self.y = max(self.y - self.speed, self.target_y)








def move_lift_people(lift):
    #People move out of lift if its their stop (add later)

    #People move into lift if waiting
    if len(lift.people) >= lift_capacity:
        return #Lift is full

    #Take as many people as possible
    amount_to_take = lift_capacity - len(lift.people)
    if amount_to_take < len(floor_people[lift.current_floor]):
        #More people than space
        for n in range(amount_to_take):
            person = floor_people[lift.current_floor][0]
            person.move_into_lift(len(lift.people))
            floor_people[lift.current_floor] = floor_people[lift.current_floor][1:] #Removes the person from list
    else:
        for person in floor_people[lift.current_floor]:
            person.move_into_lift(len(lift.people))
        floor_people[lift.current_floor] = []


def start_animation():

    lift = Lift()
    last_floor_change_time = 0

    run = True
    while run:

        clock.tick(120)

        if len(floors_available) > 0 and random.random() <= spawn_rate:
            add_random_person()

        if lift.y == lift.target_y and not lift.hasMovedPeople:
            move_lift_people(lift)
            lift.hasMovedPeople = True

        current_time = pygame.time.get_ticks()
        # Check if 3 seconds have passed since the last floor change
        if current_time - last_floor_change_time >= 3000:
            # Choose a random floor for the lift to move to
            current_floor = rand.randint(0, floors - 1)
            lift.hasMovedPeople = False
            lift.move_to_floor(current_floor)

            # Update the last floor change time
            last_floor_change_time = current_time

        lift.update()

        print(len(floor_people[lift.current_floor]))

        for person in floor_people:
            for p in person:
                p.move()
                sprite, position = p.get_sprite()
                screen.blit(sprite, (position[0] - p.radius, position[1] - p.radius))

        screen.fill((255, 255, 255))
        draw_tower()
        lift.draw()

        for sprite in image_sprites:
            screen.blit(sprite[0], sprite[1])

        pygame.display.flip()

    pygame.quit()



class Person:
    def __init__(self):
        self.radius = 15
        self.speed = 2

        self.starting_floor = rand.choice(floors_available)
        self.target_floor = rand.randint(0, floors - 1)

        if len(floor_people[self.starting_floor]) == max_number_waiting - 1:
            floors_available.remove(self.starting_floor)


        #Target floor cannot be the same as target floor
        while self.starting_floor == self.target_floor:
            self.target_floor = rand.randint(0, floors - 1)

        self.position = self._get_starting_position()
        self.target_position = self.position[:]


    def get_sprite(self):
        blue = (84, 150, 255)

        surface = pygame.Surface((self.radius*2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, blue, (self.radius, self.radius), self.radius)

        return surface, self.position

    def move(self):
        # Smooth movement towards the target position
        if self.position[1] < self.target_position[1]:
            self.position[1] = min(self.position[1] + self.speed, self.target_position[1])
        elif self.position[1] > self.target_position[1]:
            self.position[1] = max(self.position[1] - self.speed, self.target_position[1])

        if self.position[0] < self.target_position[0]:
            self.position[0] = min(self.position[0] + self.speed, self.target_position[0])
        elif self.position[0] > self.target_position[0]:
            self.position[0] = max(self.position[0] - self.speed, self.target_position[0])



    def move_into_lift(self, people_in_lift):
        #Figure out new location
        global lift_x
        x = lift_x
        y = self.position[1]
        if people_in_lift % 2 == 1:
            x += self.radius * 2

        self.target_position = [x, y]


    def _get_starting_position(self):

        #Determine which position it needs to go
        people_waiting = len(floor_people[self.starting_floor])

        #Get X coordinate
        x = tower_start_x + (tower_width / 2) - lift_width - ((people_waiting // 2) * 2 * self.radius) - (person_spacing * (people_waiting // 2))

        y = screen_height - screen_height_offset - (self.radius * 2) - (self.starting_floor * floor_spacing) - ((floor_spacing - (self.radius * 4)) / 2) + (person_spacing / 2)
        if len(floor_people[self.starting_floor]) % 2 == 0:
            y -= (self.radius * 2) + person_spacing

        return [x, y]









if __name__ == '__main__':
    initialise_floors()
    start_animation()