import turtle

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

wn = turtle.Screen()
wn.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
wn.title("AIRFARTS BY @MrWapog")
wn.bgcolor("black")
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()

class Sprite():
    # THIs is the Contractor
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.dx = 0
        self.dy = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()

# Create player sprite
player = Sprite(0, 0, "triangle", "white")
player.dx = 1
player.dy = 0.5

enemy = Sprite(0, 100, "square", "red")
enemy.dx = -1
enemy.dy = -0.3

powerup = Sprite(0, -100, "circle", "blue")
powerup.dy = 1
powerup.dx = 0.1

#Sprites List
sprites = []
sprites.append(player)
sprites.append(enemy)
sprites.append(powerup)

#Where the magic starts here: MAIN LOOP!
while True:
    #clear screen
    pen.clear()

    #GaMeStuff
    #Update sprites
    for sprite in sprites:
        sprite.update()

    #render sprites
    for sprite in sprites:
        sprite.render(pen)

    #UpdateScreen
    wn.update()



