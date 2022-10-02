from math import sin, cos, radians
import pygame

screen = (700, 700)

pygame.init()
win = pygame.display.set_mode(screen)
pygame.display.set_caption("HowdyHack 2022")

map_img = pygame.image.load("map.png")
map_img = pygame.transform.scale(map_img, (6285, 4896))

car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (50, 50))

student_img = pygame.image.load("student.png")
student_img = pygame.transform.scale(student_img, (40, 40))

current_transport = "walk"

x = 200
y = 200
angle = 0

car_x = -50
car_y = -70

width = 20
height = 20
angle_vel = 1

run = True

# timer/countdoewn
clock = pygame.time.Clock()
counter = 30 # number of seconds
timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, 1000)


"""
# unimplemented vehicle class
class Vehicle:
	def __init__(self, pos_x, pos_y, angle, url, w, h, collision_type, drive_type, check_points):
		self.name = pos_x
		self.age = pos_y
		self.image = pygame.image.load(url)
		self.image = pygame.transform.scale(self.image, (w, h))
		self.collision_type = collision_type
		self.drive_type = drive_type
		self.check_points = check_points

	def collision_check(self):
		if self.collision_type == "road-only":
			for i in range(len(self.check_points)):
				if not road_collision(self.check_points[i]):
					return True
		elif self.collision_type == "no-buildings":
			for i in range(len(self.check_points)):
				if not within_collision_hex(self.check_points[i]):
					return True
		return False
"""


# clean image rotation
def rotate_img(image, pos, originPos, angle):
    originPos = (originPos[0]/2, originPos[1]/2)
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    return (rotated_image, rotated_image_rect)

def within_collision_hex(check_hex):
	collision_refs = [(190, 175, 160), (175, 165, 155), (155, 140, 130)]
	count = 0
	for c in range(len(collision_refs)):
		for i in range(len(check_hex)):
			if abs(check_hex[i] - collision_refs[c][i]) < 10:
				count += 1
		if count == 3:
			return True
		else:
			count = 0
	return False

def road_collision(check_hex):
	count = 0
	for i in range(len(check_hex)):
		if abs(check_hex[i] - 82) < 10:
			count += 1
	return count == 3


# infinite loop
while run:
	# delay between frames
	pygame.time.delay(10)
	
	# input handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:			
			run = False

		if event.type == pygame.KEYDOWN: # single click action
			# interactions
			if event.key == pygame.K_SPACE:
				if current_transport == "car": # get out of car
					current_transport = "walk"
					car_x = 350 - x
					car_y = 350 - y
				elif current_transport == "walk": # get into car
					car_screen_pos_x = x + car_x
					car_screen_pos_y = y + car_y
					if ((350 - (car_screen_pos_x)) ** 2 + (350 - (car_screen_pos_y)) ** 2) ** (1/2) < 60:
						current_transport = "car"

		if event.type == timer_event:
			counter -= 1
			text = font.render(str(counter), True, "blue")
			if counter == 0:
				pygame.time.set_timer(timer_event, 0)  

	keys = pygame.key.get_pressed()
	
	# speed boost (shift)
	speed_boost = 0
	if keys[pygame.K_SPACE]:
		speed_boost = 5

	# drive forward or backwards
	if current_transport == "car": # car movement
		vel = 4

		# car front/back collision
		check_front_coords = (int(350 + 35 * sin(radians(angle))), int(350 + 35 * cos(radians(angle))))
		check_back_coords = (int(350 - 35 * sin(radians(angle))), int(350 - 35 * cos(radians(angle))))

		if keys[pygame.K_w] and road_collision(win.get_at(check_front_coords)[:3]):
			x -= vel * sin(radians(angle))
			y -= vel * cos(radians(angle))
			forward_backward_movement = True
		if keys[pygame.K_s] and road_collision(win.get_at(check_back_coords)[:3]): # backwards is slower than forwards
			x += vel * sin(radians(angle)) * (2/3)
			y += vel * cos(radians(angle)) * (2/3)
			forward_backward_movement = True

		if keys[pygame.K_a]:
			angle += angle_vel * -1 if keys[pygame.K_DOWN] else 1
		if keys[pygame.K_d]:
			angle -= angle_vel * -1 if keys[pygame.K_DOWN] else 1
	elif current_transport == "walk": # on foot
		vel = 1 + speed_boost

		check_top_coords = (350, 350 - 20)
		check_bottom_coords = (350, 350 + 20)
		check_left_coords = (350 + 15, 350)
		check_right_coords = (350 - 15, 350)

		if keys[pygame.K_w] and not(within_collision_hex(win.get_at(check_top_coords)[:3])):
			y += vel
		if keys[pygame.K_s] and not(within_collision_hex(win.get_at(check_bottom_coords)[:3])):
			y -= vel
		if keys[pygame.K_a] and not(within_collision_hex(win.get_at(check_left_coords)[:3])):
			x += vel
		if keys[pygame.K_d] and not(within_collision_hex(win.get_at(check_right_coords)[:3])):
			x -= vel



	# background and moving map
	win.fill((255, 255, 255))
	rotated_info = rotate_img(map_img, (x, y), map_img.get_rect().size, 0)
	win.blit(rotated_info[0], rotated_info[1])

	# character
	if current_transport == "car":
		rotated_info = rotate_img(car_img, (350, 350), car_img.get_rect().size, angle)
		win.blit(rotated_info[0], rotated_info[1])


	elif current_transport == "walk":
		win.blit(student_img, (330, 330))
		rotated_info = rotate_img(car_img, (x + car_x, y + car_y), car_img.get_rect().size, angle)
		win.blit(rotated_info[0], rotated_info[1])

	# direction line
	goal = (2500, 3000)
	goal_screen_x = goal[0] + x - 3140
	goal_screen_y = goal[1] + y - 2450
	pygame.draw.line(win, "blue", (350, 350), (goal_screen_x, goal_screen_y), width=5)

	# win condition (if close enough to destination)
	if(((350 - (goal_screen_x)) ** 2 + (350 - (goal_screen_y)) ** 2) ** (1/2)) < 100:
		print("WIN!")

	# countdown
	font = pygame.font.SysFont(None, 75)
	text = font.render(str(counter), True, "blue")
	win.blit(text, (615, 25))
	pygame.display.flip()

pygame.quit()
