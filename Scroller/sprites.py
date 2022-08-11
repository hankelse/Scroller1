import pygame, math, time, random



class Player:
    def __init__(self, x, y, size, color, speed):
        self.x, self.y, self.size, self.color = x, y, size, color
        self.starting_y = self.y
        self.xv, self.yv = 0, 0
        self.moving = False
        self.base_speed = speed
        self.speed = speed
        self.jumps = 0 #number of jumps performed before landing
        self.jump_delay = 0.2
        self.last_jump = 0 # time of last jump
    
    def move(self, keys, bindings, width, height, max_jumps):
        ##__________Y__________##

        if time.time() - self.last_jump > self.jump_delay and  self.jumps < max_jumps and  keys[bindings["jump"]]:
            self.yv = -10
            self.jumps+=1
            self.last_jump = time.time()
            #print(self.jumps)

        elif self.y >= self.starting_y:
            self.yv, self.jumps = 0, 0
        
        else:
            self.yv += 0.9
        
        if self.yv != 0: self.y += self.yv
        else: self.y = self.starting_y
        

        ##__________X___________##
        if keys[bindings["sprint"]]:
            self.speed = 2*self.base_speed
        elif self.speed != self.base_speed:
            if self.speed > self.base_speed:
                self.speed -= self.speed/10
            else: self.speed = self.base_speed
        if keys[bindings["foward"]]:
            self.moving = True
            self.xv = self.speed
        elif keys[bindings["back"]]:
            self.moving = True
            self.xv = -self.speed

        if self.xv > self.speed/15: self.xv -= self.speed/15
        elif self.xv < -self.speed/15: self.xv += self.speed/15
        else: self.moving, self.xv = False, 0
        
        if self.xv <0:
            if self.x > width*(3/8):
                self.x += self.xv
                return False, 0, self.speed
            else:
                return True, -1, self.speed
        
        elif self.xv  > 0:
            if self.x < width*(5/8):
                self.x += self.xv
                return False, 0, self.speed
            else:
                return True, 1, self.speed
        
        else:
            return False, 0, self.speed
        
        
    
        
        

    
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))


class Obstacle:
    def __init__(self, width, height, delay, y, size, color):
        self.color = color
        self.width, self.height, self.size = width, height, size
        self.x, self.y = width+random.randint(self.size, self.size+100)+delay, y

    def move(self, scroll_direction, player_speed, ground_pixel_size):
        if scroll_direction == 1:
            self.x = self.x - player_speed
            #
        elif scroll_direction == -1:
            self.x = self.x + player_speed

        

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x-self.size/2, self.y-self.size/2, self.size, self.size))