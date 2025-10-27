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
        self.state = "splash"

    def start_level(self):
        sprites.clear()

        # Add enemy missiles (so they exist in sprites if active later)
        for enemy_missile in enemy_missiles:
            sprites.append(enemy_missile)

        # Add player
        sprites.append(player)

        # Add missile placeholders
        for missile in missiles:
            sprites.append(missile)

        # Add enemies
        for _ in range(self.level):
            x = random.randint(int(-self.width / 2), int(self.width / 2))
            y = random.randint(int(-self.height / 2), int(self.height / 2))
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
            enemy = Enemy(x, y, "square", "red")
            enemy.dx = dx
            enemy.dy = dy
            sprites.append(enemy)

        # Add powerups
        for _ in range(self.level):
            x = random.randint(int(-self.width / 2), int(self.width / 2))
            y = random.randint(int(-self.height / 2), int(self.height / 2))
            dx = random.uniform(-2, 2)
            dy = random.uniform(-2, 2)
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

    def render_info(self, pen, score, active_enemies=0):
        pen.color("#222255")
        pen.penup()
        pen.goto(400, 0)
        pen.shape("square")
        pen.setheading(90)
        pen.shapesize(10, 32, None)
        pen.stamp()

        pen.color("white")
        pen.width(3)
        pen.goto(300, 400)
        pen.pendown()
        pen.goto(300, -400)

        pen.penup()
        pen.color("white")
        # Some variables referenced here must exist; using globals from script
        character_pen.scale = 1.0
        character_pen.draw_string(pen, "AIRFARTS", 400, 270)
        character_pen.draw_string(pen, "SCORE {}".format(score), 400, 240)
        character_pen.draw_string(pen, "ENEMIES {}".format(active_enemies), 400, 210)
        character_pen.draw_string(pen, "LIVES {}".format(player.lives), 400, 180)
        character_pen.draw_string(pen, "LEVEL {}".format(game.level), 400, 150)

    def start(self):
        self.state = "playing"


class CharacterPen():
    def __init__(self, color="white", scale=1.0):
        self.color = color
        self.scale = scale

        self.characters = {}
        self.characters["1"] = ((-5, 10), (0, 10), (0, -10), (-5, -10), (5, -10))
        self.characters["2"] = ((-5, 10), (5, 10), (5, 0), (-5, 0), (-5, -10), (5, -10))
        self.characters["3"] = ((-5, 10), (5, 10), (5, 0), (0, 0), (5, 0), (5, -10), (-5, -10))
        self.characters["4"] = ((-5, 10), (-5, 0), (5, 0), (2, 0), (2, 5), (2, -10))
        self.characters["5"] = ((5, 10), (-5, 10), (-5, 0), (5, 0), (5, -10), (-5, -10))
        self.characters["6"] = ((5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0), (-5, 0))
        self.characters["7"] = ((-5, 10), (5, 10), (0, -10))
        self.characters["8"] = ((-5, 0), (5, 0), (5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0))
        self.characters["9"] = ((5, -10), (5, 10), (-5, 10), (-5, 0), (5, 0))
        self.characters["0"] = ((-5, 10), (5, 10), (5, -10), (-5, -10), (-5, 10))

        self.characters["A"] = ((-5, -10), (-5, 10), (5, 10), (5, -10), (5, 0), (-5, 0))
        self.characters["B"] = ((-5, -10), (-5, 10), (3, 10), (3, 0), (-5, 0), (5, 0), (5, -10), (-5, -10))
        self.characters["C"] = ((5, 10), (-5, 10), (-5, -10), (5, -10))
        self.characters["D"] = ((-5, 10), (-5, -10), (5, -8), (5, 8), (-5, 10))
        self.characters["E"] = ((5, 10), (-5, 10), (-5, 0), (0, 0), (-5, 0), (-5, -10), (5, -10))
        self.characters["F"] = ((5, 10), (-5, 10), (-5, 0), (5, 0), (-5, 0), (-5, -10))
        self.characters["G"] = ((5, 10), (-5, 10), (-5, -10), (5, -10), (5, 0), (0, 0))
        self.characters["H"] = ((-5, 10), (-5, -10), (-5, 0), (5, 0), (5, 10), (5, -10))
        self.characters["I"] = ((-5, 10), (5, 10), (0, 10), (0, -10), (-5, -10), (5, -10))
        self.characters["J"] = ((5, 10), (5, -10), (-5, -10), (-5, 0))
        self.characters["K"] = ((-5, 10), (-5, -10), (-5, 0), (5, 10), (-5, 0), (5, -10))
        self.characters["L"] = ((-5, 10), (-5, -10), (5, -10))
        self.characters["M"] = ((-5, -10), (-3, 10), (0, 0), (3, 10), (5, -10))
        self.characters["N"] = ((-5, -10), (-5, 10), (5, -10), (5, 10))
        self.characters["O"] = ((-5, 10), (5, 10), (5, -10), (-5, -10), (-5, 10))
        self.characters["P"] = ((-5, -10), (-5, 10), (5, 10), (5, 0), (-5, 0))
        self.characters["Q"] = ((5, -10), (-5, -10), (-5, 10), (5, 10), (5, -10), (2, -7), (6, -11))
        self.characters["R"] = ((-5, -10), (-5, 10), (5, 10), (5, 0), (-5, 0), (5, -10))
        self.characters["S"] = ((5, 8), (5, 10), (-5, 10), (-5, 0), (5, 0), (5, -10), (-5, -10), (-5, -8))
        self.characters["T"] = ((-5, 10), (5, 10), (0, 10), (0, -10))
        self.characters["V"] = ((-5, 10), (0, -10), (5, 10))
        self.characters["U"] = ((-5, 10), (-5, -10), (5, -10), (5, 10))
        self.characters["W"] = ((-5, 10), (-3, -10), (0, 0), (3, -10), (5, 10))
        self.characters["X"] = ((-5, 10), (5, -10), (0, 0), (-5, -10), (5, 10))
        self.characters["Y"] = ((-5, 10), (0, 0), (5, 10), (0, 0), (0, -10))
        self.characters["Z"] = ((-5, 10), (5, 10), (-5, -10), (5, -10))

        self.characters["-"] = ((-3, 0), (3, 0))

    def draw_string(self, pen, s, x, y):
        pen.width(2)
        pen.color(self.color)

        # Center text
        x -= 15 * self.scale * ((len(s) - 1) / 2)
        for character in s:
            self.draw_character(pen, character, x, y)
            x += 15 * self.scale

    def draw_character(self, pen, character, x, y):
        scale = self.scale

        if character in "abcdefghijklmnopqrstuvwxyz":
            scale *= 0.8

        character = character.upper()

        # Check if the character is in the dictionary
        if character in self.characters:
            pen.penup()
            xy = self.characters[character][0]
            pen.goto(x + xy[0] * scale, y + xy[1] * scale)
            pen.pendown()
            for i in range(1, len(self.characters[character])):
                xy = self.characters[character][i]
                pen.goto(x + xy[0] * scale, y + xy[1] * scale)
            pen.penup()


# Splash Screen
character_pen = CharacterPen("red", 3.0)
character_pen.draw_string(pen, "AIRFARTS", 0, 160)

character_pen.scale = 1.0
character_pen.draw_string(pen, "BY MrWapog", 0, 100)

pen.color("white")
pen.shape("triangle")
pen.goto(-150, 20)
pen.stamp()

character_pen.draw_string(pen, "Player", -150, -20)

pen.color("orange")
pen.shape("square")
pen.goto(0, 20)
pen.stamp()
character_pen.draw_string(pen, "Enemy", 0, -20)

pen.shape("circle")
pen.color("blue")
pen.goto(150, 20)
pen.stamp()
character_pen.draw_string(pen, "Powerup", 150, -20)

character_pen.draw_string(pen, "Up Arrow", -100, -60)
character_pen.draw_string(pen, "Accelerate", 100, -60)

character_pen.draw_string(pen, "Left Arrow", -100, -100)
character_pen.draw_string(pen, "Rotate Left", 100, -100)

character_pen.draw_string(pen, "Right Arrow", -100, -140)
character_pen.draw_string(pen, "Rotate Right", 100, -140)

character_pen.draw_string(pen, "Space", -100, -180)
character_pen.draw_string(pen, "Fire", 100, -180)

character_pen.scale = 1.0
character_pen.draw_string(pen, "PRESS S TO START", 0, -240)

wn.tracer(0)


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
        self.radar = 250  # detection radius

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
        # collect ready missiles
        ready = [m for m in missiles if m.state == "ready"]
        num_of_missiles = len(ready)

        # choose directions based on how many ready
        if num_of_missiles == 0:
            return

        if num_of_missiles == 1:
            directions = [0]
        elif num_of_missiles == 2:
            directions = [-5, 5]
        else:
            # cap to 3 directions
            directions = [0, -5, 5]

        # fire missiles (match each ready missile with a direction)
        for i, m in enumerate(ready[: len(directions)]):
            dir_angle = directions[i]
            m.fire(self.x, self.y, self.heading + dir_angle, self.dx, self.dy)

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

            self.x += self.dx
            self.y += self.dy

            self.border_check()

            # Check health
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
            self.fuel -= abs(self.thrust)
            if self.fuel <= 0:
                self.reset()

            self.heading += self.da
            self.heading %= 360

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


class EnemyMissile(Sprite):
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
            self.x = x
            self.y = y
            self.heading = heading
            self.dx = dx
            self.dy = dy

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

    def update(self):
        if self.state == "active":
            self.fuel -= abs(self.thrust)
            if self.fuel <= 0:
                self.reset()

            self.heading += self.da
            self.heading %= 360

            self.x += self.dx
            self.y += self.dy

            self.border_check()

    def reset(self):
        self.fuel = self.max_fuel
        self.dx = 0
        self.dy = 0
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
        self.type = random.choice(["hunter", "mine", "surveillance"])
        # limits for speed
        self.max_dx = 3.0
        self.max_dy = 3.0
        # small default thrust so they move
        self.thrust = 0.02

        if self.type == "hunter":
            self.color = "red"
            self.shape = "square"

        elif self.type == "mine":
            self.color = "orange"
            self.shape = "square"

        elif self.type == "surveillance":
            self.color = "pink"
            self.shape = "square"

    def update(self):
        if self.state == "active":
            self.heading += self.da
            self.heading %= 360

            self.dx += math.cos(math.radians(self.heading)) * self.thrust
            self.dy += math.sin(math.radians(self.heading)) * self.thrust

            self.x += self.dx
            self.y += self.dy

            self.border_check()

            # Check health
            if self.health <= 0:
                self.reset()

            # Code for different types
            if self.type == "hunter":
                if self.x < player.x:
                    self.dx += 0.05
                else:
                    self.dx -= 0.05
                if self.y < player.y:
                    self.dy += 0.05
                else:
                    self.dy -= 0.05

            elif self.type == "mine":
                self.dx = 0
                self.dy = 0

            elif self.type == "surveillance":
                if self.x < player.x:
                    self.dx -= 0.05
                else:
                    self.dx += 0.05
                if self.y < player.y:
                    self.dy -= 0.05
                else:
                    self.dy += 0.05

            # Set max speed
            if self.dx > self.max_dx:
                self.dx = self.max_dx
            elif self.dx < -self.max_dx:
                self.dx = -self.max_dx

            if self.dy > self.max_dy:
                self.dy = self.max_dy
            elif self.dy < -self.max_dy:
                self.dy = -self.max_dy

    def reset(self):
        # mark inactive so level end can detect
        self.state = "inactive"


class Powerup(Sprite):
    def __init__(self, x, y, shape, color):
        super().__init__(x, y, shape, color)


class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, x, y):
        self.x = x
        self.y = y


class Radar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, pen, sprites):
        # Draw radar circle
        pen.color("white")
        pen.setheading(90)
        pen.goto(self.x + self.width / 2.0, self.y)
        pen.pendown()
        pen.circle(self.width / 2.0)
        pen.penup()

        # Draw sprites
        for sprite in sprites:
            if sprite.state == "active":
                radar_x = self.x + (sprite.x - player.x) * (self.width / game.width)
                radar_y = self.y + (sprite.y - player.y) * (self.height / game.height)
                pen.goto(radar_x, radar_y)
                pen.color(sprite.color)
                pen.shape(sprite.shape)
                pen.setheading(sprite.heading)
                pen.shapesize(0.1, 0.1, None)

                # Make sure the sprite is close to the player
                distance = ((player.x - sprite.x) ** 2 + (player.y - sprite.y) ** 2) ** 0.5
                if distance < player.radar:
                    pen.stamp()


# Create game object
game = Game(700, 500)

# Create the radar object
radar = Radar(400, -200, 200, 200)

# Create player sprite
player = Player(0, 0, "triangle", "white")

# Create camera
camera = Camera(player.x, player.y)

# Create missile objects
missiles = []
for _ in range(3):
    missiles.append(Missile(0, 100, "circle", "yellow"))

enemy_missiles = []
for _ in range(1):
    enemy_missiles.append(EnemyMissile(0, 100, "circle", "red"))

# Sprites list
sprites = []

# Setup the level
game.start_level()

# Keyboard bindings
wn.listen()
wn.onkeypress(player.rotate_left, "Left")
wn.onkeypress(player.rotate_right, "Right")

wn.onkeyrelease(player.stop_rotation, "Left")
wn.onkeyrelease(player.stop_rotation, "Right")

wn.onkeypress(player.accelerate, "Up")
wn.onkeyrelease(player.decelerate, "Up")

wn.onkeypress(player.fire, "space")

wn.onkeypress(game.start, "s")
wn.onkeypress(game.start, "S")

# Main Loop
while True:
    # Splash
    if game.state == "splash":
        wn.update()

    elif game.state == "playing":
        # Main Game
        # Clear screen
        pen.clear()

        # Update sprites
        for sprite in sprites[:]:
            # update only active/inactive as appropriate
            try:
                sprite.update()
            except Exception:
                # keep loop robust if some update raises
                pass

        # Fire enemy missiles
        for enemy_missile in enemy_missiles:
            if enemy_missile.state == "ready":
                # Find all active enemies
                enemies = [s for s in sprites if isinstance(s, Enemy) and s.state == "active"]
                if enemies:
                    enemy = random.choice(enemies)

                    # Set heading to aim at player (convert atan2 to degrees)
                    heading = math.degrees(math.atan2(player.y - enemy.y, player.x - enemy.x))
                    enemy_missile.fire(enemy.x, enemy.y, heading, enemy.dx, enemy.dy)

        # Check for collisions
        for sprite in sprites:
            if isinstance(sprite, Enemy) and sprite.state == "active":
                if player.is_collision(sprite):
                    sprite.health -= 10
                    player.health -= 10
                    player.bounce(sprite)

                for missile in missiles:
                    if missile.state == "active" and missile.is_collision(sprite):
                        sprite.health -= 10
                        missile.reset()

            if isinstance(sprite, Powerup):
                if player.is_collision(sprite):
                    # simple powerup effect: teleport out of way
                    sprite.x = 100
                    sprite.y = 100

                for missile in missiles:
                    if missile.state == "active" and missile.is_collision(sprite):
                        sprite.x = 100
                        sprite.y = -100
                        missile.reset()

            # Enemy Missile Collisions with Player
            if isinstance(sprite, EnemyMissile):
                if sprite.state == "active" and sprite.is_collision(player):
                    sprite.reset()
                    player.health -= 10

        # Render sprites
        for sprite in sprites:
            sprite.render(pen, camera.x + 100, camera.y)

        game.render_border(pen, camera.x + 100, camera.y)

        # Check for end of level
        end_of_level = True
        for sprite in sprites:
            # Look for an active enemy
            if isinstance(sprite, Enemy) and sprite.state == "active":
                end_of_level = False
                break
        if end_of_level:
            game.level += 1
            game.start_level()

        # Update the camera
        camera.update(player.x, player.y)

        # Draw text
        game.render_info(pen, player.score, sum(1 for s in sprites if isinstance(s, Enemy) and s.state == "active"))

        # Render the radar
        radar.render(pen, sprites)

        # Update the screen
        wn.update()
