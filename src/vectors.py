
import math

class Vector2(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        
    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)
    
    def getCoords(self):
        return self.x, self.y
    
    @staticmethod
    def from_points(P1, P2):
        return Vector2(P2[0] - P1[0], P2[1] - P2[1])
    
    @staticmethod
    def get_distance(A, B):
        return (B - A).get_magnitude()
    
    def get_magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        magnitude = self.get_magnitude()
        self.x /= magnitude
        self.y /= magnitude
    
    def get_normalized(self):
        mag = self.get_magnitude()
        return mag and Vector2(self.x/mag, self.y/mag) or Vector2(0, 0)
           
    def get_distance_to_DEPRECATED(self, location):
        # optimize later
        return Vector2(self.x - location.x, self.y - location.y).get_magnitude()
        
    def __add__(self, rhs):
        return Vector2(self.x + rhs.x, self.y + rhs.y)
    
    def __sub__(self, rhs):
        return Vector2(self.x - rhs.x, self.y - rhs.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __eq__(self, obj):
        if type(obj) != type(self):
            return False
        return self.x == obj.x and self.y == obj.y 

LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)
DOWN = Vector2(0, 1)
UP = Vector2(0, -1)
STOP = Vector2(0, 0)
        