import math
import random
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

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.level = 1

    def start_level(self):
        sprites.clear()

        # Add player
        sprites.append(player)

        # Add missile
        sprites.append(missile)

        # Add enemies
        for _ in range(self.level):
            x = random.randint(int(-self.width / 2), int(self.width / 2))
            y = random.randint(int(-self.height / 2), int(self.height / 2))
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            enemy = Enemy(x, y, "square", "red")
            enemy.dx = dx
            enemy.dy = dy
            sprites.append(enemy)

        # Add powerups
        for _ in range(self.level):
            x = random.randint(int(-self.width / 2), int(self.width / 2))
            y = random.randint(int(-self.height / 2), int(self.height / 2))
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            powerup = Powerup(x, y, "circle", "blue")
            powerup.dx = dx
            powerup.dy = dy
            sprites.append(powerup)

    def render_border(self, pen, x_offset, y_offset):
        pen.color("white")
        pen.width(3)
        pen.penup()

        left = -self.width / 2.0 - x_offset
        right = self.width / 2.0 - x_offset
        top = self.height / 2.0 - y_offset
        bottom = -self.height / 2.0 - y_offset

        pen.goto(left, top)
        pen.pendown()
        pen.goto(right, top)
        pen.goto(right, bottom)
        pen.goto(left, bottom)
        pen.goto(left, top)
        pen.penup()


class Sprite:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.dx = 0
        self.dy = 0
        self.heading = 0
        self.da = 0
        self.thrust = 0.0
        self.acceleration = 0.01
        self.health = 100
        self.max_health = 100
        self.width = 20
        self.height = 20
        self.state = "active"

    def is_collision(self, other):
        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )

    def bounce(self, other):
        temp_dx, temp_dy = self.dx, self.dy
        self.dx, self.dy = other.dx, other.dy
        other.dx, other.dy = temp_dx, temp_dy

    def update(self):
        self.heading += self.da
        self.heading %= 360
        self.dx += math.cos(math.radians(self.heading)) * self.thrust
        self.dy += math.sin(math.radians(self.heading)) * self.thrust
        self.x += self.dx
        self.y += self.dy
        self.border_check()

    def border_check(self):
        if self.x > game.width / 2.0 - 10:
            self.x = game.width / 2.0 - 10
            self.dx *= -1
        elif self.x < -game.width / 2.0 + 10:
            self.x = -game.width / 2.0 + 10
            self.dx *= -1
        if self.y > game.height / 2.0 - 10:
            self.y = game.height / 2.0 - 10
            self.dy *= -1
        elif self.y < -game.height / 2.0 + 10:
            self.y = -game.height / 2.0 + 10
            self.dy *= -1

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()
            self.render_health_meter(pen, x_offset, y_offset)

    def render_health_meter(self, pen, x_offset, y_offset):
        pen.goto(self.x - x_offset - 10, self.y - y_offset + 20)
        pen.width(3)
        pen.pendown()
        pen.setheading(0)

        ratio = self.health / self.max_health
        if ratio < 0.3:
            pen.color("red")
        elif ratio < 0.7:
            pen.color("yellow")
        else:
            pen.color("green")

        pen.fd(20.0 * ratio)
        if self.health != self.max_health:
            pen.color("grey")
            pen.fd(20.0 * ((self.max_health - self.health) / self.max_health))
        pen.penup()


class Player(Sprite):
    def __init__(self, x, y, shape, color):
        super().__init__(x, y, shape, color)
        self.lives = 3
        self.score = 0
        self.heading = 90
        self.da = 0

    def rotate_left(self):
        self.da = 2

    def rotate_right(self):
        self.da = -2

    def stop_rotation(self):
        self.da = 0

    def accelerate(self):
        self.thrust = self.acceleration

    def decelerate(self):
        self.thrust = 0.0

    def fire(self):
        missile.fire(self.x, self.y, self.heading, self.dx, self.dy)

    def update(self):
        if self.state == "active":
            super().update()
            if self.health <= 0:
                self.reset()

    def reset(self):
        self.x, self.y = 0, 0
        self.health = self.max_health
        self.heading = 90
        self.dx = self.dy = 0
        self.lives -= 1

    def render(self, pen, x_offset, y_offset):
        pen.shapesize(0.5, 1.0, None)
        pen.goto(self.x - x_offset, self.y - y_offset)
        pen.setheading(self.heading)
        pen.shape(self.shape)
        pen.color(self.color)
        pen.stamp()
        pen.shapesize(1.0, 1.0, None)
        self.render_health_meter(pen, x_offset, y_offset)


class Missile(Sprite):
    def __init__(self, x, y, shape, color):
        super().__init__(x, y, shape, color)
        self.state = "ready"
        self.thrust = 8.0
        self.max_fuel = 200
        self.fuel = self.max_fuel
        self.height = 4
        self.width = 4

    def fire(self, x, y, heading, dx, dy):
        if self.state == "ready":
            self.state = "active"
            self.x, self.y = x, y
            self.heading = heading
            self.dx = dx + math.cos(math.radians(heading)) * self.thrust
            self.dy = dy + math.sin(math.radians(heading)) * self.thrust

    def update(self):
        if self.state == "active":
            self.fuel -= self.thrust
            if self.fuel <= 0:
                self.reset()
            self.x += self.dx
            self.y += self.dy
            self.border_check()

    def reset(self):
        self.fuel = self.max_fuel
        self.dx = self.dy = 0
        self.state = "ready"

    def render(self, pen, x_offset, y_offset):
        if self.state == "active":
            pen.shapesize(0.2, 0.2, None)
            pen.goto(self.x - x_offset, self.y - y_offset)
            pen.setheading(self.heading)
            pen.shape(self.shape)
            pen.color(self.color)
            pen.stamp()
            pen.shapesize(1.0, 1.0, None)


class Enemy(Sprite):
    def __init__(self, x, y, shape, color):
        super().__init__(x, y, shape, color)
        self.max_health = 20
        self.health = self.max_health

    def update(self):
        super().update()
        if self.health <= 0:
            self.state = "inactive"


class Powerup(Sprite):
    pass


class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x = x
        self.y = y


# Initialize Game
game = Game(700, 500)
player = Player(0, 0, "triangle", "white")
camera = Camera(player.x, player.y)
missile = Missile(0, 100, "circle", "yellow")
sprites = []
game.start_level()

# Controls
wn.listen()
wn.onkeypress(player.rotate_left, "Left")
wn.onkeypress(player.rotate_right, "Right")
wn.onkeyrelease(player.stop_rotation, "Left")
wn.onkeyrelease(player.stop_rotation, "Right")
wn.onkeypress(player.accelerate, "Up")
wn.onkeyrelease(player.decelerate, "Up")
wn.onkeypress(player.fire, "space")

# MAIN LOOP
while True:
    pen.clear()

    for sprite in sprites:
        sprite.update()

    for sprite in sprites:
        if isinstance(sprite, Enemy) and sprite.state == "active":
            if player.is_collision(sprite):
                sprite.health -= 10
                player.health -= 10
                player.bounce(sprite)

            if missile.state == "active" and missile.is_collision(sprite):
                sprite.health -= 10
                missile.reset()

        if isinstance(sprite, Powerup):
            if player.is_collision(sprite):
                sprite.x = 100
                sprite.y = 100
            if missile.state == "active" and missile.is_collision(sprite):
                sprite.x = 100
                sprite.y = -100
                missile.reset()

    for sprite in sprites:
        sprite.render(pen, camera.x, camera.y)

    game.render_border(pen, camera.x, camera.y)

    # End of level
    end_of_level = not any(isinstance(s, Enemy) and s.state == "active" for s in sprites)
    if end_of_level:
        game.level += 1
        game.start_level()

    camera.update(player.x, player.y)
    wn.update()
