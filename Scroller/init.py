from background import Background
from sprites import Player, Obstacle
from Shape_Collisions import collision

import pygame, sys, time, math, random
from pygame.constants import K_SPACE, K_ESCAPE, K_w, K_a, K_s, K_d, K_LSHIFT
pygame.init()

size = width, height =  800, 800
cycle_time = 0.025

screen = pygame.display.set_mode(size)




#------SETTINGS--------#

#player_input
bindings = {
    "foward": K_d,
    "back"  : K_a,
    "sprint": K_LSHIFT,
    "jump": K_SPACE,
    "reset": K_SPACE
}

#background
sky_pixel_size = 8
ground_pixel_size = 8
sky_colors= {
    0 : (210, 210, 215),
    1 : (120, 130, 255)
}
ground_colors = {
    0: (82, 46, 9),
    1: (85, 51, 33),
    2: (88, 56, 15),
}

grass_colors = {
    0: (10, 130, 10),
    1: (20, 150, 10),
    2: (15, 125, 50)
}

#player
base_player_speed = 10
player_size = 50
player_jumps = 6
player_color = (0, 0, 0)

#obstacles
num_obstacles = 4
obstacle_color = (0, 0, 0)



#-------SETUP----------#
def setup():

    obstacles = []
    for i in range(num_obstacles):
        obstacles.append(Obstacle(width, height, i*200, random.randint(int(height/2), int(height*(6/8))), random.randint(30, 70), obstacle_color))

    player = Player(width/2, height*(6/8)-player_size/2, player_size, player_color, base_player_speed)
    background = Background(width, height, sky_pixel_size, ground_pixel_size, sky_colors, ground_colors, grass_colors)

    lose = False
    return obstacles,player, background, lose

obstacles,player, background, lose = setup()

while 1:
    now = time.time()
    #screen.fill((160, 160, 160))
    keys=pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if lose == False:

        should_scroll, scroll_direction, player_speed = player.move(keys, bindings, width, height, player_jumps)
        background.move(scroll_direction, player_speed)

        for obstacle in obstacles:
            obstacle.move(scroll_direction, player_speed, ground_pixel_size)
            #if obstacle.x < -obstacle.size and obstacle.x > -obstacle.size-player_speed: obstacles.append(Obstacle(width, height, 100, random.randint(height/2, height*(6/8)), random.randint(30, 70), obstacle_color))
            if obstacle.x < -1000 or obstacle.x > width+1000:
                obstacles.remove(obstacle)
                obstacles.append(Obstacle(width, height, 100, random.randint(height/2, height*(6/8)), random.randint(30, 70), obstacle_color))
            
    if lose == True and keys[bindings["reset"]]:
        obstacles,player, background, lose = setup()

    
    
    
    background.draw(screen)
    player.draw(screen)
    for obstacle in obstacles: 
        obstacle.draw(screen)
        if lose == False and collision(player, obstacle, "circle", "rect") == True: 
                lose = True

    
    
    

    
    pygame.display.flip()
    elapsed = time.time()-now
    if elapsed < cycle_time:
        time.sleep(cycle_time-elapsed)