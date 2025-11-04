import random
tycoons = [
    "Start",
    "Mumbai-₹2200",
    "Delhi-₹2000",
    "Bangalore-₹1800",
    "Kolkata-₹1600",
    "Chennai-₹1400",
    "Hyderabad-₹1200",
    "Jail",
    "Pune-₹1100",
    "Ahmedabad-₹1000",
    "Jaipur-₹900",
    "Surat-₹800",
    "Lucknow-₹700",
    "Kanpur-₹600",
    "Nagpur-₹500",
    "Visakhapatnam-₹400",
    "Indore-₹300",
    "Ranchi-₹200"
]

money_values = [
    0,2200, 2000, 1800, 1600, 1400, 1200,-1, 1100, 1000,
    900, 800, 700, 600, 500, 400, 300, 200
]
rent = [0.1 * value for value in money_values]
players=int(input("enter number of players "))
print(len(tycoons))

bought_status=[-1]*len(tycoons) 
bought_status[0]=True
pointer=[0]*players
money=[10000]*players
jail_rounds=[0]*players
while True:
    print(bought_status)
    for player in range(players):
        print(bought_status)
        print(f"turn for {player+1} player")
        if jail_rounds[player]!=0:
            print("uh oh! you are stucked for 3 rounds")
            jail_rounds[player]-=1
            continue
        a=int(input("1. Roll 2.Exit\n"))
        if a==1:
            dice=random.randint(1,6)
            print(f"{dice} appeared on dice")
            for i,city in enumerate(tycoons):
                print(i,city)
            pointer[player]=pointer[player]+dice
            print(money[player])
            if pointer[player]>=len(tycoons):
                pointer[player]=(pointer[player]%len(tycoons))
                print("Recieved ₹200")
                money[player]=money[player]+200
                print(money[player])
            print(f"{pointer[player]}\n{tycoons[pointer[player]]}")
            if money_values[pointer[player]]!=-1:
                if bought_status[pointer[player]]==-1:
                    choice=int(input("1. Buy 2.Pass\n" ))
                    if choice==1:
                        if money[player]>=money_values[pointer[player]]:
                            print(f"Congratulations,you bought {tycoons[pointer[player]]}\n")
                            money[player]=money[player]-money_values[pointer[player]]
                            bought_status[pointer[player]]=player
                            print(money[player])
                        else:
                            print("Uh Oh! you are broke!")
                    elif choice==2:
                        continue
                    else:
                        print("not a correct input")
                else:
                    print(rent[pointer[player]])
                    if money[player]>=rent[pointer[player]]:
                        print(f"You paid {rent[pointer[player]]} to player {bought_status[pointer[player]]}")
                        money[player]=money[player]-rent[pointer[player]]
                        money[bought_status[pointer[player]]]=money[bought_status[pointer[player]]]+rent[pointer[player]]
            else:
                if tycoons[pointer[player]]=="Jail":
                    jail=int(input("1. You want to get out by giving ₹150\n2. Stuck for 3 rounds"))
                    if jail==1:
                        money[player]=money[player]-150
                    else:
                        jail_rounds[player]=3

                    
                
            
                    
        else:
            break
    
    
    


            