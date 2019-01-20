import random
import pygame

pygame.init()


class Map:
    def __init__(self, size=10):
        self.world_map = []
        self.world_map_last = []
        self.size = size
        self.dead = []
        self.born = []

    def generate(self):  # generating map
        self.world_map.append([])
        self.world_map_last.append([])
        for i in range(self.size + 2):
            self.world_map[0].append(0)
            self.world_map_last[0].append(0)

        for i in range(self.size):
            q = i + 1
            self.world_map.append([])
            self.world_map_last.append([])
            self.world_map[q].append(0)
            self.world_map_last[q].append(0)

            for j in range(self.size):
                self.world_map_last[q].append(0)
                rand = random.randint(0, 100)
                if rand < 10:
                    self.world_map[q].append(1)  # wall
                elif rand < 50:
                    self.world_map[q].append(2)  # fish
                elif rand < 90:
                    self.world_map[q].append(3)  # shrimp
                else:
                    self.world_map[q].append(0)  # nothing

            self.world_map[q].append(0)
            self.world_map_last[q].append(0)

        self.world_map.append([])
        self.world_map_last.append([])
        for i in range(self.size + 2):
            self.world_map[-1].append(0)
            self.world_map_last[-1].append(0)

    def draw(self):  # console drawing
        flag = True
        for i in range(self.size + 2):
            for j in range(self.size + 2):
                if self.world_map[i][j] != self.world_map_last[i][j]:
                    print("\033[1;32;30m{}\033[0m".format(self.world_map[i][j]), end=' ')
                    self.world_map_last[i][j] = self.world_map[i][j]
                    flag = False
                else:
                    print("{}".format(self.world_map[i][j]), end=' ')
            print()
        if flag:
            print("No changes happened")
            return True
        print()
        return False

    def draw_pics(self, screen):  # pygame drawing
        sprite_size = (40, 40)
        x_now = 0
        y_now = 0
        spriterect = pygame.Rect(x_now, y_now, sprite_size[0], sprite_size[1])
        fish = pygame.image.load("sprites/fish2.png")
        fish = pygame.transform.scale(fish, sprite_size)
        prawn = pygame.image.load("sprites/prawn.png")
        prawn = pygame.transform.scale(prawn, sprite_size)
        rock = pygame.image.load("sprites/rock2.png")
        rock = pygame.transform.scale(rock, sprite_size)
        for i in range(0, len(self.world_map)):
            for j in range(0, len(self.world_map[i])):
                if self.world_map[i][j] == 1:
                    screen.blit(rock, spriterect)
                elif self.world_map[i][j] == 2:
                    screen.blit(fish, spriterect)
                elif self.world_map[i][j] == 3:
                    screen.blit(prawn, spriterect)
                x_now = x_now + sprite_size[0]
                spriterect = pygame.Rect(x_now, y_now, sprite_size[0], sprite_size[1])
            x_now = 0
            y_now = y_now + sprite_size[1]
            spriterect = pygame.Rect(x_now, y_now, sprite_size[0], sprite_size[1])

    def neighbours(self, x, y):  # checking neighbour squares
        fish = 0
        shrimp = 0
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
        return fish, shrimp

    def turn(self):  # step function
        self.dead = []
        self.born = []
        for i in range(1, self.size+1):
            for j in range(1, self.size+1):
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
