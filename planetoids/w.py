"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in the 
Planetoids game.  Instances of Wave represent a single level, and should correspond
to a JSON file in the Data directory. Whenever you move to a new level, you are 
expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on screen. These 
are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Ed Discussions and we will answer.

Name: Mensah Jephthah Kwame(jkm255)
Date: Nov 8, 2022
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)    


class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    
    This subcontroller has a reference to the ship, asteroids, and any bullets on screen.
    It animates all of these by adding the velocity to the position at each step. It
    checks for collisions between bullets and asteroids or asteroids and the ship 
    (asteroids can safely pass through each other). A bullet collision either breaks
    up or removes a asteroid. A ship collision kills the player. 
    
    The player wins once all asteroids are destroyed.  The player loses if they run out
    of lives. When the wave is complete, you should create a NEW instance of Wave 
    (in Planetoids) if you want to make a new wave of asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 25 for an example.  This class will be similar to
    than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be accessed 
    without going through a getter/setter first. However, just because you have an
    attribute does not mean that you have to have a getter for it. For example, the
    Planetoids app probably never needs to access the attribute for the bullets, so 
    there is no need for a getter there. But at a minimum, you need getters indicating
    whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    
    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    
    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    
    # RESET METHOD FOR CREATING A NEW LIFE
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def getData(self):
        """
        Returns the wave
        """
        return self._data

    def setData(self, wave_dict):
        """
        Sets the data of the wave

        Parameter wave_dict: is the new data to be set
        Precondition: wave_dict is a dictionary
        """
        assert isinstance(wave_dict, dict)

        self._data = wave_dict

    def getAsteroids(self):
        """
        Returns the list of asteroids
        """
        return self._asteroids

    def setAsteroids(self, asteroids):
        """
        Sets the list of asteroids

        Parameter asteroids: is the properties of the asteroids to be set
        Precondition: list of dictionaries
        """
        assert isinstance(asteroids, list)

        for asteroid_properties in asteroids:
            if "direction" in asteroid_properties:
                asteroid = Asteroid(position = asteroid_properties["position"],
                                    size = asteroid_properties["size"],
                                    direction = asteroid_properties["direction"])
                self._asteroids.append(asteroid)

            elif "velocity" in asteroid_properties:
                asteroid = Asteroid(position = asteroid_properties["position"],
                                    size = asteroid_properties["size"],
                                    velocity = asteroid_properties["velocity"])
                self._asteroids.append(asteroid)

    def getBullets(self):
        """
        Returns the list of bullets
        """
        return self._bullets

    def getLives(self):
        """
        Returns the lives left
        """
        return self._lives

    def setLives(self, lives):
        """
        Sets the lives

        Parameter lives: the new life to be set
        Precondition: lives is an int greater or equal to zero
        """
        assert isinstance(lives, int)
        assert lives >= 0

        self._lives = lives

    def getFirerate(self):
        """
        Returns the firerate of the bullet
        """
        return self._firerate

    def setFirerate(self, firerate):
        """
        Sets the firerate of the ship

        Parameter firerate: is the firerate of the ship
        Precondition: firarate is an int greater than or equal to zero
        """
        assert isinstance(firerate, int)
        assert firerate >= 0

        self._firerate = firerate

    def getShip(self):
        """
        Returns the ship
        """
        return self._ship

    def setShip(self):
        """
        Sets the ship
        """
        self._ship = Ship(position = self._data["ship"]["position"],
                          angle = self._data["ship"]["angle"])

    def __init__(self, wave_no):
        """
        Initializes a wave

        Parameter: wave_no is the wave to be set
        Precondition: wave_no is a dict
        """
        assert isinstance(wave_no, dict)
        self._data = wave_no
        self._ship = Ship(position = self._data["ship"]["position"],
                          angle = self._data["ship"]["angle"])
        self._asteroids = []
        self.setAsteroids(self._data["asteroids"])
        self._bullets = []
        self._firerate = 0
        self._lives = 3

    def update(self, input):
        """
        Updates the wave objects

        Parameter: is a key input
        Precondition: input is a GInput object
        """
        assert isinstance(input, GInput), repr(input)+ ' is not a key input'
        if self._ship != None:
            for asteroid in self._asteroids:
                asteroid.update()
        
            self._ship.update(input)
            self._firerate +=1
            if input.is_key_down('spacebar') and self._firerate >= BULLET_RATE:
                self._addBullet()
            for bullet in self._bullets:
                bullet.update()
            self._removeBullet()
            self._ship_collide()
            self._bullet_collide()

    def draw(self, view):
        """
        Draws the wave objects

        Parameter: view is a GView object
        Precondition: view is a GView object
        """
        assert isinstance(view, GView)
        if self._data != None and self._ship != None:
            self._ship.draw(view)

        if len(self._asteroids) > 0:
            for asteroid in self._asteroids:
                asteroid.draw(view)

        if len(self._bullets) > 0:
            for bullet in self._bullets:
                bullet.draw(view)

    def _removeBullet(self):
        """
        Removes bullets when they cross the deadzones
        """
        i = 0
        while i < len(self._bullets):
            if len(self._bullets) > 0:
                position = self._bullets[i].getPosition() 
                
                if position[0] <= -DEAD_ZONE:
                    self._bullets.remove(self._bullets[i])

                elif position[0] >= GAME_WIDTH + DEAD_ZONE:
                    self._bullets.remove(self._bullets[i])
                    
                elif position[1] <= -DEAD_ZONE:
                    self._bullets.remove(self._bullets[i])
                    
                elif position[1] >= GAME_HEIGHT + DEAD_ZONE:
                    self._bullets.remove(self._bullets[i])
                i+=1
                
    def _addBullet(self):
        """
        Adds bullet to the bullet list
        """
        ship_tip = self._ship.getFacing() * SHIP_RADIUS 
        x = ship_tip.x + self._ship.getPosition()[0]
        y = ship_tip.y + self._ship.getPosition()[1]
        position = [x, y]

        bullet = Bullet(position, self._ship.getFacing())
        self._firerate = 0
        self._bullets.append(bullet)

    def _ship_collide(self):
        """
        Updates ship and asteroid when they collide
        """
        for asteroid in self._asteroids:
            if self._ship != None and len(self._asteroids) > 0:
                if self._ship.has_crashed(asteroid):
                    self.setLives(self._lives - 1)
                    self._replace_asteroid(self._ship, asteroid)
                    self._ship = None
                    self._asteroids.remove(asteroid)

    def _bullet_collide(self):
        """
        Updates bullet list and asteroid when they collide
        """
        for asteroid in self._asteroids:
            for bullet in self._bullets:
                if len(self._bullets) > 0 and len(self._asteroids) > 0:
                    if bullet.has_crashed(asteroid):
                        self._replace_asteroid(bullet, asteroid)
                        self._bullets.remove(bullet)
                        self._asteroids.remove(asteroid)

    def _replace_asteroid(self, item1, item2):
        """
        Replaces big asteroids with smaller asteroids

        Parameter item1:
        Precondition: item1 is a Bullet object or a Ship object

        Parameter item2:
        Precondition: item2 is an Asteroid object
        """
        assert isinstance(item1, (Bullet, Ship))
        assert isinstance(item2, Asteroid)
        if item2.getSize() == MEDIUM_ASTEROID:
            self._breaks_asteroid(item1, item2, SMALL_ASTEROID)
        elif item2.getSize() == LARGE_ASTEROID:
            self._breaks_asteroid(item1, item2, MEDIUM_ASTEROID)

    def gameWon(self):
        """
        Returns True when the game is won
        """
        if len(self._asteroids) == 0 and self._lives > 0:
            return True

    def gameLost(self):
        """
        Returns True when the game is lost
        """
        if self._lives <= 0:
            return True

    def _breaks_asteroid(self, item1, item2, size):
        """
        Breaks big asteroids into smaller asteroids

        Parameter item1: is a Bullet object or a Ship object
        Precondition: item1 is a Bullet object or a Ship object

        Parameter item2: is the object to be broken
        Precondition: item2 is an Asteroid object

        Parameter size: the size of item2
        Precondition: size is a string
        """
        vector1, vector2, vector3 = item1.resultant_vectors()
        if size == MEDIUM_ASTEROID:
            radius = MEDIUM_RADIUS
            speed = MEDIUM_SPEED
        elif size == SMALL_ASTEROID:
            radius = SMALL_RADIUS
            speed = SMALL_SPEED
        position = [radius*vector1.x + item2.x, 
                    radius*vector1.y + item2.y]
        velocity = vector1 * speed
        asteroid1 = {"size" : size,
                     "position" : position,
                     "velocity" : velocity}
        position = [radius*vector2.x + item2.x, 
                    radius*vector2.y + item2.y]
        velocity = vector2 * speed
        asteroid2 = {"size" : size,
                     "position" : position,
                     "velocity" : velocity}
        position = [radius*vector3.x + item2.x, 
                    radius*vector3.y + item2.y]
        velocity = vector3 * speed
        asteroid3 = {"size" : size,
                     "position" : position,
                     "velocity" : velocity}
        asteroids = [asteroid1, 
                     asteroid2, 
                     asteroid3]
        self.setAsteroids(asteroids)

