from math import sin, cos, radians
import random
import pygame

pygame.init()

ID_img = pygame.image.load("id.jpg")
ID_img = pygame.transform.scale(ID_img, (50, 28))
idCoords = [(150, 50), (100, 100)]
idStatus = []
for i in range(len(idCoords)):
	idStatus += [True] if random.randint(0, 1) > 0.5 else [False]

idCount = 0

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

    def collision(self, world, points):
        # points = [(self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y), (self.rect.x, self.rect.y + self.rect.height), (self.rect.x + self.rect.width, self.rect.y + self.rect.height)]
        collision_refs = [(190, 175, 160), (175, 165, 155), (155, 140, 130)]

        for i in range(len(points)):
            # edge detection
            if points[i][0] <= self.rect.width + 5 or points[i][1] <= self.rect.height + 5 or points[i][0] >= 1000 or points[i][1] > 1000:
                return True


            # get pixel colors
            test_hex = world.get_at(points[i][:3])[:3]
            
            count = 0
            for c in range(len(collision_refs)):
                for i in range(len(test_hex)):
                    section = collision_refs[c]
                    comparison = section[i]
                    if abs(test_hex[i] - comparison) < 10:
                        count += 1
                if count == 3:
                    return True
                else:
                    count = 0
        return False

    def move(self,camera_pos,world):
        pos_x,pos_y = camera_pos # pos_x and pos_y represent the camera

        # input
        if not self.in_vehicle:
            key = pygame.key.get_pressed()
            if key[pygame.K_w] and not self.collision(world, [(self.rect.x, self.rect.y - self.rect.height)]):
                self.rect.y -= self.vel
                pos_y += self.vel
            if key[pygame.K_a] and not self.collision(world, [(self.rect.x - self.rect.width, self.rect.y)]):
                self.rect.x -= self.vel
                pos_x += self.vel
            if key[pygame.K_s] and not self.collision(world, [(self.rect.x, self.rect.y + self.rect.height)]):
                self.rect.y += self.vel
                pos_y -= self.vel
            if key[pygame.K_d] and not self.collision(world, [(self.rect.x + self.rect.width, self.rect.y)]):
                self.rect.x += self.vel
                pos_x -= self.vel
        
        return (pos_x,pos_y)

    def render(self, display): # display itself
        if not self.in_vehicle:
            display.blit(self.image, (self.rect.x - 20,self.rect.y - 20))

    def menu(self):
        stay = True
        menuBack = pygame.image.load("aggie.png")
        menuBack = pygame.transform.scale(menuBack, (700, 700))

        while stay:
            display.blit(menuBack, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                stay = False

        return

class Vehicle:
    def __init__(self, url, x, y, vel, rotatable):
        self.image = pygame.image.load(url)
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = pygame.Rect((30,30), (10, 10)) # hitbox
        self.rotatable = rotatable

        self.rect.x = x
        self.rect.y = y

        self.player_in_vehicle = False

        self.vel = vel
        self.angle = 0
        self.angle_vel = 5

    def collision(self, world, points): # road-only collision (uses 4 coordinates - need to update to check rotational front/back)
        # points = [(self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y), (self.rect.x, self.rect.y + self.rect.height), (self.rect.x + self.rect.width, self.rect.y + self.rect.height)]
        for i in range(len(points)):
            test_hex = world.get_at(points[i][:3])
            count = 0
            for i in range(len(test_hex)):
                if abs(test_hex[i] - 82) < 10:
                    count += 1
            if count == 3:
                return True
        return False

    def move(self, world):
        change_x, change_y = 0, 0

        if self.player_in_vehicle:
            key = pygame.key.get_pressed()

            if key[pygame.K_w] and self.collision(world, [(int(self.rect.x - 35 * sin(radians(self.angle))), int(self.rect.y - 35 * cos(radians(self.angle))))]):
                change_x = self.vel * sin(radians(self.angle))
                change_y = self.vel * cos(radians(self.angle))
                self.rect.x += change_x
                self.rect.y += change_y
            elif key[pygame.K_s] and self.collision(world, [(int(self.rect.x - 35 * sin(radians(self.angle))), int(self.rect.y - 35 * cos(radians(self.angle))))]):
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
    calc_size = (6285, 4896)
    world = pygame.Surface((1000, 1000))

    map = pygame.image.load("map.png")
    map = pygame.transform.scale(map, calc_size)

    # init
    player = Player()
    camera_pos = (350, 350)

    player.menu() # menu

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
                if event.key == pygame.K_ESCAPE:
                    player.menu()

        # camera_pos is generated from player class
        camera_pos = player.move(camera_pos, world)
        in_any_vehicle = False
        for vehicle in vehicles:
            if vehicle.interact(player.get_pos(), keypress):
                in_any_vehicle = True
        player.update_in_vehicle(in_any_vehicle)

        # clear
        display.fill((89, 0, 35))

        # map
        rotated_info = rotate_img(map, (0, 0), (4200, 3600), 0)
        world.blit(rotated_info[0], rotated_info[1])

        # display player
        player.render(world)

        # display vehicles
        for vehicle in vehicles:    
            camera_update = vehicle.move(world)
            if camera_update:
                camera_pos = (350 - camera_update[0], 350 - camera_update[1])
                player.pos_update(camera_update)
            vehicle.render(world)

        # powerups
        for i in range(len(idStatus)):
            pos = player.get_pos()
            if (idStatus[i] == True):
                world.blit(ID_img, idCoords[i])
                if ((pos[0] - (idCoords[i][0] + 25)) ** 2 + (pos[1] - (idCoords[i][1] + 14)) ** 2) < 1200:
                    idStatus[i] = False
                    global idCount
                    idCount += 1 
                    print(idCount)

        # map
        display.blit(world,camera_pos)

        # debugging coordinates
        font = pygame.font.SysFont(None, 75)
        text = font.render(str(350 - camera_pos[0]), True, "white")
        display.blit(text, (100, 25))
        text = font.render(str(350 - camera_pos[1]), True, "white")
        display.blit(text, (300, 25))

        pygame.display.flip()


if __name__ in "__main__":
    display = pygame.display.set_mode((700, 700))

    pygame.display.set_caption("HowdyHack 2022")
    clock = pygame.time.Clock()
    
    game(display,clock)
