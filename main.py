import pygame
import os
pygame.font.init()
pygame.mixer.init()
WIDTH,HEIGHT=900,700
BORDER=pygame.Rect(WIDTH/2,0,10,HEIGHT)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,40
VEL=5
BULLET_VEL=7
MAX_BULLETS=3
YELLOW_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2
HEALTH_FONT=pygame.font.SysFont("comicsans",40)
WINNER_FONT=pygame.font.SysFont("comicsans",100)
BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join("Assets","Grenade+1.mp3"))
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join("Assets","Gun+Silencer.mp3"))
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join("Assets","spaceship_red.png"))
RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)
SPACE=pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")),(WIDTH,HEIGHT))
pygame.display.set_caption("First Game")
def draw(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
     WIN.blit(SPACE,(0,0))
     pygame.draw.rect(WIN,BLACK,BORDER)
     red_text=HEALTH_FONT.render("Health :"+str(red_health),1,(255,255,255))
     yellow_text=HEALTH_FONT.render("Health :"+str(yellow_health),1,(255,255,255))
     WIN.blit(red_text,(WIDTH-red_text.get_width()-10,10))
     WIN.blit(yellow_text,(10,10))
     WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
     WIN.blit(RED_SPACESHIP,(red.x,red.y))
     for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
     for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
     pygame.display.update()
def yellow_movement(keys,yellow):
     if keys[pygame.K_a] and yellow.x-VEL>0:
          yellow.x-=VEL
     if keys[pygame.K_d] and yellow.x+VEL+yellow.width<BORDER.x:
          yellow.x+=VEL
     if keys[pygame.K_w] and yellow.y-VEL>0:
            yellow.y-=VEL
     if keys[pygame.K_s] and yellow.y+VEL+yellow.height<HEIGHT-15:
            yellow.y+=VEL
def red_movement(keys,red):
     if keys[pygame.K_LEFT]  and red.x-VEL>BORDER.x+BORDER.width:
          red.x-=VEL
     if keys[pygame.K_RIGHT] and red.x+VEL+red.width<WIDTH:
          red.x+=VEL
     if keys[pygame.K_UP]and red.y-VEL>0:
            red.y-=VEL
     if keys[pygame.K_DOWN] and red.y+VEL+red.height<HEIGHT-15:
            red.y+=VEL
def handle_bullets(yellow_bullet,red_bullet,yellow,red):
    for bullet in yellow_bullet:
        bullet.x+=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)
        elif bullet.x> WIDTH:
            yellow_bullet.remove(bullet)
    for bullet in red_bullet:
        bullet.x-=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullet.remove(bullet)
        elif bullet.x<0:
            red_bullet.remove(bullet)
def draw_text(text):
    draw_test_word=WINNER_FONT.render(text,1,(255,255,255))
    WIN.blit(draw_test_word,(WIDTH//2-draw_test_word.get_width()/2,HEIGHT//2-draw_test_word.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
def main():
    red=pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow=pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullet=[]
    yellow_bullet=[]
    red_health=10
    yellow_health=10
    clock=pygame.time.Clock()
    run=True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_LCTRL and len(yellow_bullet)<MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5)
                    yellow_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()
               if event.key==pygame.K_RCTRL and len(red_bullet)<MAX_BULLETS:
                    bullet=pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type==RED_HIT:
                 red_health-=1
                 BULLET_HIT_SOUND.play()
            if event.type==YELLOW_HIT:
                 yellow_health-=1
                 BULLET_HIT_SOUND.play()
        winner_text=""
        if red_health<=0:
             winner_text="yellow wins!"
        if yellow_health<=0:
             winner_text="red wins!"
        if winner_text!="":
             draw_text(winner_text)
             break
        keys=pygame.key.get_pressed()
        yellow_movement(keys,yellow)
        red_movement(keys,red)
        handle_bullets(yellow_bullet,red_bullet,yellow,red)
        draw(red,yellow,red_bullet,yellow_bullet,red_health,yellow_health)

    main()

if __name__=="__main__":
    main()