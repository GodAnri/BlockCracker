import pygame
import copy
import os

class Rect:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def scorecalc(broken_blocks):
    if broken_blocks == 0:
        return 0
    else:
        return broken_blocks + scorecalc(broken_blocks - 1)

def lose_life(lives, matrix, start_matrix, score, difficulty):
    broken_blocks = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if start_matrix[row][col] == 1 and matrix[row][col] == 0:
                broken_blocks += 1
    if broken_blocks != 0:
        score += scorecalc(broken_blocks)*100*difficulty
    start_matrix = copy.deepcopy(matrix)
    stick_rect.x = 260
    stick_rect.y = 500
    ball_rect.x = 300
    ball_rect.y = 480
    ball_speed_x = 1
    ball_speed_y = -1
    lives -= 1
    return (stick_rect.x,stick_rect.y,ball_rect.x,ball_rect.y,ball_speed_x,ball_speed_y,lives, matrix, start_matrix, score)

def colliderect(rect1, rect2):
    hcollide = rect1[0] <= rect2[0]+rect2[2] and rect1[0]+rect1[2] >= rect2[0]
    vcollide = rect1[1] <= rect2[1]+rect2[3] and rect1[1]+rect1[3] >= rect2[1]
    return hcollide and vcollide

def block_colision(old_ball_rect, ball_rect, matrix):
    rect = []
    direction = 0
    for i, row in enumerate(matrix):
        for j, block in enumerate(row):
            if block == 1:
                x = j*(block_len_x)
                y = 50 + i*(block_len_y)
                block_rect = (x, y, 540/8, 180/8)
                h_ball_rect = (ball_rect[0], *old_ball_rect[1:])
                # horizontal collision
                if colliderect(h_ball_rect, block_rect):
                    rect.append((i, j))
                    direction = 1
                elif colliderect(ball_rect, block_rect):
                    rect.append((i, j))
                    direction = -1
    return rect, direction

def Loser(win, running, menu, reset, lives, score):
    pygame.mouse.set_visible(True)
    if os.path.exists('highscore.txt'):
        highscore = int(open('highscore.txt', 'r').read())
    else:
        highscore = 0
    if score > highscore:
        highscore = score
        open('highscore.txt', 'w').write(str(highscore))
    while (not menu == True) and (not reset == True):
        pygame.time.delay(1)
        gameover = pygame.image.load("Images/Game Over.png")
        win.blit(gameover, (150,150))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if 239 < x < 356 and 270 < y < 332:
                    reset = True
                    lives = 3
                    return menu, reset, lives, score, highscore
                elif 239 < x < 356 and 360 < y < 422:
                    menu = True
                    lives = 3
                    return menu, reset, lives, score, highscore
    return menu, reset, lives, score, highscore

def Winner(win, running, menu, reset, lives, start_matrix, score, difficulty):
    broken_blocks = 0
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if start_matrix[row][col] == 1 and matrix[row][col] == 0:
                broken_blocks += 1
    if broken_blocks != 0:
        score += scorecalc(broken_blocks)*100*difficulty
    score += 3000*lives
    lives = 3
    pygame.mouse.set_visible(True)
    if os.path.exists('highscore.txt'):
        highscore = int(open('highscore.txt', 'r').read())
    else:
        highscore = 0
    if score > highscore:
        highscore = score
        open('highscore.txt', 'w').write(str(highscore))    
    while (not menu == True) and (not reset == True):
        pygame.time.delay(1)
        gameover = pygame.image.load("Images/Win.png")
        win.blit(gameover, (150,150))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                (x,y) = pygame.mouse.get_pos()
                if 239 < x < 356 and 270 < y < 332:
                    reset = True
                    return menu, reset, lives, score, highscore
                elif 239 < x < 356 and 360 < y < 422:
                    reset = True
                    menu = True
                    return menu, reset, lives, score, highscore
    return menu, reset, lives, score, highscore
    
def Game(win, running, menu, reset, pause, difsel, stick_rect, stick_color, lives, ball_rect, ball_color, ball_speed_x, ball_speed_y, block_len_x, block_len_y, matrix, block_hue, difficulty, score):
    start_matrix = copy.deepcopy(matrix)
    clock = pygame.time.Clock()

    pygame.font.init()
    sldfont = pygame.font.Font(pygame.font.get_default_font(), 48)
    highfont = pygame.font.Font(pygame.font.get_default_font(), 22)

    if os.path.exists('highscore.txt'):
        highscore = int(open('highscore.txt', 'r').read())
    else:
        highscore = 0

    #Running
    while running:
        if difficulty == 1:
            clock.tick(200)
        elif difficulty == 2:
            clock.tick(500)
        else:
            clock.tick(800)
            
        #Main menu
        if menu:
            pygame.mouse.set_visible(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = pygame.mouse.get_pos()
                    if 230 < x < 347 and 284 < y < 346:
                        difsel = True
                        menu = False
                    elif 230 < x < 347 and 412 < y < 474:
                        running = False
        
        if difsel:
            pygame.mouse.set_visible(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = pygame.mouse.get_pos()
                    if 230 < x < 347 and 284 < y < 346:
                        difficulty = 1
                    elif 230 < x < 347 and 348 < y < 410:
                        difficulty = 2
                    elif 230 < x < 347 and 412 < y < 474:
                        difficulty = 3
                    elif 230 < x < 347 and 509 < y < 571:
                        difsel = False
                        reset = True
                
        #In-game
        ##Reset
        elif reset:
            score = 0
            stick_rect = Rect(260, 500, 80, 15)
            lives = 3
            ball_rect = Rect(300,480,10,10)
            ball_speed_x = 1
            ball_speed_y = -1
            matrix = [[0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0]]
            start_matrix = copy.deepcopy(matrix)
            reset = False
        
        ##Pause
        elif pause:
            pygame.mouse.set_visible(True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = pygame.mouse.get_pos()
                    if 239 < x < 356 and 180 < y < 242:
                        pause = False
                    elif 239 < x < 356 and 270 < y < 332:
                        pause = False
                        reset = True
                    elif 239 < x < 356 and 360 < y < 422:
                        pause = False
                        menu = True
        ##Playing        
        else:
            pygame.mouse.set_visible(False)
            #Lose if lives == 0
            if lives == 0:
                menu, reset, lives, score, highscore = Loser(win, running, menu, reset, lives, score)
            
            elif matrix == [[0]*8]*7:
                menu, reset, lives, score, highscore = Winner(win, running, menu, reset, lives, start_matrix, score, difficulty)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEMOTION:
                        if 0 <= event.pos[0] <= 520 and 0 <= event.pos[1] <= 600:
                            stick_rect.x, _ = event.pos
                
                #Key config
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    menu = True
                if keys[pygame.K_LEFT]:
                    if stick_rect.x >= 1:
                        stick_rect.x -= 1
                if keys[pygame.K_RIGHT]:
                    if stick_rect.x <= 519:
                        stick_rect.x += 1
                if keys[pygame.K_p]:
                    pause = True
            
                #Game logics
                ##Ball movement
                old_ball_pos = (ball_rect.x, ball_rect.y)
                ball_rect.x += ball_speed_x
                ball_rect.y += ball_speed_y
                if ball_rect.x + ball_rect.width >= 600:
                    ball_speed_x = -abs(ball_speed_x)
                if ball_rect.x - ball_rect.width <= 0:
                    ball_speed_x = abs(ball_speed_x)
                if ball_rect.y - ball_rect.width <= 0:
                    ball_speed_y = abs(ball_speed_y)
                if stick_rect.x <= ball_rect.x <= stick_rect.x + stick_rect.width and stick_rect.y - stick_rect.height//2 <= ball_rect.y <= stick_rect.y and ball_speed_y > 0:
                    rel_x = 2*((ball_rect.x - stick_rect.x)/stick_rect.width) - 1
                    rel_x = 0.9*rel_x
                    rel_y = -1*(1-rel_x**2)**0.5
                    ball_speed_x = rel_x*2
                    ball_speed_y = rel_y
                    broken_blocks = 0
                    for row in range(len(matrix)):
                        for col in range(len(matrix[0])):
                            if start_matrix[row][col] == 1 and matrix[row][col] == 0:
                                broken_blocks += 1
                    if broken_blocks != 0:
                        score += scorecalc(broken_blocks)*100*difficulty
                    start_matrix = copy.deepcopy(matrix)
                if ball_rect.y > 520:
                    stick_rect.x,stick_rect.y,ball_rect.x,ball_rect.y,ball_speed_x,ball_speed_y,lives, matrix, start_matrix, score = lose_life(lives, matrix, start_matrix, score, difficulty)
                
                
                ##Block collision
                blocks, collision_dir = block_colision(
                    (old_ball_pos[0]-ball_rect.width, old_ball_pos[1]-ball_rect.width, ball_rect.width*2, ball_rect.height*2),
                    (ball_rect.x-ball_rect.width, ball_rect.y-ball_rect.width, ball_rect.width*2, ball_rect.height*2),
                    matrix)
                if collision_dir == -1:  # vertical
                    ball_speed_y = -1*ball_speed_y
                elif collision_dir == 1:  # horizontal
                    ball_speed_x = -1*ball_speed_x
                for i, j in blocks:
                    matrix[i][j] = 0
                
        
        #Drawing
        win.fill((0,0,0))
               
        if not menu:
            block_color = pygame.Color(0)
            block_color.hsva = (int(block_hue), 100, 100, 100)
            block_hue = (block_hue + 0.5) % 360
            
            score_color = (255,0,0) if score > highscore else (255,255,255)
            win.blit(sldfont.render("Score: {0}".format(str(score)), 1, score_color),(20,550))
            win.blit(sldfont.render("Lives: {0}".format(str(lives)), 1, (255,255,255)),(400,550))
            win.blit(sldfont.render("Difficulty: {0}".format(str(difname[difficulty])), 1, (100,100,100)), (difposition[difficulty],20))

            pygame.draw.rect(win, stick_color, (int(stick_rect.x), int(stick_rect.y), stick_rect.width, stick_rect.height))
            pygame.draw.circle(win, ball_color, (int(ball_rect.x), int(ball_rect.y)), ball_rect.width)
            for i, row in enumerate(matrix):
                for j, block in enumerate(row):
                    if block == 1:
                        x = j*(block_len_x)
                        y = 50 + i*(block_len_y)
                        pygame.draw.rect(win, block_color, (x,y, 540/8, 180/8))
            if pause:
                pauseimage = pygame.image.load("Images/Pause Menu.png")
                win.blit(pauseimage,(150,150))
            
            elif difsel:
                if difficulty == 1:
                    difimage = pygame.image.load("Images/Difficulty Easy.png")
                elif difficulty == 2:
                    difimage = pygame.image.load("Images/Difficulty Medium.png")
                else:
                    difimage = pygame.image.load("Images/Difficulty Hard.png")
                win.blit(difimage,(0,0))
    
        elif menu:
            pygame.mouse.set_visible(True)
            menuimage = pygame.image.load("Images/Main Menu.png")
            win.blit(menuimage,(0,0))
            win.blit(highfont.render("Highscore: {0}".format(str(highscore)), 1, (255,255,255)),(20,560))

        pygame.display.update()
        
#Open window
pygame.init()
win = pygame.display.set_mode((600,600))
pygame.display.set_caption("BlockCracker")
running = True
menu = True
pause = False
reset = False
difsel = False

#Config
stick_rect = Rect(260, 500, 80, 15)
stick_color = (255,255,255)
lives = 3
ball_rect = Rect(300,480,10,10)
ball_color = (255,255,255)
ball_speed_x = 1
ball_speed_y = -1
block_len_x = 600/8
block_len_y = 250/8
matrix = [[0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0]]
block_hue = 0
difficulty = 1
score = 0
difname = {1:"Easy",2:"Medium",3:"Hard"}
difposition = {1:120,2:80,3:120}

Game(win, running, menu, reset, pause, difsel, stick_rect, stick_color, lives, ball_rect, ball_color, ball_speed_x, ball_speed_y, block_len_x, block_len_y, matrix, block_hue, difficulty, score)

#Close window
pygame.quit()