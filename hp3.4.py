import pygame,sys,random

pygame.init()

screen = pygame.display.set_mode((800,500))

class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #background image
        self.image=pygame.Surface((310,310))
        self.image.fill(pygame.Color('aqua'))

        #lines
        pygame.draw.line(self.image,(0,0,0),(102.5,0),(102.5,320),5)
        pygame.draw.line(self.image,(0,0,0),(207.5,0),(207.5,320),5)
        pygame.draw.line(self.image,(0,0,0),(0,102.5),(320,102.5),5)
        pygame.draw.line(self.image,(0,0,0),(0,207.5),(320,207.5),5)

        #rect
        self.rect=self.image.get_rect()
        self.rect.center = (400,250)

class Human(pygame.sprite.Sprite):
    def __init__(self,box):
        super().__init__()

        #image
        self.image = pygame.Surface([100, 100]) 
        self.image.fill(pygame.Color('green4')) 
        pygame.draw.rect(self.image,pygame.Color('aqua'),pygame.Rect(0, 0, 100, 100),5)

        #rect
        self.rect = box

        #selection property
        self.selected = False

    def select(self):
        self.selected=True
        pygame.draw.rect(self.image,pygame.Color('khaki'),pygame.Rect(0,0,100,100),5)

    def unselect(self):
        self.selected=False
        pygame.draw.rect(self.image,pygame.Color('aqua'),pygame.Rect(0,0,100,100),5)

    def reset(self,box_no):
        self.rect=boxes[box_no]

    def forward(self):
        self.rect = boxes[boxes.index(self.rect)-3]

    def kill_left(self):
        self.rect = boxes[boxes.index(self.rect)-4]
        for algo in algos:
            if algo.rect.colliderect(self.rect):
                algos.remove(algo)
                chars.remove(algo)
                all_sprite_list.remove(algo)

    def kill_right(self):
        self.rect = boxes[boxes.index(self.rect)-2]
        for algo in algos:
            if algo.rect.colliderect(self.rect):
                algos.remove(algo)
                chars.remove(algo)
                all_sprite_list.remove(algo)

class Algo(pygame.sprite.Sprite):
    def __init__(self,box):
        super().__init__()

        #image
        self.image = pygame.Surface([100, 100]) 
        self.image.fill(pygame.Color('crimson'))
        pygame.draw.rect(self.image,pygame.Color('aqua'),pygame.Rect(0, 0, 100, 100),5) 

        #rect
        self.rect = box

    def reset(self,box_no):
        self.rect=boxes[box_no]

    def forward(self):
        self.rect = boxes[boxes.index(self.rect)+3]

    def kill_left(self):
        self.rect = boxes[boxes.index(self.rect)+2]
        for human in humans:
            if human.rect.colliderect(self.rect):
                humans.remove(human)
                chars.remove(human)
                all_sprite_list.remove(human)

    def kill_right(self):
        self.rect = boxes[boxes.index(self.rect)+4]
        for human in humans:
            if human.rect.colliderect(self.rect):
                humans.remove(human)
                chars.remove(human)
                all_sprite_list.remove(human)

class Move(pygame.sprite.Sprite):
    def __init__(self,box,function):
        super().__init__()

        #image
        self.image=pygame.Surface((100,100))
        self.image.set_alpha(75)

        #rect
        self.rect = box

        #set movement
        self.movement=function

    def move(self):
        self.movement()

class Resetmenu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #image
        self.image=pygame.Surface((800,500))
        self.image.set_colorkey((0,0,0))

        #rect
        self.rect = pygame.rect.Rect(0,0,800,500)
        
        #button
        self.button_rect=pygame.rect.Rect(325,420,150,60)
        pygame.draw.rect(self.image,pygame.Color('darkgoldenrod1'),self.button_rect,0,10)
        pygame.draw.rect(self.image,pygame.Color('darkblue'),self.button_rect,7,10)
        font=pygame.font.SysFont('rockwell',34)
        text = font.render('RESET',True,pygame.Color('indigo'),pygame.Color('darkgoldenrod1'))
        textrect=text.get_rect()
        textrect.center=self.button_rect.center
        self.image.blit(text,textrect)

        #message
        font=pygame.font.SysFont('rockwell',40)
        if win==1:
            win_text='You Win'
        elif win==-1:
            win_text='You Lose'
        else:
            win_text='Error'

        text=font.render(win_text,True,pygame.Color('khaki1'),(0,0,0))
        self.message_rect=text.get_rect()
        self.message_rect.center=(400,50)
        self.image.blit(text,self.message_rect)
        
def check_combination(a,h):
    if len(algos)!=len(a) or len(humans)!=len(h):
        return False
    for i in a:
        if algo_at(i)==dummy:
            return False
    for i in h:
        for human in humans:
            if boxes[i].colliderect(human.rect):
                break
        else:
            return False
    return True

def algo_at(num):
    for algo in algos:
        if algo.rect.colliderect(boxes[num]):
            return algo
    else:
        return dummy

def execute(values):
    box_num,function =  values
    algo=algo_at(box_num)
    match function:
        case 0:
            algo.forward()
        case 1:
            algo.kill_left()
        case 2:
            algo.kill_right()

def flip_board():
    for char in chars:
        ind = boxes.index(char.rect)
        if ind in (0,3,6):
            char.rect=boxes[ind+2]
        elif ind in (2,5,8):
            char.rect=boxes[ind-2]

def algo_move(move_no):
    global current_moves,this_move,all_current_moves,all_this_move
    comb=combs[int(move_no/2)-1]
    for i in range(len(comb)):
        if check_combination(comb[i][0],comb[i][1]):
            current_moves=algo_moves[int(move_no/2)-1][i]
            this_move = random.choice(current_moves)
            all_current_moves.append(current_moves)
            all_this_move.append(this_move)
            execute(this_move)
            return True
    flip_board()
    for i in range(len(comb)):
        if check_combination(comb[i][0],comb[i][1]):
            current_moves=algo_moves[int(move_no/2)-1][i]
            this_move = random.choice(current_moves)
            all_current_moves.append(current_moves)
            all_this_move.append(this_move)
            execute(this_move)
            flip_board()
            return True
    
    return False
    
def find_winner():
    global win
    valid_human_moves=[]
    valid_algo_moves=[]

    if move_no%2==0:

        #end reach check
        for human in humans:
            if boxes.index(human.rect) in (0,1,2):
                win=1
                return
            
        #no algo left
        if algos==[]:
            win=1
            return
        
        #no move left
        for algo in algos:
            #forward box check
            for char in chars:
                if boxes[boxes.index(algo.rect)+3].colliderect(char.rect):
                    break
            else:
                valid_move=Move(boxes[boxes.index(algo.rect)-3],algo.forward)
                valid_algo_moves.append(valid_move)
            #left kill check
            if boxes.index(algo.rect) in (1,2,4,5):
                for human in humans:
                    if boxes[boxes.index(algo.rect)+2].colliderect(human.rect):
                        valid_move=Move(boxes[boxes.index(algo.rect)+2],algo.kill_left)
                        valid_algo_moves.append(valid_move)
                                    
            #right kill check
            if boxes.index(algo.rect) in (0,1,3,4):
                for human in humans:
                    if boxes[boxes.index(algo.rect)+4].colliderect(human.rect):
                        valid_move=Move(boxes[boxes.index(algo.rect)+4],algo.kill_right)
                        valid_algo_moves.append(valid_move)

        if valid_algo_moves==[]:  
            win=1
            return

    else:
        #end reach check
        for algo in algos:
            if boxes.index(algo.rect) in (6,7,8):
                win=-1
                return
            
        #no human left
        if humans==[]:
            win=-1
            return
        
        #human no moves left
        for human in humans:
            #forward box check
            for char in chars:
                if boxes[boxes.index(human.rect)-3].colliderect(char.rect):
                    break
            else:
                valid_move=Move(boxes[boxes.index(human.rect)-3],human.forward)
                valid_human_moves.append(valid_move)
            #left kill check
            if boxes.index(human.rect) in (4,5,7,8):
                for algo in algos:
                    if boxes[boxes.index(human.rect)-4].colliderect(algo.rect):
                        valid_move=Move(boxes[boxes.index(human.rect)-4],human.kill_left)
                        valid_human_moves.append(valid_move)
                                    
            #right kill check
            if boxes.index(human.rect) in (3,4,6,7):
                for algo in algos:
                    if boxes[boxes.index(human.rect)-2].colliderect(algo.rect):
                        valid_move=Move(boxes[boxes.index(human.rect)-2],human.kill_right)
                        valid_human_moves.append(valid_move)
        
        if valid_human_moves==[]: 
            win=-1
            return      

def display_winner():

    #update algo
    update_algo()

    #show menu
    reset_menu = Resetmenu()
    all_sprite_list.add(reset_menu)

    #update screen
    all_sprite_list.update()
    screen.fill(pygame.Color('darkcyan'))
    all_sprite_list.draw(screen)
    pygame.display.flip()

    reset=False
    while not reset:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if reset_menu.button_rect.collidepoint(event.pos):
                    reset_all()
                    reset=True
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

def update_algo():
    global current_moves,this_move,all_current_moves,all_this_move
    if win==-1:
        if current_moves.count(this_move)<2:
            current_moves.append(this_move)
    elif win==1:
        current_moves.remove(this_move)
        if current_moves==[]:
            current_moves=all_current_moves[-2]
            this_move=all_this_move[-2]
            current_moves.remove(this_move)
        if current_moves==[]:
            current_moves=all_current_moves[-3]
            this_move=all_this_move[-3]
            current_moves.remove(this_move)

def reset_all():
    global all_sprite_list,humans,algos,chars,board,a1,a2,a3,h1,h2,h3,dummy,win,move_no
    all_sprite_list.empty()
    win=0
    move_no=1

    h1.reset(6)
    h2.reset(7)
    h3.reset(8)
    humans=[h1,h2,h3]

    a1.reset(0)
    a2.reset(1)
    a3.reset(2)
    #dummy = Algo(pygame.rect.Rect(0,0,0,0))
    algos=[a1,a2,a3]

    chars=[h1,h2,h3,a1,a2,a3]

    all_sprite_list.add(board)
    for i in chars:
        all_sprite_list.add(i)
        
clock = pygame.time.Clock()
all_sprite_list=pygame.sprite.Group()

#elements/sprites
board = Board()

boxes=[]
for i in range(3):
    for j in range(3):
        boxes.append(pygame.rect.Rect(board.rect.x+(j*105),board.rect.y+(i*105),100,100))

h1 = Human(boxes[6])
h2 = Human(boxes[7])
h3 = Human(boxes[8])
humans=[h1,h2,h3]

a1 = Algo(boxes[0])
a2 = Algo(boxes[1])
a3 = Algo(boxes[2])
dummy = Algo(pygame.rect.Rect(0,0,0,0))
algos=[a1,a2,a3]

chars=[h1,h2,h3,a1,a2,a3]

all_sprite_list.add(board)
for i in chars:
    all_sprite_list.add(i)

#combinations
    
comb_of_2=[
    [(0,1,2),(3,7,8)],
    [(0,1,2),(4,6,8)]
]

comb_of_4=[
    [(0,2,3),(4,8)],
    [(1,2,4),(3,8)],
    [(0,2),(3,4,7)],
    [(0,1),(3,5,8)],

    [(1,2,4),(5,6)],
    [(1,2,3),(4,5,6)],
    [(0,2,3),(5,7)],
    [(0,1,5),(3,4,8)],
    [(1,2),(4,8)],
    [(1,2),(4,6)],

    [(0,2),(3,8)]
]

comb_of_6 = [
    [(2,3,4),(5,)],
    [(0,),(3,4,5)],
    [(1,3),(4,5)],
    [(1,5),(3,4)],
    [(0,3,4),(5,)],

    [(2,4,5),(3,)],
    [(2,3),(4,)],
    [(1,4),(3,)],
    [(1,4),(5,)],
    [(0,3),(4,)],
    [(2,5),(4,)]
]

combs = [comb_of_2,comb_of_4,comb_of_6]

#algorithm learnt moves 

algo_moves_2=[
[(1,1),(1,0),(2,0)],
[(0,0),(0,2)]
]

algo_moves_4=[
[(0,2),(2,1),(2,0),(3,0)],
[(1,1),(2,0),(4,0)],
[(0,2),(2,1),(2,0)],
[(1,1),(1,0),(1,2)],

[(1,2),(4,1),(4,0)],
[(1,2),(2,1)],
[(3,0),(3,2)],
[(1,1),(0,2)],
[(2,1),(2,0)],
[(2,1),(2,0)],

[(2,0)]
]

algo_moves_6=[
[(3,0),(4,0)],
[(0,2)],
[(1,2),(3,0)],
[(1,1),(5,0)],
[(3,0),(4,0)],

[(4,0),(5,0)],
[(3,0),(2,1),(2,0)],
[(1,1),(4,0)],
[(1,2),(4,0)],
[(0,2),(3,0)],
[(2,1),(5,0)]
]

algo_moves=[algo_moves_2,algo_moves_4,algo_moves_6]

#game
    
move_no=1
selected = False
win=0
valid_moves=[]
all_current_moves=[]
all_this_move=[]
current_moves=this_move=0

running = True
while running:
    for event in pygame.event.get():

        #quit
        if event.type==pygame.QUIT:
            running=False
            sys.exit()

        if event.type==pygame.MOUSEBUTTONDOWN:
            #select
            if not selected:
                for human in humans:
                    if human.rect.collidepoint(event.pos):
                        human.select()
                        selected=True

                        #forward box check
                        for char in chars:
                            if boxes[boxes.index(human.rect)-3].colliderect(char.rect):
                                break
                        else:
                            valid_move=Move(boxes[boxes.index(human.rect)-3],human.forward)
                            valid_moves.append(valid_move)
                            all_sprite_list.add(valid_move)
                        #left kill check
                        if boxes.index(human.rect) in (4,5,7,8):
                            for algo in algos:
                                if boxes[boxes.index(human.rect)-4].colliderect(algo.rect):
                                    valid_move=Move(boxes[boxes.index(human.rect)-4],human.kill_left)
                                    valid_moves.append(valid_move)
                                    all_sprite_list.add(valid_move)
                                
                        #right kill check
                        if boxes.index(human.rect) in (3,4,6,7):
                            for algo in algos:
                                if boxes[boxes.index(human.rect)-2].colliderect(algo.rect):
                                    valid_move=Move(boxes[boxes.index(human.rect)-2],human.kill_right)
                                    valid_moves.append(valid_move)
                                    all_sprite_list.add(valid_move)

            #select action
            else:
                if valid_moves!=[]:
                    for valid_move in valid_moves:
                        if valid_move.rect.collidepoint(event.pos):
                            valid_move.movement()
                            move_no+=1
                    
                for human in humans:
                    human.unselect()
                selected=False
                for valid_move in valid_moves:
                    all_sprite_list.remove(valid_move)
                valid_moves=[]
            
            


    #update screen
    all_sprite_list.update()
    screen.fill(pygame.Color('darkcyan'))
    all_sprite_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    pygame.time.delay(500)

    #check winner
    find_winner()
    if win!=0:
        display_winner()

    #algorithm move    
    if move_no%2==0:
        algo_move(move_no)
        move_no+=1

    #update screen
    all_sprite_list.update()
    screen.fill(pygame.Color('darkcyan'))
    all_sprite_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)

    #check winner
    find_winner()
    if win!=0:
        display_winner()

    
