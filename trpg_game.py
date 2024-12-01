from transformers import pipeline
import random

# HuggingFace 모델 로드
story_generator = pipeline("text-generation", model="gpt2")

# 초기 설정
game_intro = (
    "Welcome to Eldoria, a land of mystery and adventure. "
    "You are an adventurer seeking fame and fortune. "
    "Your journey begins in a small village on the edge of a dark forest."
)

# 플레이어 상태 관리
player = {
    "HP": 100,
    "Inventory": [],
    "Gold": 50,
    "Experience": 0,
    "Companions": [],
}

# 동료 정의
companions = {
    "Mage": {"name": "Mage", "Skill": "Fireball", "Damage": (15, 25)},
    "Rogue": {"name": "Rogue", "Skill": "Backstab", "Damage": (10, 20)},
    "Archer": {"name": "Archer", "Skill": "Arrow Shot", "Damage": (12, 18)},
}

# 일반 적 정의
enemies = [
    {"name": "Goblin", "HP": 30, "Damage": (5, 10)},
    {"name": "Wolf", "HP": 40, "Damage": (8, 12)},
    {"name": "Bandit", "HP": 50, "Damage": (10, 15)},
    {"name": "Orc", "HP": 70, "Damage": (15, 25)},
    {"name": "Zombie", "HP": 60, "Damage": (10, 20)},
    {"name": "Skeleton", "HP": 35, "Damage": (12, 18)},
]

# 보스 몬스터 정의
boss = {"name": "Lich", "HP": 200, "Damage": (25, 40)}

# 랜덤 이벤트 함수
def random_event():
    events = [
        "You find a small chest containing 10 gold coins.",
        "You encounter an old man who offers you a healing potion.",
        "A wild boar charges at you from the bushes!",
        "You discover a hidden path leading deeper into the forest.",
        "You find an ancient relic glowing faintly.",
    ]
    return random.choice(events)

# 전투 시스템 구현
def battle(enemy):
    print(f"\nA wild {enemy['name']} appears with {enemy['HP']} HP!")
    while enemy["HP"] > 0 and player["HP"] > 0:
        print("\nYour options: 'attack', 'defend', 'run'")
        action = input("Choose your action: ").lower()

        if action == "attack":
            damage = random.randint(10, 20)
            enemy["HP"] -= damage
            print(f"You deal {damage} damage to the {enemy['name']}. It has {max(0, enemy['HP'])} HP left.")
            
            if enemy["HP"] > 0:
                enemy_damage = random.randint(*enemy["Damage"])
                player["HP"] = max(player["HP"] - enemy_damage, 0)
                print(f"The {enemy['name']} attacks you for {enemy_damage} damage. You have {player['HP']} HP left.")
        elif action == "defend":
            reduced_damage = random.randint(3, 8)
            player["HP"] = max(player["HP"] - reduced_damage, 0)
            print(f"You defend yourself and take only {reduced_damage} damage. Your HP: {player['HP']}")
        elif action == "run":
            print(f"You successfully escape from the {enemy['name']}!")
            return True
        else:
            print("Invalid action. The enemy attacks!")
            enemy_damage = random.randint(*enemy["Damage"])
            player["HP"] = max(player["HP"] - enemy_damage, 0)
            print(f"The {enemy['name']} attacks you for {enemy_damage} damage. You have {player['HP']} HP left.")

    return player["HP"] > 0

# 동료 모집 함수
def recruit_companion():
    available_companions = [comp for comp in companions if comp not in player["Companions"]]
    if not available_companions:
        print("\nYou have already recruited all available companions!")
        return

    print("\nYou meet potential companions:")
    for i, comp in enumerate(available_companions, 1):
        print(f"{i}. {companions[comp]['name']} - Skill: {companions[comp]['Skill']}")

    choice = input("\nChoose a companion to recruit (1-3): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(available_companions):
        chosen = available_companions[int(choice) - 1]
        player["Companions"].append(chosen)
        print(f"\n{companions[chosen]['name']} has joined your party!")
    else:
        print("\nInvalid choice. No companion recruited.")

# 보스 전투 시스템
def boss_battle():
    print(f"\nYou encounter the final boss: {boss['name']}!")
    boss_hp = boss["HP"]

    while boss_hp > 0 and player["HP"] > 0:
        print("\nYour options: 'attack', 'defend', 'run'")
        if player["Companions"]:
            print("Your companions will assist you in battle!")

        action = input("Choose your action: ").lower()
        if action == "attack":
            damage = random.randint(10, 20)
            boss_hp -= damage
            print(f"You deal {damage} damage to the {boss['name']}. It has {max(0, boss_hp)} HP left.")

            if random.random() < 0.3:  # 보스 회복 확률
                heal = random.randint(15, 30)
                boss_hp += heal
                print(f"The {boss['name']} uses dark magic to heal {heal} HP. Current HP: {boss_hp}")

            if boss_hp > 0:
                boss_damage = random.randint(*boss["Damage"])
                player["HP"] = max(player["HP"] - boss_damage, 0)
                print(f"The {boss['name']} attacks you for {boss_damage} damage. You have {player['HP']} HP left.")

            for companion in player["Companions"]:
                comp_damage = random.randint(*companions[companion]["Damage"])
                boss_hp -= comp_damage
                print(f"{companions[companion]['name']} uses {companions[companion]['Skill']} and deals {comp_damage} damage!")

        elif action == "defend":
            reduced_damage = random.randint(5, 15)
            player["HP"] = max(player["HP"] - reduced_damage, 0)
            print(f"You defend yourself and take only {reduced_damage} damage. Your HP: {player['HP']}")
        
        elif action == "run":
            print("You cannot run away from the final boss!")
        
        else:
            print("Invalid action. The boss attacks!")
            boss_damage = random.randint(*boss["Damage"])
            player["HP"] = max(player["HP"] - boss_damage, 0)
            print(f"The {boss['name']} attacks you for {boss_damage} damage. You have {player['HP']} HP left.")

    if player["HP"] <= 0:
        print("\nYou have been defeated by the Lich. The world is shrouded in darkness...")
        display_bad_ending()
        return False
    else:
        print(f"\nCongratulations! You have defeated the {boss['name']} and saved Eldoria!")
        display_happy_ending()
        return True

def display_happy_ending():
    print("""
██   ██  ██████  ██████   ██████   ██    ██      ███████ ███    ██ ██████  ██ ███    ██  ██████
██   ██ ██    ██ ██    ██ ██    ██  ██  ██       ██      ████   ██ ██   ██ ██ ████   ██ ██    ██
███████ ████████ ████████ ██████     ████        █████   ██ ██  ██ ██   ██ ██ ██ ██  ██ ██ ▄▄▄▄▄
██   ██ ██    ██ ██       ██          ██         ██      ██  ██ ██ ██   ██ ██ ██  ██ ██ ██    ██
██   ██ ██    ██ ██       ██          ██         ███████ ██   ████ ██████  ██ ██   ████  ██████ 
""")
    print("\n=== HAPPY ENDING ===")

# BAD ENDING 표시 함수
def display_bad_ending():
    print("""
███████     ██████    ███████      ███████ ███    ██ ██████  ██ ███    ██  ██████  
██    ██   ██    ██   ██    ██     ██      ████   ██ ██   ██ ██ ████   ██ ██    ██ 
███████    ████████   ██    ██     █████   ██ ██  ██ ██   ██ ██ ██ ██  ██ ██ ▄▄▄▄▄ 
██    ██  ██      ██  ██    ██     ██      ██  ██ ██ ██   ██ ██ ██  ██ ██ ██    ██ 
███████   ██      ██  ███████      ███████ ██   ████ ██████  ██ ██   ████  ██████  
""")
    print("\n=== BAD ENDING ===")
# 게임 루프
def trpg_game():
    print("=== Welcome to the Expanded TRPG Game! ===")
    print(game_intro)

    while player["HP"] > 0:
        print("\nYour choices:")
        print("1. Explore the village")
        print("2. Enter the forest")
        print("3. Recruit a companion")
        print("4. Check your status")
        print("5. Rest to regain HP")
        print("6. Search for treasure")
        print("7. Fight the final boss")

        choice = input("\nChoose an action (1-7): ").strip()
        if not choice.isdigit() or int(choice) not in range(1, 8):
            print("\nInvalid choice. Please select a valid option.")
            continue
        
        choice = int(choice)
        if choice == 1:
            print("\nYou explore the village and talk to some locals.")
        elif choice == 2:
            print("\nYou venture into the forest.")
            if random.random() < 0.5:
                event = random_event()
                print(f"\nEvent: {event}")
                if "boar" in event:
                    if not battle(random.choice(enemies)):
                        break
                elif "chest" in event:
                    player["Gold"] += 10
                    print("You gain 10 gold. Total gold:", player["Gold"])
                elif "potion" in event:
                    player["HP"] += 20
                    print("You gain 20 HP. Total HP:", player["HP"])
        elif choice == 3:
            recruit_companion()
        elif choice == 4:
            print("\nYour current status:")
            print(f"HP: {player['HP']}")
            print(f"Gold: {player['Gold']}")
            print(f"Experience: {player['Experience']}")
            print(f"Inventory: {', '.join(player['Inventory']) if player['Inventory'] else 'Empty'}")
            print(f"Companions: {', '.join(player['Companions']) if player['Companions'] else 'None'}")
        elif choice == 5:
            player["HP"] = min(player["HP"] + 30, 100)
            print("\nYou take a rest and recover 30 HP. Total HP:", player["HP"])
        elif choice == 6:
            print("\nYou search for treasure...")
            treasure = random.choice(["a rare gem", "an ancient map", "a cursed coin"])
            player["Inventory"].append(treasure)
            print(f"You found {treasure}! Your inventory: {player['Inventory']}")
        elif choice == 7:
            if boss_battle():
                break
            else:
                break

    if player["HP"] <= 0:
        print("\nGame Over. You have been defeated. Better luck next time!")

# 게임 실행
if __name__ == "__main__":
    trpg_game()
