import random

import pygame

from LiftManager import LiftManager
from SCAN import scan
from LOOK import look
from LiftQueue import LiftQueue
from Call import Call

rand = random.Random()

floor_people = [] #2D list
floors = 7
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
max_number_waiting = 6
lift_width = 100
lift_x = (screen_width / 2) - (lift_width / 2)
lift_y = (floors - 1) * floor_spacing
floors_available = []
person_spacing = 10
spawn_rate = 0.02
lift_capacity = 4
people_leaving = []
game_speed = 2
lift_wait_delay = 1000

people_count = 50

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
        self.y = lift_y  # Start at floor 0
        self.target_y = self.y  # Target position for smooth movement
        self.speed = game_speed  # Speed of lift movement
        self.is_stopped = False
        self.current_floor = 0
        self.people : [Person] = []
        self.hasMovedPeople = False
        self.target_floor = self.current_floor
        self.open_spaces = []

    def draw(self):
        # Draw the lift as a rectangle
        pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, self.width, self.height))

    def move_to_floor(self, floor):
        # Set the target position based on the floor number
        self.target_y = (floors - 1 - floor) * floor_spacing + (floor_spacing - self.height) / 2
        self.target_floor = floor

    def update(self):
        # Smooth movement towards the target_y
        if self.y < self.target_y:
            self.y = min(self.y + self.speed, self.target_y)
        elif self.y > self.target_y:
            self.y = max(self.y - self.speed, self.target_y)

        #Update people in lift as well
        new_y = self.y
        if self.y < self.target_y:
            new_y = min(self.y + self.speed, self.target_y)
        elif self.y > self.target_y:
            new_y = max(self.y - self.speed, self.target_y)

        for person in self.people:
            person.move_with_lift(new_y)


    def is_full(self):
        return len(self.people) == lift_capacity



def move_lift_people(lift):
    #People move out of lift if its their stop

    people_to_remove = []
    for person in lift.people:
        if person.target_floor == lift.current_floor:
            lift.open_spaces.append([person.position[0], person.lift_y_offset])
            person.target_position[0] = tower_width + tower_start_x - (person.radius * 2)
            people_to_remove.append(person)
            people_leaving.append(person)

    for person in people_to_remove:
        lift.people.remove(person)


    #People move into lift if waiting
    if len(lift.people) >= lift_capacity:
        return #Lift is full

    if len(floor_people[lift.current_floor]) == 0:
        return #Floor is empty

    #Take as many people as possible
    amount_to_take = lift_capacity - len(lift.people)
    if amount_to_take < len(floor_people[lift.current_floor]):
        #More people than space
        for n in range(amount_to_take):
            person = floor_people[lift.current_floor][0]
            person.move_into_lift(lift)
            lift.people.append(person)
            floor_people[lift.current_floor] = floor_people[lift.current_floor][1:]
    else:
        for person in floor_people[lift.current_floor]:
            person.move_into_lift(lift)
            lift.people.append(person)
        floor_people[lift.current_floor] = []

    floors_available.append(lift.current_floor)

    #Move the people waiting closer to the lift
    move_waiting_people_to_lift(lift)

def move_waiting_people_to_lift(lift : Lift):
    for person in floor_people[lift.current_floor]:

        #Count how many people in front of you on the same level
        counter = 0
        for person_in_line in floor_people[lift.current_floor]:
            if person.position[1] == person_in_line.position[1]:
                if person == person_in_line:
                    break
                counter += 1

        person.move_towards_lift(counter)


def start_animation():

    lift = Lift()
    last_floor_change_time = 0
    direction = "up"
    lift_queue = LiftQueue()

    dequeue_flag = True


    run = True
    while run:

        lift_data = (lift_queue, direction, lift.current_floor)

        clock.tick(120)

        lift_queue.print_calls()


        for n, floor in enumerate(floor_people):
            if len(floor) > 0:
                lift_queue.enqueue(Call(n, False))

        for people in lift.people:
            lift_queue.enqueue(Call(people.target_floor, True))


        global people_count
        if len(floors_available) > 0 and random.random() <= spawn_rate and people_count > 0:
            add_random_person()
            people_count -= 1

        if lift.y == lift.target_y and not lift.hasMovedPeople:
            lift.current_floor = lift.target_floor
            move_lift_people(lift)
            lift.hasMovedPeople = True
            dequeue_flag = True


        current_time = pygame.time.get_ticks()
        # Check if 3 seconds have passed since the last floor change
        if current_time - last_floor_change_time >= lift_wait_delay:
            # Choose a random floor for the lift to move to

            if not lift_queue.isEmpty() and dequeue_flag:
                current_direction, next_floor = look(lift_data)

                lift.hasMovedPeople = False
                dequeue_flag = False
                lift.move_to_floor(next_floor)

                # Update the last floor change time
                last_floor_change_time = current_time

        lift.update()
        move_sprites(lift)


        screen.fill((255, 255, 255))
        draw_tower()
        lift.draw()

        for sprite in image_sprites:
            screen.blit(sprite[0], sprite[1])

        pygame.display.flip()

    pygame.quit()


def move_sprites(lift : Lift):
    for person in floor_people:
        for p in person:
            p.move()

    for person in lift.people:
        person.move()

    old_sprites = []
    old_people = []
    for person in people_leaving:
        if person.position[0] >= tower_width + tower_start_x - (person.radius * 2):
            old_people.append(person)
            old_sprites.append(person.sprite)
        person.move()

    remove_old_sprites(old_sprites, old_people)


def remove_old_sprites(old_sprites, old_people):
    for sprite in old_sprites:
        for surface in image_sprites:
            if sprite == surface:
                image_sprites.remove(surface)

    for person in old_people:
        people_leaving.remove(person)


class Person:
    def __init__(self):
        self.radius = 15
        self.speed = game_speed
        self.lift_y_offset = 0

        self.starting_floor = rand.choice(floors_available)
        self.target_floor = rand.randint(0, floors - 1)
        self.can_call_external = True
        self.can_call_internal = True

        self.sprite = None

        self.opacity = 255

        if len(floor_people[self.starting_floor]) >= max_number_waiting - 1:
            floors_available.remove(self.starting_floor)


        #Target floor cannot be the same as target floor
        while self.starting_floor == self.target_floor:
            self.target_floor = rand.randint(0, floors - 1)

        self.position = self._get_starting_position()
        self.target_position = self.position[:]

    def get_sprite(self):
        blue = (84, 150, 255)

        surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, blue, (self.radius, self.radius), self.radius)

        self.sprite = surface

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



    def move_into_lift(self, lift):
        #Figure out new location

        if len(lift.open_spaces) > 0:
            self.target_position[0] = lift.open_spaces[0][0]
            self.lift_y_offset = lift.open_spaces[0][1]
            lift.open_spaces = lift.open_spaces[1:]
            return

        global lift_x
        offset = 5
        x = lift_x + (lift_width / 2) - (self.radius * 2) - offset
        if len(lift.people) % 2 == 1:
            x += self.radius * 2 + (offset * 2)

        if len(lift.people) < 2:
            self.lift_y_offset = (floor_spacing / 2) - (self.radius * 2) - offset
        else:
            self.lift_y_offset = (floor_spacing / 2) + offset


        self.target_position[0] = x


    def move_with_lift(self, y):
        self.target_position[1] = y + self.lift_y_offset


    def move_towards_lift(self, position_in_line):
        x = tower_start_x + (tower_width / 2) - lift_width - ((position_in_line) * 2 * self.radius) - (person_spacing * (position_in_line))

        self.target_position[0] = x



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


