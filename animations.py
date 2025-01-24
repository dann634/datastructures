import pygame
import random

rand = random.Random()

floor_people = [] #2D list
floors = 5
image_sprites = []

pygame.init()
screen_width = 1000
screen_height = 50 + (floors * 100)
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

tower_width = 600
floor_spacing = 100
tower_start_x = (screen_width / 2) - (tower_width / 2)
max_number_waiting = 6
lift_width = 100

def draw_tower():
    for i in range(floors + 1):  # +1 to include the top floor line
        y = i * floor_spacing
        pygame.draw.line(screen, (0, 0, 0), (tower_start_x, y), (tower_start_x + tower_width, y), 2)  # Horizontal line
        # Draw the vertical edges
    pygame.draw.line(screen, (0, 0, 0), (tower_start_x, 0), (tower_start_x, floors * floor_spacing), 2)  # Left edge
    pygame.draw.line(screen, (0, 0, 0), (tower_start_x + tower_width, 0), (tower_start_x + tower_width, floors * floor_spacing),
                     2)  # Right edge


def initialise_floors():
    global floor_people
    for n in range(floors):
        floor_people.append([])

def add_random_person():
    person = Person()
    floor_people[person.starting_floor].append(person)
    image_sprites.append(person.get_sprite())

class Lift:
    def __init__(self):
        self.width = lift_width
        self.height = floor_spacing
        self.x = (screen_width / 2) - (self.width / 2)
        self.y = floors * floor_spacing - self.height  # Start at the bottom floor
        self.target_y = self.y  # Target position for smooth movement
        self.speed = 2  # Speed of lift movement

    def draw(self):
        # Draw the lift as a rectangle
        pygame.draw.rect(screen, (200, 0, 0), (self.x, self.y, self.width, self.height))

    def move_to_floor(self, floor):
        # Set the target position based on the floor number
        self.target_y = floor * floor_spacing + (floor_spacing - self.height) / 2

    def update(self):
        # Smooth movement towards the target_y
        if self.y < self.target_y:
            self.y = min(self.y + self.speed, self.target_y)
        elif self.y > self.target_y:
            self.y = max(self.y - self.speed, self.target_y)


def start_animation():

    lift = Lift()
    current_floor = floors - 1

    run = True
    while run:
        clock.tick(120)
        # add_random_person()

        # Move lift to a new random floor every few seconds
        if pygame.time.get_ticks() % 3000 < 60:  # Change floor every 3 seconds
            current_floor = rand.randint(0, floors - 1)
            lift.move_to_floor(current_floor)

        lift.update()

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

        self.starting_floor = rand.randint(0, floors - 1)
        self.target_floor = rand.randint(0, floors - 1)

        #Target floor cannot be the same as target floor
        while self.starting_floor == self.target_floor:
            self.target_floor = rand.randint(0, floors - 1)


    def get_sprite(self):
        blue = (84, 150, 255)


        surface = pygame.Surface((self.radius*2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, blue, (self.radius, self.radius), self.radius)

        position = (rand.randint(0, 600), rand.randint(0, 600))

        return surface, position


    def get_starting_floor(self):
        return self.starting_floor

    def _get_starting_position(self):
        #Determine which position it needs to go
        people_waiting = len(floor_people[self.starting_floor])

        #Get X coordinate
        x = tower_start_x + (tower_width / 2) - lift_width - ((people_waiting // 2) * 2 * self.radius)







if __name__ == '__main__':
    initialise_floors()
    start_animation()