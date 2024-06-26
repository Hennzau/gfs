import pygame
import numpy as np

from gfs.image import Image

from gfs.fonts import PLAYGROUND_50, PLAYGROUND_30, PLAYGROUND_20, render_font
from gfs.pallet import DARKBLUE, RED, IVORY

from jam.level.tiles import TILE_SIZE, TILE_ROAD, POINT_STONE, TILE_WATER
from jam.level.grid import Grid

from gfs.sounds import PICKUP

from gfs.images import TRUCK_RIGHT, TRUCK_LEFT, TRUCK_UP, TRUCK_DOWN

from gfs.sprite import AnimatedSprite

from gfs.sounds import BUNNY


class Robot:
    def __init__(self, grid):
        self.grid = grid

        self.power = grid.robot_power
        self.power_image = render_font(PLAYGROUND_20, str(int(self.power)), IVORY)

        self.grid_pos = grid.robot_start

        self.render_pos = np.array([self.grid_pos[0], self.grid_pos[1]], dtype=float)
        self.velocity = np.array([0, 0], dtype=float)

        self.entropy = 0

        self.sprite = AnimatedSprite(0, 0, TILE_SIZE, TILE_SIZE, {
            "right": (4, TRUCK_RIGHT),
            "left": (4, TRUCK_LEFT),
            "up": (4, TRUCK_UP),
            "down": (4, TRUCK_DOWN),
        }, 4)

        self.sprite.animate("right")

        self.type = TILE_ROAD
        self.level0 = False

        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.timer = 0.0

    def move_up(self):
        if self.grid_pos[1] - 1 >= 0 and TILE_ROAD == self.grid.get_tile(self.grid_pos[0], self.grid_pos[
                                                                                               1] - 1):
            self.grid_pos[1] -= 1
        elif self.grid_pos[1] - 1 >= 0 and TILE_ROAD != self.grid.get_tile(self.grid_pos[0],
                                                                           self.grid_pos[
                                                                               1] - 1) and self.power > 0:
            self.grid_pos[1] -= 1
            self.power -= 1
            self.build_image()
            self.grid.set_tile(self.grid_pos[0], self.grid_pos[1], TILE_ROAD)
            self.entropy += 1

    def move_down(self):
        if self.grid_pos[1] + 1 < self.grid.height and TILE_ROAD == self.grid.get_tile(self.grid_pos[0],
                                                                                       self.grid_pos[
                                                                                           1] + 1):
            self.grid_pos[1] += 1
        elif self.grid_pos[1] + 1 < self.grid.height and TILE_ROAD != self.grid.get_tile(self.grid_pos[0],
                                                                                         self.grid_pos[
                                                                                             1] + 1) and self.power > 0:
            self.grid_pos[1] += 1
            self.power -= 1
            self.build_image()
            self.grid.set_tile(self.grid_pos[0], self.grid_pos[1], TILE_ROAD)
            self.entropy += 1

    def move_left(self):
        if self.grid_pos[0] - 1 >= 0 and TILE_ROAD == self.grid.get_tile(self.grid_pos[0] - 1,
                                                                         self.grid_pos[1]):
            self.grid_pos[0] -= 1
        elif self.grid_pos[0] - 1 >= 0 and TILE_ROAD != self.grid.get_tile(self.grid_pos[0] - 1,
                                                                           self.grid_pos[
                                                                               1]) and self.power > 0:
            self.grid_pos[0] -= 1
            self.power -= 1
            self.build_image()
            self.grid.set_tile(self.grid_pos[0], self.grid_pos[1], TILE_ROAD)
            self.entropy += 1

    def move_right(self):
        if self.grid_pos[0] + 1 < self.grid.width and TILE_ROAD == self.grid.get_tile(
                self.grid_pos[0] + 1, self.grid_pos[1]):
            self.grid_pos[0] += 1
        elif self.grid_pos[0] + 1 < self.grid.width and TILE_ROAD != self.grid.get_tile(self.grid_pos[0] + 1,
                                                                                        self.grid_pos[
                                                                                            1]) and self.power > 0:
            self.grid_pos[0] += 1
            self.power -= 1
            self.build_image()
            self.grid.set_tile(self.grid_pos[0], self.grid_pos[1], TILE_ROAD)
            self.entropy += 1

    def keyboard_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.up = True
                BUNNY.play()
            elif event.key == pygame.K_DOWN:
                self.down = True
                BUNNY.play()
            elif event.key == pygame.K_LEFT:
                self.left = True
                BUNNY.play()
            elif event.key == pygame.K_RIGHT:
                self.right = True
                BUNNY.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.up = False
            elif event.key == pygame.K_DOWN:
                self.down = False
            elif event.key == pygame.K_LEFT:
                self.left = False
            elif event.key == pygame.K_RIGHT:
                self.right = False

    def build_image(self):
        self.power_image = render_font(PLAYGROUND_20, str(int(self.power)), IVORY)

    def update(self):
        if self.up and self.timer < 0.016:
            self.move_up()
            self.sprite.animate("up")
        if self.down and self.timer < 0.016:
            self.move_down()
            self.sprite.animate("down")
        if self.left and self.timer < 0.016:
            self.move_left()
            self.sprite.animate("left")
        if self.right and self.timer < 0.016:
            self.move_right()
            self.sprite.animate("right")

        if self.up or self.down or self.left or self.right:
            self.timer += 1 / 60
        else:
            self.timer = 0.0

        if self.timer >= 0.3:
            self.timer = 0.0

        self.render_pos += self.velocity * (1 / 60)

        if np.linalg.norm(self.grid_pos - self.render_pos) < 0.05:
            self.render_pos = np.array([self.grid_pos[0], self.grid_pos[1]], dtype=float)
            self.velocity = np.array([0, 0], dtype=float)
        else:
            self.velocity = (self.grid_pos - self.render_pos) * 15

        if self.level0 == False:
            if self.grid.get_points(self.grid_pos[0], self.grid_pos[1]) > 0 and self.grid.get_victory_points(
                    self.grid_pos[0], self.grid_pos[1]) == POINT_STONE:
                self.power += self.grid.get_points(self.grid_pos[0], self.grid_pos[1])
                self.build_image()
                self.grid.set_points_to_zero(self.grid_pos[0], self.grid_pos[1])
                self.entropy += 1
                PICKUP.play()

        if self.level0 == True:
            self.power = 0
