import pygame
import sys
import socket
import threading


server_ip ='127.0.0.1'
port = 8888

pygame.init()
pygame.display.set_caption('1v1_game_client')
height=400
width=600

# sound=pygame.mixer.Sound('Goat - Wayne Jones.mp3')
# sound.play(-1)
# demo video를 위해 주석처리함

enemy_img = pygame.image.load('penguin_blue.png')
enemy_img2 = pygame.image.load('penguin_blue2.png')


en_penguin_height = enemy_img.get_size()[1]
en_penguin_bottom = height - en_penguin_height
en_penguin_x = 50
en_penguin_y = en_penguin_bottom

en_jump_top = 200
en_leg_swap = True
en_is_bottom = True
en_is_go_up = False


enemy_imgice = pygame.image.load('ice.png')
en_ice_height = enemy_imgice.get_size()[1]
en_ice_x = width
en_ice_y = height - en_ice_height


en_running=True

blue_win=pygame.image.load('blue_win.png')
gray_win=pygame.image.load('gray_win.png')
draw = pygame.image.load('draw.png')



def consoles():
    global en_penguin_x, en_penguin_y,en_is_bottom, en_is_go_up

    while True:
        msg = client.recv(1024)
        if(msg.decode()=='up'):
            en_is_go_up = True
            en_is_bottom = False
        if en_is_go_up:
            en_penguin_y -=10
        elif not en_is_go_up and not en_is_bottom:
            en_penguin_y += 10.0
 
        # penguin top and bottom check
        if en_is_go_up and en_penguin_y <= en_jump_top:
            en_is_go_up = False
 
        if not en_is_bottom and en_penguin_y >= en_penguin_bottom:
            en_is_bottom = True
            en_penguin_y = en_penguin_bottom
        

def acceptC():
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((server_ip,port))
    # input()
    thr=threading.Thread(target=consoles,args=())
    thr.Daemon=True
    thr.start()


def GameMain():
    global en_penguin_x,en_penguin_y,en_is_bottom, en_is_go_up, en_ice_x,en_ice_y,en_jump_top,enemy_imgice, enemy_img, en_leg_swap,en_running,blue_win,gray_win,draw
    img = pygame.image.load('penguin_final1.png')
    img2 = pygame.image.load('penguin_final2.png')
    imgh=img.get_size()[1]
    imgw=img.get_size()[0]
    x=50
    penguin_bottom = height - imgh
    y=penguin_bottom

    is_bottom=True
    is_go_up =False
    jump_top=200
    leg_swap = True

    imgice = pygame.image.load('ice.png')
    ice_height = imgice.get_size()[1]
    ice_x = width
    ice_y = height - en_ice_height
    

    running = True


    screen= pygame.display.set_mode((width,height))
    fps = pygame.time.Clock()


    while (en_running and running):
        screen.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if is_bottom:
                    is_go_up = True
                    is_bottom = False
                    msg='up'
                    client.sendall(msg.encode())
        if is_go_up:
            y -= 10.0
        elif not is_go_up and not is_bottom:
            y += 10.0
        
        if is_go_up and y <= jump_top:
            is_go_up = False
 
        if not is_bottom and y >= penguin_bottom:
            is_bottom = True
            y = penguin_bottom
        
        ice_x -= 12.0
        if ice_x <= 0:
            ice_x = width


        if en_is_go_up:
            en_penguin_y -= 10.0
        elif not en_is_go_up and not en_is_bottom:
            en_penguin_y += 10.0
        
        if en_is_go_up and en_penguin_y <= en_jump_top:
            en_is_go_up = False
 
        if not en_is_bottom and en_penguin_y >= en_penguin_bottom:
            en_is_bottom = True
            en_penguin_y = en_penguin_bottom

        en_ice_x -= 12.0
        if en_ice_x <= 0:
            en_ice_x = width
        
        penguin_rect1=pygame.Rect(img.get_rect())
        penguin_rect2=pygame.Rect(img2.get_rect())
        penguin_rect1.left=x
        penguin_rect1.top=y
        penguin_rect2.left=x
        penguin_rect2.top=y
        ice_rect = pygame.Rect(imgice.get_rect())
        ice_rect.left=ice_x
        ice_rect.top=ice_y

        en_penguin_rect1=pygame.Rect(enemy_img.get_rect())
        en_penguin_rect1.left = en_penguin_x
        en_penguin_rect1.top=en_penguin_y
        en_penguin_rect2=pygame.Rect(enemy_img2.get_rect())
        en_penguin_rect2.left=en_penguin_x
        en_penguin_rect2.top=en_penguin_y
        en_ice_rect = pygame.Rect(enemy_imgice.get_rect())
        en_ice_rect.left=en_ice_x
        en_ice_rect.top=en_ice_y


        if ice_rect.colliderect(penguin_rect1) or ice_rect.colliderect(penguin_rect2): # blue
            print("충돌")
            running = False
        if en_ice_rect.colliderect(en_penguin_rect1) or en_ice_rect.colliderect(en_penguin_rect2): # gray
            print("충돌")
            en_running=False
 

        if leg_swap:
            screen.blit(img, (x, y))
            leg_swap = False
        else:
            screen.blit(img2, (x, y))
            leg_swap = True

        if en_leg_swap:
            screen.blit(enemy_img, (en_penguin_x, en_penguin_y))
            en_leg_swap = False
        else:
            screen.blit(enemy_img2, (en_penguin_x, en_penguin_y))
            en_leg_swap = True
        # screen.blit(img,(x,y))
        # screen.blit(enemy_img,(en_penguin_x,en_penguin_y))
        screen.blit(imgice, (ice_x, ice_y))
        screen.blit(enemy_imgice, (en_ice_x, en_ice_y))
        

        pygame.display.update()
        fps.tick(5)
    if(running==True and en_running==False):
        screen.blit(gray_win,(0,0))
    elif(running==False and en_running==True):
        screen.blit(blue_win,(0,0))
    elif(running==False and en_running==False):
        screen.blit(draw,(0,0))
    pygame.display.update()


if __name__ =='__main__':
    acceptC()
    GameMain()
