from pygame import *

FPS = 60
TILE_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = 20, 15
WIDTH, HEIGHT = TILE_SIZE*MAP_WIDTH, TILE_SIZE*MAP_HEIGHT

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Maze")#назва вікна
clock = time.Clock()


#завантаження картинок
bg = image.load("background.jpg")
bg = transform.scale(bg, (WIDTH, HEIGHT))

player_img = image.load("hero.png")
enemy_img = image.load("cyborg.png")
wall_img = image.load("wall.png")
all_sprites = sprite.Group()



#створення класу для спрайтів
class BaseSprite(sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x, y, width, height)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)


    def draw(self, window):
        window.blit(self.image, self.rect)




class Player(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.speed = 5
        self.hp = 100
        self.coins_counter = 0
    
    def update(self):
        old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed()
        if keys[K_ESCAPE]:
            run = False
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.image = self.left_image
        if keys[K_d] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed
            self.image = self.right_image

        coll_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)#перевірка на зіткнення зі стіною
        if len(coll_list)>0:
            self.rect.x, self.rect.y = old_pos

class Enemy(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.speed = 3




#створення об'єктів
player1 = Player(player_img, 50, 300, TILE_SIZE - 5, TILE_SIZE - 5)
walls = sprite.Group()
enemys = sprite.Group()



#завантаження карти
with open("map.txt", "r") as file:
    map = file.readlines()
    x, y = 0, 0
    for row in map:
        for symbol in row:
            if symbol == "w":
                walls.add(BaseSprite(wall_img, x, y, TILE_SIZE, TILE_SIZE))
            if symbol == "e":
                enemys.add(Enemy(enemy_img, x, y, TILE_SIZE - 5, TILE_SIZE - 5))
            
            if symbol == "p":
                player1.rect.x = x
                player1.rect.y = y
            x += TILE_SIZE
        x = 0
        y += TILE_SIZE




#головний цикл
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    player1.update()

    window.blit(bg, (0, 0))
    
    all_sprites.draw(window)
    display.update()
    clock.tick(FPS)