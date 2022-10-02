from math import sin, cos, radians

import pygame
pygame.init()

class Player:
    def __init__(self):
        self.image = pygame.image.load("student.png")
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = pygame.Rect((40, 40), (16,16)) # holds player x,y for collision purposes
        self.vel = 8

        self.in_vehicle = False

    def get_pos(self):
        return (self.rect.x, self.rect.y)

    def pos_update(self, pos_update):
        self.rect.x = pos_update[0]
        self.rect.y = pos_update[1]

    def update_in_vehicle(self, value):
        self.in_vehicle = value

    def move(self,camera_pos):
        pos_x,pos_y = camera_pos # pos_x and pos_y represent the camera

        # input
        if not self.in_vehicle:
            key = pygame.key.get_pressed()
            if key[pygame.K_w]:
                self.rect.y -= self.vel
                pos_y += self.vel
            if key[pygame.K_a]:
                self.rect.x -= self.vel
                pos_x += self.vel
            if key[pygame.K_s]:
                self.rect.y += self.vel
                pos_y -= self.vel
            if key[pygame.K_d]:
                self.rect.x += self.vel
                pos_x -= self.vel
        
        return (pos_x,pos_y)

    def render(self, display): # display itself
        if not self.in_vehicle:
            display.blit(self.image, (self.rect.x - 20,self.rect.y - 20))

class Vehicle:
    def __init__(self, url, x, y, vel, rotatable):
        self.image = pygame.image.load(url)
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = pygame.Rect((50,50), (16,16))
        self.rotatable = rotatable

        self.rect.x = x
        self.rect.y = y

        self.player_in_vehicle = False

        self.vel = vel
        self.angle = 0
        self.angle_vel = 5

    def move(self):
        change_x, change_y = 0, 0

        if self.player_in_vehicle:
            key = pygame.key.get_pressed()

            if key[pygame.K_w]:
                change_x = self.vel * sin(radians(self.angle))
                change_y = self.vel * cos(radians(self.angle))
                self.rect.x += change_x
                self.rect.y += change_y
            elif key[pygame.K_s]:
                change_x = -1 * self.vel * sin(radians(self.angle))
                change_y = -1 * self.vel * cos(radians(self.angle))
                self.rect.x += change_x
                self.rect.y += change_y
            if key[pygame.K_a]:
                self.angle += self.angle_vel * (-1 if key[pygame.K_DOWN] else 1)
            if key[pygame.K_d]:
                self.angle -= self.angle_vel * (-1 if key[pygame.K_DOWN] else 1)

            return (self.rect.x, self.rect.y)
        return False

    def interact(self, player_pos, keypress):
        if keypress:
            # determine distance from player
            distance = ( (self.rect.x - player_pos[0]) ** 2 + (self.rect.y - player_pos[1]) ** 2 ) ** (1/2)
            if distance < 50 and not self.player_in_vehicle:
                self.player_in_vehicle = True
            elif self.player_in_vehicle:
                self.player_in_vehicle = False
        return self.player_in_vehicle


    def render(self, display):
        #display.blit(self.image, (self.rect.x,self.rect.y))
        rotated_info = rotate_img(self.image, (self.rect.x, self.rect.y), self.image.get_rect().size, self.angle if self.rotatable else 0)
        display.blit(rotated_info[0], rotated_info[1])

def rotate_img(image, pos, originPos, angle):
    originPos = (originPos[0]/2, originPos[1]/2)
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    return (rotated_image, rotated_image_rect)

def game(display, clock):
    world = pygame.Surface((1200, 1200))
    map = pygame.image.load("map.png")

    # init
    player = Player()
    camera_pos = (350, 350)

    car = Vehicle("car.png", 200, 50, 10, True)
    scooter = Vehicle("scooter.png", 30, 45, 10, False)
    vehicles = [car, scooter] # array of all vehicles
    
    while True:
        clock.tick(60)

        keypress = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    keypress = True

        # camera_pos is generated from player class
        camera_pos = player.move(camera_pos)
        in_any_vehicle = False
        for vehicle in vehicles:
            if vehicle.interact(player.get_pos(), keypress):
                in_any_vehicle = True
        player.update_in_vehicle(in_any_vehicle)

        # clear
        display.fill((122, 122, 122))

        # map
        rotated_info = rotate_img(map, (0, 0), map.get_rect().size, 0)
        world.blit(rotated_info[0], rotated_info[1])

        # display player
        player.render(world)

        # display vehicles
        for vehicle in vehicles:    
            camera_update = vehicle.move()
            if camera_update:
                camera_pos = (350 - camera_update[0], 350 - camera_update[1])
                player.pos_update(camera_update)
            vehicle.render(world)

        # map
        display.blit(world,camera_pos)

        pygame.display.flip()

if __name__ in "__main__":
    display = pygame.display.set_mode((700, 700))

    pygame.display.set_caption("HowdyHack 2022")
    clock = pygame.time.Clock()
    
    game(display,clock)
