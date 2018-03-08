import pygame
import random
import math
import copy
class spaceAI(object):

    def __init__(self):
        self.right = {'scancode': 114, 'key': 275, 'unicode': u'', 'mod': 4096}
        self.down = {'scancode': 116, 'key': 274, 'unicode': u'', 'mod': 4096}
        self.left = {'scancode': 113, 'key': 276, 'unicode': u'', 'mod': 4096}
        self.up = {'scancode': 111, 'key': 273, 'unicode': u'', 'mod': 4096}
        self.center = {'scancode': 114, 'key': 275, 'unicode': u'', 'mod': 4096}
        self.moves = [self.right,self.left,self.down,self.up,self.center]
        #both in respective order
        self.coordMoves = [[20,0],[-20,0],[0,-20],[0,-20],[0,0]]



    def sendKey(self,enemySprites,shipSprite):
        scores = [self.evaluationFunction(enemySprites,shipSprite,action) for action in self.moves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        event = self.makeEvent(self.moves[chosenIndex])
        return event

    def evaluationFunction(self, esprites, shipSprite, action):
        shipSprite = shipSprite.sprites()[0]
        enemySprites = copy.deepcopy(esprites)
        nextShipSprite = copy.deepcopy(shipSprite)
        nextShipSprite = self.getNewCoord(nextShipSprite,action)
        shipCoord = shipSprite.getRect()
        nextShipCoord = nextShipSprite.getRect()
        newshipxy = [nextShipCoord.x,nextShipCoord.y]
        playerSprites = pygame.sprite.RenderPlain(())
        playerSprites.add(nextShipSprite)
        if(len(pygame.sprite.groupcollide(enemySprites,playerSprites,1,0))):
            print 'avoided collison'
            return -10
        minDist = 9999999
        for enemy in enemySprites:
            enemyCoord = enemy.getRect()
            enemyxy = [enemyCoord.x,enemyCoord.y]
            minDist = min(minDist, self.manhattan(newshipxy,enemyxy))
        return minDist

    def getNewCoord(self,sprite,action):
        pos = self.moves.index(action)
        newCoord = self.coordMoves[pos]
        sprite.rect.move_ip(newCoord[0],newCoord[1])
        return sprite

    def makeEvent(self, direction):
        return pygame.event.Event(pygame.KEYDOWN, direction)

    def manhattan(self,c1,c2):
        return abs(c1[0]-c2[0]) + abs(c1[1]-c2[1])

import SpaceShooter
