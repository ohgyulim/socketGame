import pygame
import pyautogui
import sys
import socket
import threading

server_ip ='127.0.0.1'
port = 8080

pygame.init()
pygame.display.set_caption('1v1_game')
height=960
width=1200

# enemy_img = pygame.image.load('dd.png')
# imgw=enemy_img.get_size()[0]
# imgh=enemy_img.get_size()[1]
# enex=0
# eney=imgw


enemy_imgDino1 = pygame.image.load('dino1.png')
enemy_imgDino2 = pygame.image.load('dino2.png')
enemy_dino_height = enemy_imgDino1.get_size()[1]
enemy_dino_bottom = height-enemy_dino_height
enemy_dino_x = 50
enemy_dino_y = enemy_dino_bottom
enemy_jump_top =200
enemy_leg_swap = True
enemy_is_bottom = True
enemy_is_go_up = False

imgTree = pygame.image.load('tree.png')
tree_height = imgTree.get_size()[1]
tree_x = height
tree_y = height - tree_height


def consoles():
    global enemy_dino_x,enemy_dino_y
    while True:
        msg=client.recv(1024)
        if(msg.decode()=='up' and enemy_is_go_up):
            enemy_dino_y -= 10.0
        elif(not enemy_is_go_up and not enemy_is_bottom):
            enemy_dino_y+=10.0
        
        if (enemy_is_go_up and enemy_dino_y <= enemy_jump_top):
            enemy_is_go_up = False
        if (not enemy_is_bottom and enemy_dino_y >= enemy_dino_bottom):
            enemy_is_bottom =True
            enemy_dino_y = enemy_dino_bottom


    # global eney,enex
    # while True:
    #     msg=client.recv(1024)
    #     if(msg.decode()=='up'):
    #         eney-=30
    #     elif(msg.decoe()=='down'):
    #         eney+=30
    #     elif(msg.decode()=='right'):
    #         enex+=30
    #     elif(msg.decode()=='left'):
    #         enex-=30

def acceptC():
    global client, server, addr
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((server_ip,port))
    server.listen()
    client,addr = server.accept()

    thr=threading.Thread(target=consoles,args=())
    thr.Daemon=True
    thr.start()

def GameMain():
    # set screen, fps
    screen = pygame.display.set_mode((width, height))
    fps = pygame.time.Clock()
 
    # dino
    imgDino1 = pygame.image.load('dino1.png')
    imgDino2 = pygame.image.load('dino2.png')
    dino_height = imgDino1.get_size()[1]
    dino_bottom = height - dino_height
    dino_x = 50
    dino_y = dino_bottom
    jump_top = 200
    leg_swap = True
    is_bottom = True
    is_go_up = False
 
    # tree
    imgTree = pygame.image.load('tree.png')
    tree_height = imgTree.get_size()[1]
    tree_x = width
    tree_y = height - tree_height
 
    while True:
        screen.fill((255, 255, 255))
 
        # event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if is_bottom:
                    is_go_up = True
                    is_bottom = False
 
        # dino move
        if is_go_up:
            dino_y -= 10.0
        elif not is_go_up and not is_bottom:
            dino_y += 10.0
 
        # dino top and bottom check
        if is_go_up and dino_y <= jump_top:
            is_go_up = False
 
        if not is_bottom and dino_y >= dino_bottom:
            is_bottom = True
            dino_y = dino_bottom
 
        # tree move
        tree_x -= 12.0
        if tree_x <= 0:
            tree_x = width
 
        # draw tree
        screen.blit(imgTree, (tree_x, tree_y))
 
        # draw dino
        if leg_swap:
            screen.blit(imgDino1, (dino_x, dino_y))
            leg_swap = False
        else:
            screen.blit(imgDino2, (dino_x, dino_y))
            leg_swap = True
 
        # update
        pygame.display.update()
        fps.tick(30)


    # global eney, enex
    # screen = pygame.display.set_mode((width,height))
    # fps = pygame.time.Clock()

    # img = pygame.image.load('dd.png')
    # imgh=img.get_size()[1]
    # imgw=img.get_size()[0]
    # x=0
    # y=imgw

    # while True:
    #     screen.fill((255,255,255))

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         elif event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_UP:
    #                 pyautogui.keyUp('up')
    #                 y-=30
    #                 msg="up"
    #                 client.sendall(msg.encode())
    #             elif event.key == pygame.K_DOWN:
    #                 pyautogui.keyUp('down')
    #                 y+=30
    #                 msg="down"
    #                 client.sendall(msg.encode())
    #             elif event.key == pygame.K_RIGHT:
    #                 pyautogui.keyUp('right')
    #                 x+=30
    #                 msg="right"
    #                 client.sendall(msg.encode())
    #             elif event.key == pygame.K_LEFT:
    #                 pyautogui.keyUp('left')
    #                 x-=30
    #                 msg="left"
    #                 client.sendall(msg.encode())
        
    #     if img.get_size()[0]+x >= width:
    #         x=width-img.get_size()[0]
    #     elif x <= 0:
    #         x=0
    #     if img.get_size()[1]+y >= height:
    #         y=height-img.get_size()[1]
    #     elif y <=0:
    #         y=0
        
    #     if enemy_img.get_size()[0]+enex >=width:
    #         enex=width-enemy_img.get_size()[0]
    #     elif enex <=0:
    #         enex=0
    #     if enemy_img.get_size()[1]+eney >= height:
    #         eney=height-enemy_img.get_size()[1]
    #     elif eney <=0:
    #         eney =0
        
    #     screen.blit(img,(x,y))
    #     screen.blit(enemy_img,(enex,eney))

    #     pygame.display.update()
    #     fps.tick(60)


if __name__ =='__main__':
    acceptC()
    GameMain()
