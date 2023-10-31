import random as r
import json
import csv
import os

hp = 0
coins = 0
damage = 0 

def printParameters():
    print ("У тебя {0} жизней, {1} монет и {2} урона.".format(hp, coins, damage))

def printHp():
    print("У тебя", hp, "жизней.")

def printCoins():
    print("У тебя", coins, "монет.")

def printDamage():
    print("У тебя", damage, "урона.")

def meetShop():
    global hp   
    global coins 
    global damage

    def buy (cost):
        global coins 
        if coins >= cost:
            coins -= cost
            printCoins ()
            return True
        print ("У тебя маловато монет!")
        return False
    
    weaponLvl = r.randint (1, 3)
    weaponDmg = r.randint (1, 5) * weaponLvl
    weapon = ["AK-47", "Железный меч", "Лопата", "Цветы", "Лук", "Арбалет", "Блочный лук", "Палка-копалка"]
    weaponRarities = ["Испорченный", "Редкий", "Легендарный"]
    weaponRarity = weaponRarities [weaponLvl -1]
    weaponCost = r.randint(3, 10) * weaponLvl
    weapon = r.choice(weapon)

    oneHpCost = 5
    threeHpCost = 12

    print("На пути тебе встретился торговец!")
    printParameters()
    while True:
        chose = input("Что ты будешь делать (зайти/уйти): ").lower ()
        if chose == "зайти":
            print("1) Одна единица здоровья -", oneHpCost, "монет;") 
            print("2) Три единицы здоровья -", threeHpCost, "монет;") 
            print("3) {0} {1} - {2} монет.".format(weaponRarity, weapon, weaponCost)) 

            choice = input ("Что хочешь приобрести: ")
            if choice == "1":
                if buy(oneHpCost):
                    hp += 1
                    printHp ()
            elif choice == "2": 
                if buy(threeHpCost):
                    hp += 3
                    printHp ()
            elif choice == "3": 
                if buy(weaponCost):
                    damage = weaponDmg
                    printDamage ()
            else:
                print("Я такое не продаю.")
        elif chose == 'уйти':
            return
    

def meetMonster():
    global hp
    global coins 

    monsterLvl = r.randint(1,3) 
    monsterHp = monsterLvl
    monsterDmg = monsterLvl * 2 - 1
    monsters = ["Lilbitch", "Clop", "Madrock", "Cholop", "Freak"]
    monster = r.choice(monsters)

    print ("Ты набрёл на монстра - {0}, у него {1} уровень, {2} жизней и {3} урона ".format (monster, monsterLvl,monsterHp,monsterDmg))
    printParameters()

    while monsterHp > 0:
        choice = input ("Что будешь делать (атака/бег): ").lower()

        if choice == "атака":
            monsterHp -= damage
            if monsterHp <= 0:
                print("Ты атаковал и у монстра не осталось жизней")
                continue
            print ("Ты атаковал монстра и у него осталось", monsterHp, "жизней" )
        elif choice == "бег": 
            chance = r.randint (0, monsterLvl)
            if chance == 0:
                print ("Тебе удалось сбежать с поля боя!")
                break
            else:
                print ("Монстр оказался чересчур сильным и догнал тебя...")
        else:
            continue

        if monsterHp > 0:
            hp -= monsterDmg
            if hp <= 0:
                print("Монстр атаковал и у тебя не осталось жизней")
                break
            print ("Монстр атаковал и у тебя осталось", hp, "жизней")

    else:
        loot = r.randint (0, 2) + monsterLvl
        coins += loot
        print ("Тебе удалось одолеть монстра, за что ты получил", loot, "монет.") 
        printCoins ()   

def initGame (initHp, initCoins, initDmg) :
    global hp   
    global coins 
    global damage

    hp = initHp
    coins = initCoins
    damage = initDmg 

    print ("Ты отправился в странствие навстречу приключеиниям и опасностям. Удачи путешественник!")
    printParameters () 

def gameLoop ():
    situation = r.randint (0, 7)
    if situation == 0: 
        meetShop()
    elif situation == 1:
        meetMonster()
    else:
        if situation == 2:
            answer = input ("Блуждаю...\nХотите сохраниться? (да/нет): ")
            if (answer == "да"):
                user = input("Введите user id сохранения: ")
                save_game(user)
        else:
            input("Блуждаю...")
        
def save_game(user_id):
    global hp, coins, damage 
    data = { 'hp':hp, 'coins':coins, 'damage':damage} 
    with open(f'{user_id}_game.json', 'w') as outfile: 
        json.dump(data, outfile) 
    print('Игра успешно сохранена.')

def load_game(user_id):
    global hp, coins, damage 
    if not os.path.exists(f'{user_id}_game.json'): 
        print(f'Сохранения для пользователя {user_id} не найдены.')
    else:
        with open(f'{user_id}_game.json') as json_file: 
            data = json.load(json_file) 
        hp, coins, damage = data['hp'], data['coins'], data['damage'] 
        print(f'Игра для пользователя {user_id} успешно загружена.')

def delete_save(user_id):
    if not os.path.exists(f'{user_id}_game.json'): 
        print(f'Сохранения для пользователя {user_id} не найдены.')
    else:
        os.remove(f'{user_id}_game.json') 
        print(f'Сохранение для пользователя {user_id} успешно удалено.')
        
def write_to_csv(user_id):
    global hp, coins, damage 
    output_data = [[user_id, hp, coins, damage]]
    with open('game_data.csv', 'a', newline ='') as file:
        writer = csv.writer(file)
        writer.writerows(output_data)
    print('Данные прошедшей игровей сессии успешно записаны в CSV.')

check = ""

def menu():
    check = input("Хотите ли вы загрузить сохранение? (да/нет): ")
    if check == "да":
        user = input("Введите user id сохранения: ")
        load_game(user)
    check2 = input("Хотите ли вы удалить сохранение? (да/нет): ")
    if check2 == "да":
        user = input("Введите user id сохранения: ")
        delete_save(user)

def normalize_data():
    global hp, coins, damage 
    if hp == 0:
        hp = 1
    if coins == 0:
        coins = 1
    if damage == 0:
        damage = 1

menu()
normalize_data()
initGame (hp, coins, damage)

while True:
    gameLoop()
    
    if hp <= 0:
        if input ("Хочешь начать сначала (да/нет):").lower() == "да":
            initGame (3, 5, 1)
        else:
            break