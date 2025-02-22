from pygame import *
import random 

init()
font.init()
mixer.init()


FONT = "Play-Bold.ttf"

FPS = 60
TILE_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = 20, 15
WIDTH, HEIGHT = TILE_SIZE*MAP_WIDTH, TILE_SIZE*MAP_HEIGHT

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Maze")#назва вікна
clock = time.Clock()


#завантаження картинок
bg = image.load("image/background.jpg")
bg = transform.scale(bg, (WIDTH, HEIGHT))

player_img = image.load("image/gamer.png")
enemy_img = image.load("image/enemy.png")
wall_img = image.load("image/wall.jpg")
treasure = image.load("image/treasure.png")
coin_img = image.load("image/coin.png")
all_sprites = sprite.Group()
all_labels = sprite.Group()

#завантаження музики
mixer.music.load("jungles.ogg")
mixer.music.set_volume(0.2)
mixer.music.play()

kick_sound = mixer.Sound("kick.ogg")
money_sound = mixer.Sound("money.ogg")

#створення класу для тексту
class Label(sprite.Sprite):
    def __init__(self, text, x, y, fontsize = 30, color = (255, 255, 255), font_name = FONT):
        super().__init__()
        self.color = color
        self.font = font.Font(FONT, fontsize)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_labels.add(self)

    def set_text(self, new_text,color=(255, 255, 255)):
        self.image = self.font.render(new_text, True, color)


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



#створення класу гравця
class Player(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.speed = 4
        self.hp = 100
        self.coins_counter = 0
        self.damage_timer = time.get_ticks()#фіксуєм час від початку гри
    
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

        coll_list = sprite.spritecollide(self, enemys, False, sprite.collide_mask)#перевірка на зіткнення з ворогом
        if len(coll_list)>0:
            now = time.get_ticks()
            if now-self.damage_timer > 1500:
                self.damage_timer = time.get_ticks()#обнуляєм таймер
                self.hp -= 10
                kick_sound.play()
                hp_label.set_text(f"HP: {self.hp}")

            self.rect.x, self.rect.y = old_pos
        
        coll_list = sprite.spritecollide(self, coins, True, sprite.collide_mask)#перевірка на зіткнення з монетою
        if len(coll_list)>0:
            self.coins_counter += 1
            money_sound.play()
            coins_label.set_text(f"Coins: {self.coins_counter}")


class Enemy(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.speed = 2
        self.dir_list = ['left', 'right', 'up', 'down']
        self.dir = random.choice(self.dir_list)

    def update(self):
        old_pos = self.rect.x, self.rect.y

        if self.dir == 'left' and self.rect.x > 0:
            self.rect.x -= self.speed
            self.image = self.right_image
        elif self.dir == 'right':
            self.rect.x += self.speed
            self.image = self.left_image
        elif self.dir == 'up':
            self.rect.y -= self.speed
        elif self.dir == 'down':
            self.rect.y += self.speed

        coll_list = sprite.spritecollide(self, walls, False)#перевірка на зіткнення зі стіною
        if len(coll_list)>0:
            self.rect.x, self.rect.y = old_pos
            self.dir = random.choice(self.dir_list)
        




#створення об'єктів
player1 = Player(player_img, 50, 300, TILE_SIZE - 5, TILE_SIZE - 5)
walls = sprite.Group()
enemys = sprite.Group()
coins = sprite.Group()

#створення тексту
result = Label("", 200, 250, fontsize = 70)
hp_label = Label(f"HP: {player1.hp}", 10, 10)
coins_label = Label(f"Coins: {player1.coins_counter}", 10, 40)
restart = Label("Press R to restart", 300, 450, fontsize = 40)
all_labels.remove(restart)




#завантаження карти
def game_start():
    global exit_sprite, run, finish
    for wall in walls:
        wall.kill()
    for enemy in enemys:
        enemy.kill()
    for coin in coins:
        coin.kill()
    finish = False
    run = True
    player1.hp = 100
    player1.coins_counter = 0
    result.set_text("")
    hp_label.set_text(f"HP: {player1.hp}")
    coins_label.set_text(f"Coins: {player1.coins_counter}")
    mixer.music.play()
    all_labels.remove(restart)


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
                if symbol == "t":
                    exit_sprite = BaseSprite(treasure, x, y, TILE_SIZE, TILE_SIZE)
                if symbol =="c":
                    coins.add(BaseSprite(coin_img, x, y, TILE_SIZE, TILE_SIZE))
                x += TILE_SIZE
            x = 0
            y += TILE_SIZE



    

game_start()
#головний цикл

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_r and finish:
                game_start()
                #enemys.empty()


    

    if player1.hp <= 0:
        finish = True
        kick_sound.play()
        result.set_text("You lose")
        result.rect.x = WIDTH/2 - result.image.get_width()/2
        mixer.music.stop()
        all_labels.add(restart)
        restart.rect.x = WIDTH/2 - restart.image.get_width()/2

        

    if not finish:
        player1.update()
        enemys.update()

    if sprite.collide_rect(player1, exit_sprite):
        finish = True
        result.set_text("You win!")
        result.rect.y = HEIGHT/2 - result.image.get_height()/2
        mixer.music.stop()
        all_labels.add(restart)
        restart.rect.x = WIDTH/2 - restart.image.get_width()/2


    window.blit(bg, (0, 0))
    
    all_sprites.draw(window)
    all_labels.draw(window)
    display.update()
    clock.tick(FPS)