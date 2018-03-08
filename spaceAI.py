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
        fireGun = {'state': 1, 'gain': 1}
        gun = self.makeActionEvent(fireGun)
        eventdown,eventup = self.makeKeyEvent(self.moves[chosenIndex])
        pygame.event.post(gun)
        pygame.event.post(eventup)
        pygame.event.post(eventdown)


    def evaluationFunction(self, esprites, shipSprite, action):
        shipSprite = shipSprite.sprites()[0]
        enemySprites = copy.deepcopy(esprites)
        nextShipSprite = copy.deepcopy(shipSprite)
        nextShipSprite = self.getNewShip(nextShipSprite,action)
        shipCoord = shipSprite.getRect()
        nextShipCoord = nextShipSprite.getRect()
        newshipxy = [nextShipCoord.x,nextShipCoord.y]
        minDistEnemy = 9999999
        maxDistEnemy = -99999
        playerSprites = pygame.sprite.RenderPlain(())
        playerSprites.add(nextShipSprite)
        newEnemySprites = pygame.sprite.RenderPlain(())
        for enemy in enemySprites:
            enemyCopy = copy.deepcopy(enemy)
            nextEnemy = self.getNewEnemy(enemyCopy)
            newEnemySprites.add(nextEnemy)
            enemyCoord = nextEnemy.getRect()
            enemyxy = [enemyCoord.x,enemyCoord.y]
            minDistEnemy = min(minDistEnemy, self.euclidean(newshipxy,enemyxy))
            maxDistEnemy = max(maxDistEnemy, self.euclidean(newshipxy,enemyxy))

        if(pygame.sprite.groupcollide(newEnemySprites,playerSprites,1,1)):
            print 'avoided collison'
            return -10000

        gameBoundry = [[0,0],[0,800],[260,0],[260,800]]
        minDistBoundry = 9999999
        for coord in gameBoundry:
            minDistBoundry = min(minDistBoundry,self.euclidean(newshipxy,coord))


        distFromCenter = self.euclidean(newshipxy,[400,150])

        return minDistEnemy + maxDistEnemy*.6 + distFromCenter*-.9

    def getNewEnemy(self,sprite):
        sprite.rect.centerx += sprite.dx
        sprite.rect.centery += sprite.dy
        return sprite

    def getNewShip(self,sprite,action):
        pos = self.moves.index(action)
        newCoord = self.coordMoves[pos]
        sprite.rect.move_ip(newCoord[0],newCoord[1])
        return sprite

    def makeActionEvent(self,action):
        return pygame.event.Event(pygame.ACTIVEEVENT, action)

    def makeKeyEvent(self, direction):
        return pygame.event.Event(pygame.KEYDOWN, direction),pygame.event.Event(pygame.KEYUP, direction)

    def euclidean(self,c1,c2):
        return math.sqrt(pow((c1[0]-c2[0]),2) + pow((c1[1]-c2[1]),2))

import SpaceShooter
