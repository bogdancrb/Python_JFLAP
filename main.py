import math
import pygame, sys, time
from pygame.locals import *
import TextInput

pygame.init()
pygame.font.init()

fontSize = 18
LEFT = 1
MIDDLE = 2
RIGHT = 3
canWrite = False

myfont = pygame.font.SysFont("Arial", fontSize)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0,32)
pygame.display.set_caption('JFLAP in Python')
surface.fill((255,255,255))

class Circle():
    coordonates = []
    def Display(self, text):
        self.coordonates = pygame.mouse.get_pos()

        pygame.draw.circle(surface, pygame.Color(0,0,255), self.coordonates, 20, 2)

        textsurface = myfont.render(text, False, (0, 0, 0))
        surface.blit(textsurface, (self.coordonates[0] - (fontSize - 10), self.coordonates[1] - (fontSize - 5)))

    def drawLine(self, circleDestIndex):
        pygame.draw.lines(surface, pygame.Color(0, 0, 255), False, [self.coordonates, circlesArray[circleDestIndex].coordonates], 2)
        return True
    def drawSelfLine(self):
        pygame.draw.arc(surface, pygame.Color(0, 0, 255), (self.coordonates[0] - 10, self.coordonates[1] - 40, 20, 50), 0, 3.14, 2)
        return True


def displayMouseCoords():
    textsurface = myfont.render("mouse at (%d, %d)" % event.pos, False, (0, 0, 0))
    pygame.draw.rect(surface, (255,255,255), [20, 20, 130, 30], 120)
    surface.blit(textsurface, [20, 20])

def getClickedCircleIndex(coords):
    for index in range(0, circlesArray.__len__()):
        x = math.pow(circlesArray[index].coordonates[0] - coords[0], 2)
        y = math.pow(circlesArray[index].coordonates[1] - coords[1], 2)
        rad = math.sqrt(x + y)

        if (rad < 20):
            return index

circlesArray = []
firstMouseCoords = None
clickedCirclesIndexes = []
textinput = TextInput.TextInput()
while True:
    if canWrite:
        pygame.draw.rect(surface, (255, 255, 255), [10, 10, 130, 30], 120)
        textinput.update(pygame.event.get())
        surface.blit(textinput.get_surface(), (10, 10))
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                var = Circle()
                circlesArray.append(var)
                index = circlesArray.index(var)
                text = 'q' + str(index)
                circlesArray[index].Display(text)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                mouseClickCoords = pygame.mouse.get_pos()
                index = getClickedCircleIndex(mouseClickCoords)

                if not(index is None):
                    clickedCirclesIndexes.append(index)

                if (clickedCirclesIndexes.__len__() >= 2):
                    if (clickedCirclesIndexes[0] == clickedCirclesIndexes[1]):
                        canWrite = circlesArray[clickedCirclesIndexes[0]].drawSelfLine()
                    else:
                        canWrite = circlesArray[clickedCirclesIndexes[0]].drawLine(clickedCirclesIndexes[1])
                    clickedCirclesIndexes = []
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == MIDDLE:
                surface.fill((255, 255, 255))
                circlesArray = []
            if event.type == pygame.MOUSEMOTION:
                displayMouseCoords()

    #Update once at the end of each gameloop.
    pygame.display.update()