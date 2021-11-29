import pygame
import pyautogui
import sys
import socket
import threading

server_ip ='127.0.0.1'
port = 8111

pygame.init()
pygame.display.set_caption('1v1_game_client')
height=400
width=800

enemy_img = pygame.image.load('dd.png')


en_dino_height = enemy_img.get_size()[1]
en_dino_bottom = height - en_dino_height
en_dino_x = 50
en_dino_y = en_dino_bottom
en_jump_top = 200
# leg_swap = True
en_is_bottom = True
en_is_go_up = False


enemy_imgTree = pygame.image.load('tree.png')
en_tree_height = enemy_imgTree.get_size()[1]
en_tree_x = width
en_tree_y = height - en_tree_height



def consoles():
    global en_dino_x, en_dino_y,en_is_bottom, en_is_go_up

    while True:
        msg = client.recv(1024)
        if(msg.decode()=='up'):
            en_is_go_up = True
            en_is_bottom = False
        if en_is_go_up:
            en_dino_y -=10
        elif not en_is_go_up and not en_is_bottom:
            en_dino_y += 10.0
 
        # dino top and bottom check
        if en_is_go_up and en_dino_y <= en_jump_top:
            en_is_go_up = False
 
        if not en_is_bottom and en_dino_y >= en_dino_bottom:
            en_is_bottom = True
            en_dino_y = en_dino_bottom

def acceptC():
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((server_ip,port))

    thr=threading.Thread(target=consoles,args=())
    thr.Daemon=True
    thr.start()

def GameMain():
    global en_dino_x,en_dino_y,en_is_bottom, en_is_go_up, en_tree_x,en_tree_y,en_jump_top,enemy_imgTree, enemy_img
    img = pygame.image.load('dd.png')
    imgh=img.get_size()[1]
    imgw=img.get_size()[0]
    x=50
    dino_bottom = height - imgh
    y=dino_bottom
    is_bottom=True
    is_go_up =False
    jump_top=200

    imgTree = pygame.image.load('tree.png')
    tree_height = imgTree.get_size()[1]
    tree_x = width
    tree_y = height - en_tree_height


    screen= pygame.display.set_mode((width,height))
    fps = pygame.time.Clock()

    while True:
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
 
        if not is_bottom and y >= dino_bottom:
            is_bottom = True
            y = dino_bottom
        
        tree_x -= 12.0
        if tree_x <= 0:
            tree_x = width


        if en_is_go_up:
            en_dino_y -= 10.0
        elif not en_is_go_up and not en_is_bottom:
            en_dino_y += 10.0
        
        if en_is_go_up and en_dino_y <= en_jump_top:
            en_is_go_up = False
 
        if not en_is_bottom and en_dino_y >= en_dino_bottom:
            en_is_bottom = True
            en_dino_y = en_dino_bottom

        en_tree_x -= 12.0
        if en_tree_x <= 0:
            en_tree_x = width
 
        screen.blit(img,(x,y))
        screen.blit(enemy_img,(en_dino_x,en_dino_y))
        screen.blit(imgTree, (tree_x, tree_y))
        screen.blit(enemy_imgTree, (en_tree_x, en_tree_y))

        pygame.display.update()
        fps.tick(30)


if __name__ =='__main__':
    acceptC()
    GameMain()

