"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that you
interact with on the screen is model: the ship, the bullets, and the planetoids.

We need models for these objects because they contain information beyond the simple
shapes like GImage and GEllipse. In particular, ALL of these classes need a velocity
representing their movement direction and speed (and hence they all need an additional
attribute representing this fact). But for the most part, that is all they need. You
will only need more complex models if you are adding advanced features like scoring.

You are free to add even more models to this module. You may wish to do this when you
add new features to your game, such as power-ups. If you are unsure about whether to
make a new class or not, please ask on Ed Discussions.

Name: Mensah Jephthah Kwame(jkm255)
Date: Nov 8, 2022
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a 
# parameter in your method, and Wave should pass it as a argument when it calls 
# the method.

# START REMOVE
# HELPER FUNCTION FOR MATH CONVERSION
def degToRad(deg):
    """
    Returns the radian value for the given number of degrees
    
    Parameter deg: The degrees to convert
    Precondition: deg is a float
    """
    return math.pi*deg/180

def is_number(num):
    """
    Returns True if parameter num is an instance of int or float

    Parameter num: the object to be checked
    Precondition: num is an object or type
    """
    if isinstance(num, int) or isinstance(num, float):
        return True

def has_objects(items, instance):
    """
    Returns True if all the elements in the parameter items 
    are instances of parameter instance if instance is not a tuple
    or instances of the instances in parameter instance if instance
    is a tuple

    Parameter items: list that contains objects
    Precondition: items is a list 

    Parameter instance: a Class or Subclass or Tuple
    Precondition: instance is a or tuple of subClass of class object 
    """
    assert isinstance(items, list)
    assert isinstance(instance, object) or isinstance(instance, list)

    if isinstance(instance, list):
        for item in instance:
            assert isinstance(item, object)
    x = 0
    for item in items:
        if isinstance(item, instance):
            x+=1
    if x == len(items):
        return True


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship
    
    Bullets are typically just white circles (ellipses). The size of the bullet is 
    determined by constants in consts.py. However, we MUST subclass GEllipse, because 
    we need to add an extra attribute for the velocity of the bullet.
    
    The class Wave will need to look at this velocity, so you will need getters for
    the velocity components. However, it is possible to write this assignment with no 
    setters for the velocities. That is because the velocity is fixed and cannot change 
    once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GEllipse as a
    helper. This init will need a parameter to set the direction of the velocity.
    
    You also want to create a method to update the bolt. You update the bolt by adding
    the velocity to the position. While it is okay to add a method to detect collisions
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #Attribute _velocity: velocity of the bullet
    #Invariant: velocity is a vector
    
    #Attribute _position: position of the bullet
    #Invariant: position is a list of ints or floats

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO SET THE POSITION AND VELOCITY
    
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)


    def getPosition(self):
        """
        Returns the position of a bullet
        """
        return self._position

    def setPosition(self, position):
        """
        Sets the position of a bullet

        Parameter position: is the new position to be set
        Precondition: position is a list of ints or float
        """
        assert isinstance(position, list)
        assert has_objects(position, (int, float))

        self._position = position[0], position[1]
        self._position = list(self._position)
        self.x, self.y =  self._position[0], self._position[1]

    def __init__(self, position, ship_facing):
        """
        Initializes a bullet object

        Parameter position: is the position of the bullet
        Precondition: position is a list of ints or floats

        Parameter ship_facing: is the facing of the ship
        Precodition: ship_facing is a Vector2 object
        """
        assert isinstance(position, list)
        assert isinstance(ship_facing, Vector2)
        assert has_objects(position, (int, float))

        super().__init__(fillcolor = BULLET_COLOR,
                         x = position[0],
                         y = position[1],
                         width = BULLET_RADIUS * 2,
                         height = BULLET_RADIUS * 2)

        self._velocity = BULLET_SPEED * ship_facing
        self._position = [self.x, self.y]

    def _move(self):
        """
        Moves a bullet object
        """
        position = self._position 
        position[0] = position[0] + self._velocity.x
        position[1] = position[1] + self._velocity.y
        
        self.setPosition(position) 

    def update(self):
        """
        Updates a bullet object
        """
        self._move()

    def has_crashed(self, asteroid):
        """
        Checks if a bullet object has crashed with an asteroid

        Parameter asteroid: is the asteroid to be checked
        Precondition: asteroid is an Asteroid object
        """
        assert isinstance(asteroid, Asteroid)
        squared_distance = (self.x - asteroid.x)**2 + (self.y - asteroid.y)**2
        squared_radii = (self.width/2 + asteroid.width/2)**2
        return  squared_radii > squared_distance

    def resultant_vectors(self):
        """
        Returns the collition vector and the resultant vectors 
        of the collition vector after 120 degree rotation of 
        the collition vector
        """
        o = degToRad(120)
        collition_vector = self._velocity.normal()
        result_vector1 = (collition_vector.x*math.cos(o) - collition_vector.y*math.sin(o),
                          collition_vector.x*math.sin(o) + collition_vector.y*math.cos(o))
        result_vector1 = Vector2(result_vector1[0], result_vector1[1])
        result_vector1.normalize()

        o = degToRad(-120)
        result_vector2 = (collition_vector.x*math.cos(o) - collition_vector.y*math.sin(o),
                          collition_vector.x*math.sin(o) + collition_vector.y*math.cos(o))
        result_vector2 = Vector2(result_vector2[0], result_vector2[1])
        result_vector2.normalize()
        return collition_vector, result_vector1, result_vector2


class Ship(GImage):
    """
    A class to represent the game ship.
    
    This ship is represented by an image. The size of the ship is determined by constants 
    in consts.py. However, we MUST subclass GEllipse, because we need to add an extra 
    attribute for the velocity of the ship, as well as the facing vecotr (not the same)
    thing.
    
    The class Wave will need to access these two values, so you will need getters for 
    them. But per the instructions,these values are changed indirectly by applying thrust 
    or turning the ship. That means you won't want setters for these attributes, but you 
    will want methods to apply thrust or turn the ship.
    
    This class needs an __init__ method to set the position and initial facing angle.
    This information is provided by the wave JSON file. Ships should start with a shield
    enabled.
    
    Finally, you want a method to update the ship. When you update the ship, you apply
    the velocity to the position. While it is okay to add a method to detect collisions 
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #Attribute _velocity: velocity of the ship
    #Invariant: velocity is a vector
    
    #Attribute _position: position of the ship
    #Invariant: _position is a list of ints or floats
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    #Attribute _facing: facing of the ship
    #Invariant: _facing is a vector
    
    # INITIALIZER TO CREATE A NEW SHIP
    
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def getVelocity(self):
        """
        Returns the velocity of a ship
        """
        return self._velocity

    def setVelocity(self, velocity):
        """
        Sets the velocity of a ship

        Parameter velocity: the new velocity to be set
        Precondition: velocity is a Vector2 object
        """
        assert isinstance(velocity, Vector2)
        self._velocity = velocity

    def getFacing(self):
        """
        Returns the facing of a ship
        """
        return self._facing

    def setFacing(self, angle):
        """
        Sets the facing of a ship

        Parameter angle: the angle to be used for the new ship facing
        Precondition: angle is a number
        """
        assert is_number(angle)
        self._facing = Vector2(math.cos(degToRad(angle)), 
                               math.sin(degToRad(angle)))

    def getPosition(self):
        """
        Returns the position of a ship
        """
        return self._position

    def setPosition(self, position):
        """
        Sets the new position of ship

        Parameter position: the new position to be set
        Precondition: position is a list of ints or floats
        """
        assert isinstance(position, list)
        assert has_objects(position, (int, float))

        self._position = position[0], position[1]
        self._position = list(self._position)
        self.x, self.y =  self._position[0], self._position[1]

    def __init__(self, position, angle):
        """
        Initializes a ship object

        Parameter position: is the position of the bullet
        Precondition: position is a list of ints or floats

        Parameter angle: is used to set the facing of the ship
        Precondition: angle is a number
        """
        assert is_number(angle)
        assert isinstance(position, list)
        assert has_objects(position, (int, float))

        self._velocity = Vector2()

        super().__init__(x = position[0],
                         y = position[1],
                         width = SHIP_RADIUS * 2,
                         height = SHIP_RADIUS * 2,
                         source = SHIP_IMAGE,
                         angle = angle)

        self._position = [self.x, self.y]
        self._facing = Vector2(math.cos(degToRad(self.angle)),
                               math.sin(degToRad(self.angle)))

    def _turn(self, angle):
        """
        Turns the ship

        Parameter angle: the angle to which the ship is turned
        Precondition: angle is an int or float
        """
        assert isinstance(angle, (int, float))

        self.angle = angle
        self.setFacing(self.angle)

    def _turn_left(self, input):
        """
        Turns the ship left

        Parameter input: input is a key input
        Precondition: input is an instance of GInput
        """
        assert isinstance(input, GInput), repr(input)+ ' is not a key input'

        if input.is_key_down('left'):
            self._turn(self.angle + SHIP_TURN_RATE)

    def _turn_right(self, input):
        """
        Turns the ship right

        Parameter input: input is a key input
        Precondition: input is an instance of GInput
        """
        assert isinstance(input, GInput), repr(input)+ ' is not a key input'

        if input.is_key_down('right'):
            self._turn(self.angle - SHIP_TURN_RATE)

    def _thrust(self, input):
        """
        Moves the ship forward

        Parameter input: input is a key input
        Precondition: input is an instance of GInput
        """
        assert isinstance(input, GInput), repr(input)+ ' is not a key input'

        impulse = self._facing * SHIP_IMPULSE

        if input.is_key_down('up'):
            self.setVelocity(self._velocity + impulse)

            if self._velocity.length() > SHIP_MAX_SPEED:
                self.setVelocity(SHIP_MAX_SPEED * self._velocity.normal())

            position = self._position
            position[0] = position[0] + self._velocity.x
            position[1] = position[1] + self._velocity.y

            self.setPosition(position)
        else:
            position = self._position
            position[0] = position[0] + self._velocity.x
            position[1] = position[1] + self._velocity.y

            self.setPosition(position)

    def _wrap(self):
        """
        Wraps the ship object
        """
        position = self._position
        
        if position[0] <= -DEAD_ZONE:
            position[0] = position[0] + (GAME_WIDTH + 2*DEAD_ZONE)
        
        if position[0] >= GAME_WIDTH + DEAD_ZONE:
            position[0] = position[0] - (GAME_WIDTH + 2*DEAD_ZONE)
            
        if position[1] <= -DEAD_ZONE:
            position[1] = position[1] + (GAME_HEIGHT + 2*DEAD_ZONE)
            
        if position[1] >= GAME_HEIGHT + DEAD_ZONE:
            position[1] = position[1] - (GAME_HEIGHT + 2*DEAD_ZONE)
        
        if self._position != position:
            self.setPosition(position)

    def update(self, input):
        """
        Updates the ship

        Parameter input: is a key input
        Precondition: input is a GInput object
        """
        assert isinstance(input, GInput), repr(input)+ ' is not a key input'

        self._turn_left(input)
        self._turn_right(input)
        self._thrust(input)
        self._wrap()

    def has_crashed(self, asteroid):
        """
        Checks if asteroid has crashed with ship

        Parameter asteroid: is the asteroid to be checked
        Precondition: asteroid is an Asteroid object
        """
        assert isinstance(asteroid, Asteroid)
        squared_distance = (self.x - asteroid.x)**2 + (self.y - asteroid.y)**2
        squared_radii = (self.width/2 + asteroid.width/2)**2
        return  squared_radii > squared_distance

    def resultant_vectors(self):
        """
        Returns the collition vector and the resultant vectors 
        of the collition vector after 120 degree rotation of 
        the collition vector
        """
        o = degToRad(120)

        if self._velocity.length() == 0:
            collition_vector = self._facing
        else:
            collition_vector =  self._velocity.normal()

        result_vector1 = (collition_vector.x*math.cos(o) - collition_vector.y*math.sin(o),
                            collition_vector.x*math.sin(o) + collition_vector.y*math.cos(o))
        result_vector1 = Vector2(result_vector1[0], result_vector1[1])
        result_vector1.normalize()

        o = degToRad(-120)
        result_vector2 = (collition_vector.x*math.cos(o) - collition_vector.y*math.sin(o),
                            collition_vector.x*math.sin(o) + collition_vector.y*math.cos(o))
        result_vector2 = Vector2(result_vector2[0], result_vector2[1])
        result_vector2.normalize()
        return collition_vector, result_vector1, result_vector2


class Asteroid(GImage):
    """
    A class to represent a single asteroid.
    
    Asteroids are typically are represented by images. Asteroids come in three 
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that 
    determine the choice of image and asteroid radius. We MUST subclass GImage, because 
    we need extra attributes for both the size and the velocity of the asteroid.
    
    The class Wave will need to look at the size and velocity, so you will need getters 
    for them.  However, it is possible to write this assignment with no setters for 
    either of these. That is because they are fixed and cannot change when the planetoid 
    is created. 
    
    In addition to the getters, you need to write the __init__ method to set the size
    and starting velocity. Note that the SPEED of an asteroid is defined in const.py,
    so the only thing that differs is the velocity direction.
    
    You also want to create a method to update the asteroid. You update the asteroid 
    by adding the velocity to the position. While it is okay to add a method to detect 
    collisions in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _size: The size of an asteroid
    # Invariant: _size is a number( int or float) > 0

    # Attribute _velocity: The velocity of an asteroid
    # Invariant: _velocity is a number( int or float)

    #Attribute _position: velocity of the ship
    #Invariant: _position is a list of ints or floats
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW ASTEROID
    
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)

    def getVelocity(self):
        """
        Returns the velocity of the asteroid
        """
        return self._velocity 

    def getSize(self):
        """
        Returns the size of the asteroid
        """
        return self._size

    def getPosition(self):
        """
        Returns the position of the asteroid
        """
        return self._position

    def setPosition(self, position):
        """
        Sets the position of the asteroid

        Parameter position: the new position to be set
        Precondition: position is a list of ints and floats
        """
        assert isinstance(position, list)
        assert has_objects(position, (int, float))

        self._position = position[0], position[1]
        self._position = list(self._position)
        self.x, self.y =  self._position[0], self._position[1]   

    def __init__(self, size, position, direction = None, velocity = None):
        """
        Initializes an asteroid object

        Parameter size: the size of asteroid
        Precondition: size is string

        Parameter position: is used to set the position of the asteroid
        Precondition: position is list of ints or floats

        Parameter: is used to set the direction of the asteroid
        Precondition:direction is a list of ints or floats or direction is None

        Parameter velocity: is used to set the velocity of the asteroid
        Precondition: velocity is a Vector2 object or None
        """
        assert isinstance(size, str)
        assert isinstance(position, list)
        assert has_objects(position, (int, float))
        if velocity != None:
            assert isinstance(velocity, Vector2)
        if direction !=None:
            assert isinstance(direction, list)
            assert has_objects(direction, (int, float))
        self._size = size
        image, radius, speed = self._asteroidKind()
        super().__init__(x = position[0],
                        y = position[1],
                        source = image,
                        width = radius * 2,
                        height = radius * 2)
        if direction != None:
            if direction[0] == 0 and direction[1] == 0:
                self._velocity = Vector2()
            else:
                unit_velocity = Vector2(x = direction[0], 
                                    y = direction[1])
                self._velocity = speed * unit_velocity.normalize()
        elif velocity != None:
            self._velocity = velocity
        self._position = [self.x, self.y]

    def _asteroidKind(self):
        """
        Returns the source, radius, and speed of a kind of asteroid
        """
        if self._size == SMALL_ASTEROID:
            image = SMALL_IMAGE
            radius = SMALL_RADIUS
            speed = SMALL_SPEED

        if self._size == MEDIUM_ASTEROID:
            image = MEDIUM_IMAGE
            radius = MEDIUM_RADIUS
            speed = MEDIUM_SPEED

        if self._size == LARGE_ASTEROID:
            image = LARGE_IMAGE
            radius = LARGE_RADIUS
            speed = LARGE_SPEED

        return image, radius, speed

    def _thrust(self):
        """
        Moves an asteroid
        """
        position = self._position
        position[0] = position[0] + self._velocity.x
        position[1] = position[1] + self._velocity.y

        self.setPosition(position)

    def _wrap(self):
        """
        Wraps an asteroid
        """
        position = self._position
        
        if position[0] <= -DEAD_ZONE:
            position[0] = position[0] + (GAME_WIDTH + 2*DEAD_ZONE)
        
        if position[0] >= GAME_WIDTH + DEAD_ZONE:
            position[0] = position[0] - (GAME_WIDTH + 2*DEAD_ZONE)
            
        if position[1] <= -DEAD_ZONE:
            position[1] = position[1] + (GAME_HEIGHT + 2*DEAD_ZONE)
            
        if position[1] >= GAME_HEIGHT + DEAD_ZONE:
            position[1] = position[1] - (GAME_HEIGHT + 2*DEAD_ZONE)
        
        if self._position != position:
            self.setPosition(position)

    def update(self):
        """
        Updates an asteroid
        """
        self._thrust()
        self._wrap()

