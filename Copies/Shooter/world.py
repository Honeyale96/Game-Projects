import pygame

from decoration import Decoration, Water, Exit
from healthbar import HealthBar
from items import ItemBox
from player import Soldier

class World:
    def __init__(self):
        self.level_length = None
        self.obstacle_list = []

    def process_data(self, tile_size, data, img_list,
                     enemy_group, item_box_group, decoration_group, water_group, exit_group, item_boxes):
        self.level_length = len(data[0])
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * tile_size
                    img_rect.y = y * tile_size
                    tile_data = (img, img_rect)
                    if 0 <= tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif 9 <= tile <= 10:   # water
                        water = Water(img, tile_size, x * tile_size, y * tile_size)
                        water_group.add(water)
                    elif 11 <= tile <= 14:  # decoration
                        decoration = Decoration(img, tile_size, x * tile_size, y * tile_size)
                        decoration_group.add(decoration)
                    elif tile == 15:    # create player
                        player = Soldier('player', x * tile_size, y * tile_size,
                                         1.65, 5, 20, 5, self.obstacle_list, self.level_length)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:    # create enemies
                        enemy = Soldier('enemy', x * tile_size, y * tile_size,
                                        1.65, 2, 20, 0, self.obstacle_list, self.level_length)
                        enemy_group.add(enemy)
                    elif tile == 17:    # Ammo box
                        item_box = ItemBox('Ammo', tile_size, x * tile_size, y * tile_size, item_boxes)
                        item_box_group.add(item_box)
                    elif tile == 18:    # Grenade box
                        item_box = ItemBox('Grenade', tile_size, x * tile_size, y * tile_size, item_boxes)
                        item_box_group.add(item_box)
                    elif tile == 19:    # Health box
                        item_box = ItemBox('Health', tile_size, x * tile_size, y * tile_size, item_boxes)
                        item_box_group.add(item_box)
                    elif tile == 20:    # Exit
                        exit = Exit(img, tile_size, x * tile_size, y * tile_size)
                        exit_group.add(exit)

        return player, health_bar

    def draw(self, screen, screen_scroll):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])