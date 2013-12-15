
class MoveAction(object):
    def __init__(self, direction):
        self.direction = direction
    
    def __str__(self):
        return "Move in direction %s" % self.direction