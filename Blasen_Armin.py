import pygame
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_SPACE, MOUSEBUTTONDOWN, MOUSEBUTTONUP)
import os, sys
from random import *
from math import *



class Settings(object):                                                                     #Window
    def __init__(self):
        self.width = 800                                                   
        self.height = 700                                                   
        self.fps = 60                                                       
        self.title = "Mein Bester Freund die Blase"                                          
        self.image_path = os.path.dirname(os.path.abspath(__file__))        

    def size(self):                                                                 # Window Size x,y  
        return (self.width, self.height)   

class Points():                                                                     # Scoreboaard
    def __init__(self, settings):
        self.settings= settings
        self.image = pygame.image.load(os.path.join(
                    self.settings.image_path, "scoreboard.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 50))

class Player(pygame.sprite.Sprite):                                                  # Player, Mouse 
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.image = pygame.image.load(os.path.join(
                    self.settings.image_path, "cursor-1.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.mask.Mask.get_rect(self.mask)
        self.rect.left, self.rect.top = pygame.mouse.get_pos()

    def update(self):                                                               # Update the Mouse position
        self.rect.left, self.rect.top = pygame.mouse.get_pos()


class Bubble(pygame.sprite.Sprite):                                                 # Bubbles(Opponents); Sprite in random place
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)
        self.settings = settings
        self.size= 10
        self.image = pygame.image.load(os.path.join(
                    self.settings.image_path, "bubblebubble.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.mask.Mask.get_rect(self.mask)
        self.rect.left = randint(110,self.settings.width-110-self.size)
        self.rect.top = randint(110,self.settings.height-110-self.size)
        self.rect.right= self.rect.left + self.size
        self.rect.bottom= self.rect.top + self.size
        self.grow = randint(1,4)

    def update(self):                                                               # Sprite get bigger
        if self.size < 221:
            center = self.rect.center
            self.size += self.grow
            self.image = pygame.image.load(os.path.join(
                        self.settings.image_path, "bubblebubble.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = pygame.mask.Mask.get_rect(self.mask)
            self.rect.center = center

    def newpos(self):   
        self.rect.left = randint(110,self.settings.width-110-self.size)
        self.rect.top = randint(110,self.settings.height-110-self.size)

    def pointcalc(self):
        points= 0
        if self.size < 51:
            points= 10
        if self.size > 50 and self.size < 101:
            points= 20
        if self.size > 100 and self.size < 151:
            points= 50
        if self.size > 150 and self.size < 221:
            points= 100
        return points



class Game(object):
    def __init__(self, pygame, settings):
        self.pygame = pygame                                                          #Backround
        self.settings = settings
        self.screen = pygame.display.set_mode(settings.size())                                      
        self.pygame.display.set_caption(self.settings.title)                                                      
        self.background = self.pygame.image.load(os.path.join(
                        self.settings.image_path, "jellyfish_field.png")).convert()
        self.background = pygame.transform.scale(self.background, (800, 700))                            
        self.background_rect = self.background.get_rect()

        self.player = Player(settings)                                              # Objects with fixed coordinates
        self.points = Points(settings)
        
        self.pointscolor = [255,255,255]                                            # Settings for the points display
        self.pointsadd = 0
        self.font = pygame.font.Font(None, 35)                                                        
        self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)                     
        self.textRect = self.text.get_rect()                                                            
        self.textRect.center = 15, 18 

        self.clock = pygame.time.Clock()                                            # Time and boolean for programme
        self.done = False

        self.bubblecount = 0                                                        # variables for creating bubbles

        pygame.mouse.set_visible(False)                                             # transparent mouse so that only sprite is there 

        self.all_bubbles = pygame.sprite.Group()                                    # Sprite groups for "Opponents" & "Players
        self.the_mouse = pygame.sprite.Group()

        self.the_mouse.add(self.player)                                             # "Player" object in the group



        self.ticks = pygame.time.get_ticks()                                        # Time variables for the time calculation
        self.numb= 0
        self.spawn= ((pygame.time.get_ticks()-self.ticks)/1000) +self.numb

        self.loop = True


    
    def run(self):                                                                  # Main programme loop
        while not self.done:                         
            self.clock.tick(self.settings.fps)    
            self.timef= (pygame.time.get_ticks()-self.ticks)/1000
            self.time= round(self.timef, 1)    

            for event in self.pygame.event.get():       
                if event.type == QUIT:                                              # Functions to close the programme
                    self.done = True                 
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause        
                    if event.key == K_ESCAPE:
                        self.done = True


                touchbubble= pygame.sprite.spritecollide(self.player, self.all_bubbles, False)     # Collision detection(players,bubbles)       

                if touchbubble:                                                                     # Change player sprite on collision
                    self.player.image = pygame.image.load(os.path.join(
                                        self.settings.image_path, "cursor-2.png")).convert_alpha()
                    self.player.image = pygame.transform.scale(self.player.image, (45, 40))
                if not touchbubble:
                    self.player.image = pygame.image.load(os.path.join(
                                        self.settings.image_path, "cursor-1.png")).convert_alpha()
                    self.player.image = pygame.transform.scale(self.player.image, (45, 40))


                
                
                if event.type == MOUSEBUTTONDOWN and touchbubble:                                   # on collision and click, kill bubble
                    for s in touchbubble:
                        self.pointsadd += s.pointcalc()
                    pygame.sprite.spritecollide(self.player, self.all_bubbles, True)
                    self.text = self.font.render(str(self.pointsadd), True, self.pointscolor)
                    self.bubblecount -= 1



                

            self.update()                                                   # Necessary updates of sprites, variables, etc.
            self.draw()                                                     # painting" on the window
 
    def draw(self):                                                         # background, bubbles, player, "paint" dots
        self.screen.blit(self.background, self.background_rect)
        self.all_bubbles.draw(self.screen)
        self.screen.blit(self.points.image,(5,5))
        self.screen.blit(self.text, self.textRect.center)
        self.the_mouse.draw(self.screen)
        self.pygame.display.flip()                                

    def update(self):                                       # "difficulty",more bubbles,growing bubbles,player position update
        self.morebubbles() 
        self.all_bubbles.update() 
        self.the_mouse.update()

    def morebubbles(self):                                  # Calculation and function for creating bubbles
        self.faster()
        if self.bubblecount < 8:
            if self.time == self.spawn:
                self.all_bubbles.add(Bubble(self.settings))
                self.bubblecount += 1
                self.spawn += self.numb
        else:
            if self.time == self.spawn:
                self.spawn += self.numb

    def faster(self):                                       # Extension of the bubble calculation
        if self.time < 21:
            self.numb= 1
        if self.time > 20 and self.time < 41:
            self.numb= 0.8 
            self.spawn= round(self.spawn,1)
        if self.time > 40 and self.time < 61:
            self.numb= 0.6  
            self.spawn= round(self.spawn,1)
        if self.time > 60 and self.time < 81:
            self.numb= 0.4
            self.spawn= round(self.spawn,1)
        if self.time > 80:
            self.numb= 0.2 
            self.spawn= round(self.spawn,1)
        
    def pause(self):
        while self.loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loop = False
                if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_p:
                        self.loop = False

                        
        self.draw()
        self.update()





if __name__ == '__main__':                         
    settings = Settings()               # Window settings, initialise pygame, game object,                 
                                        # Main loop of the game, and end of the programme
    pygame.init()   

    game = Game(pygame, settings)  
 
    game.run()          
  
    pygame.quit()             
