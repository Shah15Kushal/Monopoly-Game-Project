import pygame
import random
import pygame_menu
pygame.init()
pygame.display.set_caption("Monopoly")
#game resources
exit_game = False
screen_width = 800
screen_height = 800
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow=(255, 255, 0)
purple=(128, 0, 128)
green=(0, 128, 0)
grey= (128, 128, 128)
# loan_text=0
tycoons_colors=[yellow,purple,green,grey,white]
gameWindow = pygame.display.set_mode((screen_width, screen_height))     
pygame.display.update()
clock = pygame.time.Clock()

#game variables
tycoons = [
    "Start","Mumbai","Delhi","Bangalore","Kolkata","Chennai","Airways","Hyderabad","Kochi","Jail",
    "Pune","Ahmedabad","Jaipur","Surat","Nagpur","Dungarpur","Visakhapatnam","Jammu","CLUB",
    "Indore","Ranchi","Bhopal","Patna","Guwahati","Lucknow","Coimbatore","Madurai","Go to Jail",
    "Jodhpur", "Raipur","Allahabad","Vijayawada","Dehradun","Imphal","Siliguri","Manali"
]
curr_player=0
money_values=[0,2500,2200,2100,2100,1800,2000,1500,1100,-1,
              1400,1800,1800,900,1200,1500,900,1800,-1,
              1100,1200,900,1000,1100,1200,900,1300,-1,
              900,700,1400,1000,800,1500,1000,800]
total_players = 2
rent = [int(0.1 * value)  for value in money_values]
money=[20000]*total_players
jail_rounds=[0]*total_players
player_pos = {}
token_colors = [red, blue,green,black]
bought_status=[-1]*len(tycoons)
bought_status[0]=None
# bought_status[tycoons.index("Chance")]=None
# bought_status[tycoons.index("Community Chest")]=None

jail_rounds=[0]*total_players
for i in range(total_players):
    player_pos[f"token_x{i+1}"] = 40 - (i * 10)
    player_pos[f"token_y{i+1}"] = 40 - (i * 10)
pointer = [0] * total_players
dice_rolled= False
in_jail=False
#functions 
def ownership():
    card_size = 75  # Adjust this based on your card size
    for index,owner in enumerate(bought_status):
        if owner is not None and owner in bought_status and owner !=-1:
            card_no = index
            if 0<=card_no<=9:
                y=0
                x=card_no*80
            elif 9<card_no<=18:
                x=725
                card_no=card_no%9
                y=card_no*80
            elif 18<card_no<=27:
                y=725
                card_no=9-(card_no%9)
                x=card_no*80
            else:
                x=0
                card_no=9-(card_no%9)
                y=card_no*80
            pygame.draw.rect(gameWindow, token_colors[owner], (x, y, 75, 20))
        
def cards():
    color_index = 0
    for i in range(0, screen_width, 80):
        pygame.draw.rect(gameWindow, tycoons_colors[color_index], (i, 0, 75, 75))
        pygame.draw.rect(gameWindow, tycoons_colors[color_index], (0, i + 80, 75, 75))
        pygame.draw.rect(gameWindow, tycoons_colors[color_index], (80 + i, 725, 75, 75))
        pygame.draw.rect(gameWindow, tycoons_colors[color_index], (725, 80 + i, 75, 75))
        color_index += 1

        if color_index >= len(tycoons_colors):
            color_index = color_index % len(tycoons_colors)
    ownership()
    money_x,money_y=15,35
    tycoon_x,tycoon_y=5,15
    name=0
    for _ in range(0,screen_width,80):
        text(f"{tycoons[name]}","Times New Roman", 14,black,tycoon_x,tycoon_y)
        tycoon_x+=80
        
        if money_values[name]!=-1:
            text(f"₹{money_values[name]}","Times New Roman", 14,black,money_x,money_y)
        money_x+=80
       
            
        name+=1
    
    tycoon_x,tycoon_y=730,95
    money_x,money_y=735,115
    
    name=10
    
    for i in range(0,screen_width,80):
        text(f"{tycoons[name]}","Times New Roman", 14,black,tycoon_x,tycoon_y)
        tycoon_y+=80
        if money_values[name]!=-1:
            text(f"₹{money_values[name]}","Times New Roman", 14,black,money_x,money_y)
        money_y+=80
        
        name+=1
    tycoon_x,tycoon_y=640,735
    money_x,money_y=650,755
    
    name=19
    for i in range(0,screen_width,80):
        text(f"{tycoons[name]}","Times New Roman", 14,black,tycoon_x,tycoon_y)
        tycoon_x-=80
        if money_values[name]!=-1:
            text(f"₹{money_values[name]}","Times New Roman", 14,black,money_x,money_y)
        money_x-=80
        
        name+=1
    tycoon_x,tycoon_y=5,640
    money_x,money_y=5,660
    
    name=28
    for i in range(0, screen_width, 80):
        if name < len(tycoons) and name < len(money_values):
            
            text(f"{tycoons[name]}", "Times New Roman", 14, black, tycoon_x, tycoon_y)
            tycoon_y -= 80

            if money_values[name] != -1:
                text(f"₹{money_values[name]}", "Times New Roman", 14, black, money_x, money_y)
            money_y -= 80

            name += 1

def tokens(player_pos, colors):
    for i in range(len(player_pos) // 2):
        pygame.draw.circle(gameWindow, colors[i], (player_pos[f"token_x{i+1}"], player_pos[f"token_y{i+1}"]), 5)


def text(text,text_type,text_size,color, x, y):
    
    font = pygame.font.SysFont(text_type, text_size,bold=True)
        
    text=font.render(text,True,color)
    gameWindow.blit(text, (x, y))
    
def roll_dice():
    return random.randint(1, 6)


def move_token(pointer,dice,player_pos,curr_player):
    pointer[curr_player] = pointer[curr_player] + dice
    if pointer[curr_player] <= 9:
        player_pos[f"token_x{curr_player+1}"] += dice * 80
        player_pos[f"token_y{curr_player+1}"] = 40
    elif 9 < pointer[curr_player] <= 18:
        remaining_steps = pointer[curr_player] - 9
        if remaining_steps <= dice:
            player_pos[f"token_x{curr_player+1}"] = 760
            player_pos[f"token_y{curr_player+1}"] += remaining_steps * 80
        else:
            player_pos[f"token_y{curr_player+1}"] += dice * 80
    elif 18 < pointer[curr_player] <= 27:
        remaining_steps = pointer[curr_player] - 18
        if remaining_steps <= dice:
            player_pos[f"token_y{curr_player+1}"] = 760
            player_pos[f"token_x{curr_player+1}"] -= remaining_steps * 80
        else:
            player_pos[f"token_x{curr_player+1}"] -= dice * 80
    elif 27 < pointer[curr_player] <=35:
        remaining_steps = pointer[curr_player] - 27
        if remaining_steps <= dice:
            player_pos[f"token_x{curr_player+1}"] = 40
            player_pos[f"token_y{curr_player+1}"] -= remaining_steps * 80
        else:
            player_pos[f"token_y{curr_player+1}"] -= dice * 80
    else:
        remaining_steps = pointer[curr_player] % len(tycoons)
        if remaining_steps <= dice:
            player_pos[f"token_y{curr_player+1}"] = 40
            
            player_pos[f"token_x{curr_player+1}"] += remaining_steps * 80
        else:
            player_pos[f"token_x{curr_player+1}"] += dice * 80
        money[curr_player]+=200

    pointer[curr_player] = pointer[curr_player] % len(tycoons)
    return pointer, player_pos

def image(img,x,y,width,height):
    full_path =  f"resources/{img}"
    dice_img = pygame.image.load(full_path).convert_alpha()
    dice_img = pygame.transform.scale(dice_img,(width,height))
    gameWindow.blit(dice_img, (x, y))

def user_info(money):
    user_no=1
    for user in range(total_players): 
        
        pygame.draw.rect(gameWindow,(0,255,255),(130+user*450,120,90,25))
        image(f"user{user_no}.png",130+user*450,145,90,60)
        text(f"₹{money[user]}","Courier New",20,white,130+user*455,210)
        text(f"player{user+1}","Courier New",20,black,135+user*450,125)
        # user_no+=1
        if total_players>2 and user+2<total_players:
            pygame.draw.rect(gameWindow,(0,255,255),(580-user*450,550,90,25))
            image(f"user{user_no+2}.png",580-user*450,575,90,60)
            text(f"₹{money[user+2]}","Courier New",20,white,580-user*455,640)
            text(f"player{user+3}","Courier New",20,black,580-user*450,550)
        user_no+=1
        
def chance(dice):
    pygame.draw.rect(gameWindow,black,(360, 360, 80, 80))
    text(f"You landed on a chance with {dice}","Courier New",32,white,135,380)
    if dice==1:
        pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
        text("Insurance payment ₹500","Courier New",32,black,135,380)
        if money[curr_player]>500:
            money[curr_player]-=500
    elif dice==2:
        pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
        text("Its your birthday!Collect ₹200 from each player","Courier New",32,black,135,380)
        for player in range(total_players):
            if player!=curr_player and money[player]>200:
                money[curr_player]+=200
                money[player]-=200
    elif dice==3:
        pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
        text("Marriage,expense of ₹2000","Courier New",32,black,135,380)
        if money[curr_player]>2000:
            money[curr_player]-=2000
    elif dice==4:
        pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
        text("Collect 1000 from bank","Courier New",32,black,135,380)
        money[curr_player]+=1000 
    elif dice==5:
        pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
        text("Go to Start","Courier New",32,black,135,380)
        pointer[curr_player]=tycoons.index("Jail")
        player_pos[f"token_x{curr_player+1}"]=40
        player_pos[f"token_y{curr_player+1}"]=40
    elif dice==6:
        pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
        text("investment returns,5%","Courier New",32,black,135,380)
        money[curr_player]=0.05*money[curr_player]
    pygame.display.update()
    pygame.time.wait(250)
# def community_chest(dice):
#     if dice%2==0:
#         pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
#         text("You found a treasure!Double the you own","Courier New",32,black,135,380)
#         money[curr_player]=2*money[curr_player]
#     else:
#         pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
#         text("Daan hi dharm hai!","Courier New",32,black,135,380)
#         text("donated half for CHARITY","Courier New",32,black,135,390)
#         money[curr_player]/=2
#     pygame.display.update()        
def auction():
    pygame.draw.rect(gameWindow,(129,228,247),(50,50,600,600))
    text("You landed on an Auction!You have following to get it auctioneed!","Courier New",32,black,65,65)
    pass
    
def board():
    gameWindow.fill(black)
    cards()
    tokens(player_pos,token_colors)
    image("dice.png",380,380,40,40)
    text("Roll dice","Times New Roman", 14, white, 375, 375)
    user_info(money) 

board()
pygame.display.update()

def loan():
    pygame.draw.rect(gameWindow,(70,70,70),(360,605,80,30))
    text("Take loan","Times New Roman", 14,white,375,610)
def apply_loan():
    loan_text = ""  
    running = True  

    while running:
        
        board()
        pygame.draw.rect(gameWindow, (128, 128, 128), (360, 605, 200, 30)) 
        text("Type loan amount:", "Times New Roman", 20, white, 365, 580)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    loan_text = loan_text[:-1]  
                elif event.key == pygame.K_RETURN:
                    running = False  
                elif event.unicode.isdigit():  
                    loan_text += event.unicode

        pygame.draw.rect(gameWindow, (128, 128, 128), (360, 605, 200, 30)) 
        text(loan_text, "Times New Roman", 20, white, 370, 610)  
        
        pygame.display.flip()  

    print(f"Final loan amount: {loan_text}")
    # board()
    if loan_text.isdigit():
        interest = 2
        money[curr_player] += int(loan_text) 
    else:
        print("Invalid loan amount entered!")

    
    # interest=2
    # money[curr_player]+=int(loan_text)
    
             
             
             
             
        
while not exit_game:
    loan()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        
        if jail_rounds[curr_player]!=0:
            print("uh oh! you are stucked for 3 rounds")
            pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
            text("uh oh! you are stucked for 3 rounds","Courier New",28,black,135,380)
            jail_rounds[curr_player]-=1
            pygame.display.update()
            pygame.time.wait(1000)
            
            board()
            curr_player=curr_player+1
            if curr_player>=total_players:
                curr_player=curr_player%total_players
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # if 360<=mouse_x<=440 and 605<=mouse_y<=635:
                #     apply_loan()
                #     # board()
                #     dice_rolled=False
                #     print(f"Loan taken! Dice Rolled: {dice_rolled}, Current Player: {curr_player}")

                #     # pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (400, 400)}))
                #     pygame.display.update()
                #     board()
                #     continue
                
                
                if in_jail:                
                    if 300<=mouse_x<=380 and 525<=mouse_y<=555:
                        if money[curr_player]>=300:
                            money[curr_player]-=300
                        in_jail=False
                        board()
                                            
                    elif 360<=mouse_x<=440 and 565<=mouse_y<=595:
                        jail_rounds[curr_player]=3
                        in_jail=False
                        board()
                                        
                                                      
                pygame.display.update()
                
                if not dice_rolled and 370 <= mouse_x <= 440 and 370 <= mouse_y <= 410  :

                    dice = roll_dice()
                    pygame.draw.rect(gameWindow, black, (360, 360, 80, 80))
                    # pygame.display.update()
                    image(f"dice{dice}.png",380,380,40,40)
                    pygame.display.update()
                    pygame.time.wait(250)
                    pointer, player_pos = move_token(pointer, dice, player_pos,curr_player)
                    if money_values[pointer[curr_player]]!=-1:
                        if bought_status[pointer[curr_player]]==-1:   
                            pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
                            text(f"Would you like to buy {tycoons[pointer[curr_player]]} at","Courier New",28,black,135,380)
                            text(f"₹{money_values[pointer[curr_player]]}","Courier New",28,red,350,430)
                            pygame.draw.rect(gameWindow,red,(360,525,80,30))
                            pygame.draw.rect(gameWindow,(111,0,255),(360,565,80,30))
                            text("Buy","Times New Roman", 14,white,390,535)
                            text("Pass","Times New Roman", 14,white,390,570)
                            loan()
                            
                            pygame.display.update()
                            dice_rolled=True
                        elif bought_status[pointer[curr_player]]!=None and bought_status[pointer[curr_player]]!=curr_player:   
                            pygame.draw.ellipse(gameWindow,(0,0,0),(100,300,600,200)) 
                            board()
                            pygame.draw.rect(gameWindow, black, (360, 360, 80, 80))
                            
                            text(f"You paid rent {rent[pointer[curr_player]]} to player{bought_status[pointer[curr_player]] + 1}","Courier New",28, white, 135, 380)
                            
                            money[curr_player]=money[curr_player]-rent[pointer[curr_player]]
                            money[bought_status[pointer[curr_player]]]=money[bought_status[pointer[curr_player]]]+rent[pointer[curr_player]]
                            
                            pygame.display.update()
                            pygame.time.wait(1000)
                            board()
                    else:     
                        if tycoons[pointer[curr_player]]=="Jail":        
                            pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
                            text("You are in jail,you are a criminal","Courier New",28,black,130,380)
                            pygame.draw.rect(gameWindow,red,(300,525,80,30))
                            pygame.draw.rect(gameWindow,(111,0,255),(360,565,80,30))
                            # text("Get released by paying ₹300","Times New Roman", 14,white,390,535)
                            # text("Stuck for 3 rounds","Times New Roman", 14,white,390,570)
                            in_jail=True
                        # elif tycoons[pointer[curr_player]]=="Chance":
                        #     chance(dice)
                        #     pointer,player_pos = move_token(pointer,dice,player_pos,curr_player)
                        #     pygame.time.wait(500)
                        # elif tycoons[pointer[curr_player]]=="Community Chest":
                        #     community_chest(dice)
                        #     pygame.time.wait(500)
                        elif tycoons[pointer[curr_player]]=="Club":
                            money[curr_player]-=150
                            pygame.time.wait(500)
                            
                        elif tycoons[pointer[curr_player]]=="Go to Jail":
                            pointer=tycoons.index("Jail")
                            move_token(pointer,dice,player_pos,curr_player)
                       
                        
                                            
                        
                if dice_rolled :
                    if 360<=mouse_x<=440 and 525<=mouse_y<=555:
                        print("buy button clicked!")
                        if money[curr_player]>=money_values[pointer[curr_player]]:
                            bought_status[pointer[curr_player]]=curr_player
                            money[curr_player]-=money_values[pointer[curr_player]]
                            
                        else:
                            pygame.draw.ellipse(gameWindow,(0,255,145),(100,300,600,200))
                            text("Uh oh you are broke,try takin loan","Courier New",28,black,135,380)
                            pygame.display.update()
                            pygame.time.wait(2000)
                        board()
                        pygame.display.update()
                        dice_rolled=False
                    if 360<=mouse_x<=440 and 565<=mouse_y<=595:
                        dice_rolled=False
                        board()
                    
                        
                        
                        
                        
                
                cards()
                tokens(player_pos, token_colors)
                if not dice_rolled and not in_jail:
                    board()
                    curr_player=curr_player+1
                    if curr_player>=total_players:
                        curr_player=curr_player%total_players
    text(f"Chance for player {curr_player+1}","Courier New",28,white,250,300)
    pygame.display.flip()
pygame.quit()
quit()
