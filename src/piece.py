class Piece:
    def __init__(self, shape, rotation, color, templates, offsets):
        self.shape = shape
        self.rotation = rotation
        self.color = color
        self.templates = templates
        self.offsets = offsets
        self.width = 5
        self.height = 5

    def getTemplate(self):
        return self.templates[self.rotation]

    def getOffsets(self):
        return self.offsets[self.rotation]

    def getRotations(self):
        return len(self.templates)

    def setRotation(self, rotation):
        self.rotation = rotation

    def setX(self, x):
        self.x = x

    def setAction(self, action):
        rotation, column = action
        self.setRotation(rotation)
        self.setX(column)

    def setY(self, y):
        self.y = y - self.offsets[self.rotation][2]
