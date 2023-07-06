import pygame
from sys import exit
from random import randint



def diaplay_score():
    current_time=(pygame.time.get_ticks()-start_time)//1000
    score_surface=test_font2.render(f'score  {current_time}',False,(64,64,64))
    score_rect=score_surface.get_rect(center=(400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x-=5
            if obstacle_rect.bottom==335:screen.blit(snail_surface, obstacle_rect)
            else: screen.blit(fly_surface,obstacle_rect)
        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x>-100]
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    #play walking animation if player is on floor
    #display jum surface when player is not on floor
    global player_surface,player_index
    if player_rect.bottom<335:
        #jump
        player_surface=player_jump
    else:
        #walk
        player_index+=0.1
        if player_index>=len(player_walk):player_index=0
        player_surface=player_walk[int(player_index)]

pygame.init()
screen=pygame.display.set_mode((800,400))
# screen.fill('Yellow')
pygame.display.set_caption('Dinosaur game ka copy :)')
clock=pygame.time.Clock() #fps
test_font=pygame.font.Font('fonts/Punk kid/punk kid.ttf',40)
test_font2=pygame.font.Font('fonts/Punk kid/punk kid.ttf',30)
test_font3=pygame.font.Font('fonts/Punk kid/punk kid.ttf',60)
game_active=False
start_time=0

background_surface=pygame.image.load('background.jpg').convert_alpha()
background_surface=pygame.transform.scale(background_surface,(800,400))


#obstacles
snail_surface=pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_surface_2=pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames=[snail_surface,snail_surface_2]
snail_frame_index=0
snail_surf=snail_frames[snail_frame_index]

fly_surface=pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_surface_2=pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames=[fly_surface,fly_surface_2]
fly_frame_index=0
fly_surf=fly_frames[fly_frame_index]


obstacle_rect_list=[]

#player
player_surface=pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_surface_2=pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk=[player_surface,player_surface_2]
player_index=0
player_jump=pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_surface=player_walk[player_index]
player_rect=player_surface.get_rect(midbottom=(50,335))
player_gravity=0

#intro
player_stand=pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand=pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect=player_stand.get_rect(center=(400,200))

#timer
obstacle_timer=pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)

score=0
player=pygame.sprite.GroupSingle()
# player.add(Player())



while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and player_rect.bottom==335:
                    player_gravity=-20
        else:
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True
                start_time=pygame.time.get_ticks()

        if game_active:
            if event.type==obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900,1100),335)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900,1100),230)))

            if event.type==snail_animation_timer:
                if snail_frame_index==0:snail_frame_index=1
                else: snail_frame_index=0
                snail_surface=snail_frames[snail_frame_index]

            if event.type==fly_animation_timer:
                if fly_frame_index==0:fly_frame_index=1
                else: fly_frame_index=0
                fly_surface=fly_frames[fly_frame_index]



    if game_active:
        screen.blit(background_surface,(0,0)) #block image transfer, display one image on another


        score=diaplay_score()


        #player
        player_animation()
        screen.blit(player_surface,player_rect)
        player.draw(screen)
        player_gravity+=1
        player_rect.y+=player_gravity
        if player_rect.bottom>=335:
            player_rect.bottom=335

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collisions
        game_active=collisions(player_rect,obstacle_rect_list)


    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom=(50,335)
        player_gravity=0

        game_name = test_font3.render('Runner', False, (111, 196, 169))
        game_name_rect = game_name.get_rect(center=(400, 70))
        screen.blit(game_name,game_name_rect)

        game_message = test_font.render('Press space to start', False, (111, 196, 169))
        game_message_rect = game_message.get_rect(center=(400, 330))

        score_message=test_font.render(f'Your score  {score}',False,(111,196,169))
        score_message_rect=score_message.get_rect(center=(400,330))

        if score==0:screen.blit(game_message,game_message_rect)
        else:screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)