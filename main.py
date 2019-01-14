import pygame
import random

pygame.init()


class Map:
    def __init__(self, size=10):
        self.world_map = []
        self.world_map_last = []
        self.size = size
        self.dead = []
        self.born = []

    def generate(self):
        for i in range(self.size):
            self.world_map.append([])
            self.world_map_last.append([])
            for j in range(self.size):
                self.world_map_last[i].append(0)
                rand = random.randint(0, 100)
                if rand < 10:
                    self.world_map[i].append(1)  # wall
                elif rand < 50:
                    self.world_map[i].append(2)  # fish
                elif rand < 90:
                    self.world_map[i].append(3)  # shrimp
                else:
                    self.world_map[i].append(0)  # nothing

    def draw(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.world_map[i][j] != self.world_map_last[i][j]:
                    print("\033[1;32;30m{}\033[0m".format(self.world_map[i][j]), end=' ')
                    self.world_map_last[i][j] = self.world_map[i][j]
                else:
                    print("{}".format(self.world_map[i][j]), end=' ')
            print()
        print()

    def neighbours(self, x, y):
        fish = 0
        shrimp = 0
        try:
            if self.world_map[x + 1][y] == 2:
                fish += 1
            if self.world_map[x - 1][y] == 2:
                fish += 1
            if self.world_map[x][y + 1] == 2:
                fish += 1
            if self.world_map[x][y - 1] == 2:
                fish += 1

            if self.world_map[x + 1][y] == 3:
                shrimp += 1
            if self.world_map[x - 1][y] == 3:
                shrimp += 1
            if self.world_map[x][y + 1] == 3:
                shrimp += 1
            if self.world_map[x][y - 1] == 3:
                shrimp += 1
        except:
            pass
        return fish, shrimp

    def turn(self):
        self.dead = []
        self.born = []
        for i in range(self.size):
            for j in range(self.size):
                if (self.neighbours(i, j)[0] >= 4 or self.neighbours(i, j)[0] < 2) and self.world_map[i][j] == 2:
                    self.dead.append((i, j))
                if (self.neighbours(i, j)[1] >= 4 or self.neighbours(i, j)[1] < 2) and self.world_map[i][j] == 3:
                    self.dead.append((i, j))
                if self.neighbours(i, j)[0] == 3 and self.world_map[i][j] == 0:
                    self.born.append((i, j, 2))
                if self.neighbours(i, j)[1] == 3 and self.world_map[i][j] == 0:
                    self.born.append((i, j, 3))

        for i in range(len(self.dead)):
            self.world_map[self.dead[i][0]][self.dead[i][1]] = 0
        for i in range(len(self.born)):
            self.world_map[self.born[i][0]][self.born[i][1]] = self.born[i][2]


my_map = Map()
my_map.generate()
my_map.draw()

while True:
    my_map.turn()
    my_map.draw()

    pygame.time.wait(1000)

