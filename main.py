import math
import pygame, sys, time
from pygame.locals import *
import TextInput
import Buttons

pygame.init()
pygame.font.init()

LEFT = 1
MIDDLE = 2
RIGHT = 3
fontSize = 18
firstMouseCoords = None
nrOfButtons = 2

canWrite = False
displayButtons = True

circlesArray = []
clickedCirclesIndexes = []
buttonsArray = []
buttonsTexts = [
    'Seteaza initial',
    ' Seteaza final '
]


myfont = pygame.font.SysFont("Arial", fontSize)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),0,32)
pygame.display.set_caption('JFLAP in Python')
surface.fill((255,255,255))
surface.fill((239,239,239), [170, 20, 800, 450])

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
    def setInitial(self):
        # pygame.draw.lines(surface, pygame.Color(0, 0, 255), False, [(100,150), (250,100), (80,180)], 2)
        pygame.draw.polygon(surface, pygame.Color(0, 0, 255), [[self.coordonates[0] - 50, self.coordonates[1] - 30], [self.coordonates[0] - 50, self.coordonates[1] + 25], [self.coordonates[0] - 20, self.coordonates[1]]], 3)
    def setFinal(self):
        pygame.draw.circle(surface, pygame.Color(0, 0, 255), self.coordonates, 30, 2)

def displayMouseCoords():
    textsurface = myfont.render("mouse at (%d, %d)" % event.pos, False, (0, 0, 0))
    surface.fill((255, 255, 255), [20, 20, 130, 30])
    surface.blit(textsurface, [20, 20])

def getClickedCircleIndex(coords):
    for index in range(0, circlesArray.__len__()):
        x = math.pow(circlesArray[index].coordonates[0] - coords[0], 2)
        y = math.pow(circlesArray[index].coordonates[1] - coords[1], 2)
        rad = math.sqrt(x + y)

        if (rad < 20):
            return index

def getClickedButtonIndex(coords):
    for index in range(0, buttonsArray.__len__()):
        if (buttonsArray[index].pressed(coords)):
            return index

    return -1

def executeButtonCommand(index):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                mouseClickCoords = pygame.mouse.get_pos()

                indexCircle = getClickedCircleIndex(mouseClickCoords)

                if indexCircle is None:
                    return

                if index == 0:
                    circlesArray[indexCircle].setInitial()
                else:
                    circlesArray[indexCircle].setFinal()

                return

while True:
    if displayButtons:
        buttonsArray = []

        for i in range(0, nrOfButtons):
            buttonsArray.append(Buttons.Button())

            buttonsArray[i].create_button(surface, (255, 255, 255), 65 * (i * 4 + 1), 490, 240, 40, 80, buttonsTexts[i], (0, 0, 0))
            displayButtons = False

    if canWrite:
        # Circle 1
        x1 = circlesArray[clickedCirclesIndexes[0]].coordonates[0]
        y1 = circlesArray[clickedCirclesIndexes[0]].coordonates[1]

        # Circle 2
        x2 = circlesArray[clickedCirclesIndexes[1]].coordonates[0]
        y2 = circlesArray[clickedCirclesIndexes[1]].coordonates[1]

        # Fill input field
        if x1 == x2 and y1 == y2:
            x = (x1 + x2) / 2 - 15
            y = (y1 + y2) / 2 - 60
        else:
            x = (x1 + x2) / 2 - 40
            y = (y1 + y2) / 2 - 20

        surface.fill((239,239,239), [x, y, 45, 20])

        # Run the textinput
        canWrite = textinput.update(pygame.event.get())

        # Attach to screen
        surface.blit(textinput.get_surface(), (x, y))
    else:
        textinput = TextInput.TextInput()

        for event in pygame.event.get():
            mouseClickCoords = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                buttonIndex = getClickedButtonIndex(mouseClickCoords)

                if buttonIndex == -1 \
                        and (mouseClickCoords[0] >= 180 and mouseClickCoords[0] <= 950) \
                        and (mouseClickCoords[1] >= 80 and mouseClickCoords[1] <= 420):
                    var = Circle()
                    circlesArray.append(var)
                    index = circlesArray.index(var)
                    text = 'q' + str(index)
                    circlesArray[index].Display(text)
                else:
                    executeButtonCommand(buttonIndex)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                index = getClickedCircleIndex(mouseClickCoords)

                if (clickedCirclesIndexes.__len__() >= 2):
                    clickedCirclesIndexes = []

                if not(index is None):
                    clickedCirclesIndexes.append(index)

                if (clickedCirclesIndexes.__len__() >= 2):
                    if (clickedCirclesIndexes[0] == clickedCirclesIndexes[1]):
                        canWrite = circlesArray[clickedCirclesIndexes[0]].drawSelfLine()
                    else:
                        canWrite = circlesArray[clickedCirclesIndexes[0]].drawLine(clickedCirclesIndexes[1])
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == MIDDLE:
                surface.fill((255, 255, 255))
                surface.fill((239, 239, 239), [170, 20, 800, 450])
                circlesArray = []
                displayButtons = True
            if event.type == pygame.MOUSEMOTION:
                displayMouseCoords()

    #Update once at the end of each gameloop.
    pygame.display.update()