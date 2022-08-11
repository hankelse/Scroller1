import pygame, random, math


class Sky:
    def __init__ (self, width, height, pixel_size, colors):
        self.width, self.height = width, height*(6/8)
        self.pixel_size = pixel_size
        self.colors = colors
        self.grid =[]
        
        colomn = []
        for i in range(int(self.height/pixel_size)):colomn.append(random.choice([0, 1, 1, 1, 1]))
        self.grid.append(colomn)

        for i in range(int(self.width/pixel_size)-1):
            self.grid.append(self.new_colomn(1))
     
    def new_colomn(self, direction):
        row = []
        if direction == 1:
            prev = self.grid[-1]
        else: prev = self.grid[0]
        for pixel in prev:
            row.append(pixel)
        
        white = row.count(0)
        blue = row.count(1)
        if white > blue*0.2: dominant, submissive = 1, 0
        else: dominant, submissive = 0, 1

        def change(x, y, chance):
            if random.randint(1, 100) > chance: return(x)
            else: return(y)

        for i in range(len(row)):
            if i == 0:
                if prev[i] == submissive:
                    if prev[i+1] == dominant:
                        row[i]=change(submissive, dominant, 75)

        
            elif i == len(row)-1:
                if prev[i] == submissive:
                    if prev[i-1]== dominant:
                        row[i]=change(submissive, dominant,75)

            else:
                if prev[i] == submissive:
                    if prev[i+1] == dominant and prev[i-1] == dominant:
                        row[i]=change(submissive, dominant, 95)
                    elif prev[i+1] == dominant or prev[i-1] == dominant:
                        row[i]=change(submissive, dominant, 75)
                    else:
                        row[i]=change(submissive, dominant, 10)
                else:
                    if prev[i-1] == submissive and prev[i+1]==submissive:
                        row[i] = submissive
        return(row)


    def move(self, scroll_direction, scroll_speed):
        if scroll_direction != 0:
            # if scroll_direction == 1: new_index = -1
            # elif scroll_direction == -1: new_index = 0
            # for i in range(scroll_speed):
            #     self.grid.insert(new_index, self.new_colomn(scroll_direction))

            if scroll_direction == 1: 
                self.grid.append( self.new_colomn(scroll_direction))

            elif scroll_direction == -1: 
                self.grid.insert(0, self.new_colomn(scroll_direction))


            
            if scroll_direction == -1: 
                self.grid = self.grid[0:-1*scroll_speed]
            elif scroll_direction == 1: 
                self.grid = self.grid[scroll_speed::]
            
    def draw(self, screen):
        for colomn in range(len(self.grid)):
            for pixel in range(len(self.grid[colomn])):
                pygame.draw.rect(screen, self.colors[self.grid[colomn][pixel]], pygame.Rect(colomn*self.pixel_size, pixel*self.pixel_size, self.pixel_size, self.pixel_size))



class Ground:
    def __init__ (self, width, height, pixel_size, ground_colors, grass_colors):
        self.width, self.height = width, int(height*(1/4))
        self.screen_height = height
        self.pixel_size = pixel_size
        self.ground_colors = ground_colors
        self.grass_colors = grass_colors
        self.grid =[]
        for i in range(int(self.width/pixel_size)):
            colomn = []
            for i in range(int(self.height/pixel_size)):
                colomn.append(random.choice([0, 1, 2]))
            self.grid.append(colomn)
    
    def new_colomn(self):
        colomn = []
        for i in range(int(self.height/self.pixel_size)):
            colomn.append(random.choice([0, 1, 2]))
        return colomn

    def move(self, scroll_direction, scroll_speed):
        if scroll_direction != 0:
            # if scroll_direction == 1: new_index = -1
            # elif scroll_direction == -1: new_index = 0
            # for i in range(scroll_speed):
            #     self.grid.insert(new_index, self.new_colomn(scroll_direction))

            if scroll_direction == 1: 
                for i in range(scroll_speed):
                    self.grid.append(self.new_colomn())

            elif scroll_direction == -1: 
                for i in range(scroll_speed):
                    self.grid.insert(0, self.new_colomn())


            
            if scroll_direction == -1: 
                self.grid = self.grid[0:-1*scroll_speed]
            elif scroll_direction == 1: 
                self.grid = self.grid[scroll_speed::]
            
    def draw(self, screen):
        for colomn in range(len(self.grid)):
            for pixel in range(len(self.grid[colomn])):
                if pixel > 2:
                    pygame.draw.rect(screen, self.ground_colors[self.grid[colomn][pixel]], pygame.Rect(colomn*self.pixel_size, pixel*self.pixel_size+int(self.screen_height*(3/4)), self.pixel_size, self.pixel_size))
                else:
                    pygame.draw.rect(screen, self.grass_colors[self.grid[colomn][pixel]], pygame.Rect(colomn*self.pixel_size, pixel*self.pixel_size+int(self.screen_height*(3/4)), self.pixel_size, self.pixel_size))
                #else:
                    #pygame.draw.rect(screen, random.choice([self.grass_colors[self.grid[colomn][pixel]], self.ground_colors[self.grid[colomn][pixel]]]), pygame.Rect(colomn*self.pixel_size, pixel*self.pixel_size+int(self.screen_height*(3/4)), self.pixel_size, self.pixel_size))



class Background:
    def __init__ (self, width, height, sky_pixel_size, ground_pixel_size, sky_colors, ground_colors, grass_colors):
        self.sky = Sky(width, height, sky_pixel_size, sky_colors)
        self.ground = Ground(width, height, ground_pixel_size, ground_colors, grass_colors)
    
    def move(self,scroll_direction, player_speed):
        self.sky.move(scroll_direction, math.ceil(player_speed/(4*self.sky.pixel_size)))
        self.ground.move(scroll_direction, math.ceil(player_speed/self.ground.pixel_size))
    
    def draw(self,screen):
        self.ground.draw(screen)
        self.sky.draw(screen)
        