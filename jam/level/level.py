import pygame
import gfs.pallet

from gfs.image import Image
from gfs.sprites import Sprites
from jam.level.tiles import TILE_SIZE, TILE_GRASS, TILE_ROAD, TILE_WATER, TILE_DIRT, POINT_TREE, POINT_STONE
from gfs.fonts import PLAYGROUND_20, render_font

from jam.level.rabbit import Rabbit
from jam.level.robot import Robot
from gfs.images import GRASS_IMAGE, DIRT_IMAGE, ROAD_IMAGE, WATER_IMAGE, TREE_IMAGE, STONE_IMAGE

import numpy as np

from jam.victory_check import check_victory


class Level:
    def __init__(self, grid):
        self.image = Image(grid.width * TILE_SIZE, grid.height * TILE_SIZE)
        self.grid = grid

        self.rabbit = Rabbit(self.grid)
        self.robot = Robot(self.grid)
        self.player = self.rabbit

        self.build_image()

        self.last_player_entropy = 0
        self.sprites = Sprites()
        self.sprites.add_sprite("rabbit", self.rabbit.sprite)
        self.sprites.add_sprite("robot", self.robot.sprite)

        self.victory = False
        self.change_character=False

    def keyboard_input(self, event):
        self.player.keyboard_input(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.change_character=True
            if self.player == self.rabbit:
                self.player = self.robot
            else:
                self.player = self.rabbit

    def mouse_motion(self, event):
        pass

    def mouse_input(self, event):
        pass

    def update(self):
        self.rabbit.update()
        self.robot.update()

        if self.player.entropy != self.last_player_entropy:
            self.build_image()
            self.last_player_entropy = self.player.entropy

            # check if victory

            tile_grass_grid = np.array(self.grid.tiles == TILE_GRASS, dtype=int)
            tile_road_grid = np.array(self.grid.tiles == TILE_ROAD, dtype=int)

            victory_points = np.array(np.where(self.grid.victory_points == POINT_TREE)).T

            # transform it to a list of duets

            victory_points = [(x, y) for x, y in victory_points]
            victory_rabbit = check_victory(tile_grass_grid, victory_points)

            victory_points = np.array(np.where(self.grid.victory_points == POINT_STONE)).T
            victory_points = [(x, y) for x, y in victory_points]
            victory_robot = check_victory(tile_road_grid, victory_points)

            if victory_rabbit and victory_robot:
                self.victory = True

        self.sprites.update()

    def reload(self):
        self.grid.reload()

        self.rabbit = Rabbit(self.grid)
        self.robot = Robot(self.grid)
        self.player = self.rabbit

        self.build_image()

        self.last_player_entropy = 0
        self.sprites = Sprites()
        self.sprites.add_sprite("rabbit", self.rabbit.sprite)
        self.sprites.add_sprite("robot", self.robot.sprite)

    def build_image(self):
        for i in range(self.grid.width):
            for j in range(self.grid.height):
                type = self.grid.get_tile(i, j)
                if type == TILE_ROAD:
                    self.image.draw_image(ROAD_IMAGE, i * TILE_SIZE, j * TILE_SIZE)
                if type == TILE_GRASS:
                    self.image.draw_image(GRASS_IMAGE, i * TILE_SIZE, j * TILE_SIZE)
                if type == TILE_WATER:
                    self.image.draw_image(WATER_IMAGE, i * TILE_SIZE, j * TILE_SIZE)
                if type == TILE_DIRT:
                    self.image.draw_image(DIRT_IMAGE, i * TILE_SIZE, j * TILE_SIZE)

                point_type = self.grid.get_victory_points(i, j)
                if point_type == POINT_TREE:
                    self.image.draw_image(TREE_IMAGE, i * TILE_SIZE, j * TILE_SIZE)
                if point_type == POINT_STONE:
                    self.image.draw_image(STONE_IMAGE, i * TILE_SIZE, j * TILE_SIZE)

                points = self.grid.get_points(i, j)
                if points > 0:
                    power_image = render_font(PLAYGROUND_20, str(int(points)), gfs.pallet.IVORY)
                    self.image.draw_image(power_image,
                                          i * TILE_SIZE + (TILE_SIZE - power_image.get_width()) / 2,
                                          j * TILE_SIZE + (TILE_SIZE - power_image.get_height()) / 2)
