from pygame import *
from random import randint

font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
 
font2 = font.SysFont("Arial", 36)
 

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('bow_shoot.mp3')
 

img_back = "minecraft-1106252_1280.jpg"
img_bullet = "arrow.png"
img_hero = "steve-1815647_1920.png"
img_enemy = "minecraft-5187526_1920.png"
img_enemy2 = "1246889.png"
score = 0
goal = 50
lost = 0
max_lost = 20

class GameSprite(sprite.Sprite):
 
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       
       sprite.Sprite.__init__(self)
 
       
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
       
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
   
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)
 
 
class Enemy(GameSprite):
   
   def update(self):
       self.rect.y += self.speed
       global lost
       
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
  
class Bullet(GameSprite):
   
   def update(self):
       self.rect.y += self.speed
       
       if self.rect.y < 0:
           self.kill()

win_width = 900
win_height = 600
display.set_caption("Minecraft")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters2 = sprite.Group()
for i in range(1, 6):
   monster2 = Enemy(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
   monsters2.add(monster2)
bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
   monsters.add(monster)
bullets = sprite.Group()

finish = False

run = True 
while run:
   
   for e in event.get():
       if e.type == QUIT:
           run = False
       
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()
 
   if not finish:
       
       window.blit(background,(0,0))
 
       
       ship.update()
       monsters.update()
       monsters2.update()
       bullets.update()
 
       
       ship.reset()
       monsters.draw(window)
       monsters2.draw(window)
       bullets.draw(window)
       
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)

        
           
           score = score + 1
           monster2 = Enemy(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster2)
 
       
       if sprite.spritecollide(ship, monsters, monsters2, False) or lost >= max_lost:
           finish = True
           window.blit(lose, (200, 200))
 
       
       if score >= goal:
           finish = True
           window.blit(win, (200, 200))
 
      
       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))
 
       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))
 
       display.update()
   
   else:
       finish = False
       score = 0
       lost = 0
       for b in bullets:
           b.kill()
       for m in monsters:
           m.kill()
       for m in monsters2:
           m.kill()    
 
       time.delay(3000)


       for i in range(1, 6):
           monster2 = Enemy(img_enemy2, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
           monsters2.add(monster2)

       for i in range(1, 6):
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
      
 
   time.delay(20)