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
}

# 적 정의
enemies = [
    {"name": "Goblin", "HP": 30, "Damage": (5, 10)},
    {"name": "Wolf", "HP": 40, "Damage": (8, 12)},
    {"name": "Bandit", "HP": 50, "Damage": (10, 15)},
]

# 이벤트 함수
def random_event():
    events = [
        "You find a small chest containing 10 gold coins.",
        "You encounter an old man who offers you a healing potion.",
        "A wild boar charges at you from the bushes!",
        "You discover a hidden path leading deeper into the forest.",
    ]
    return random.choice(events)

# 전투 시스템
def battle(enemy):
    print(f"\nA wild {enemy['name']} appears!")
    enemy_hp = enemy["HP"]
    
    while enemy_hp > 0 and player["HP"] > 0:
        action = input("Do you want to 'attack' or 'run'? ").lower()
        if action == "attack":
            damage = random.randint(10, 20)
            enemy_hp -= damage
            print(f"You deal {damage} damage to the {enemy['name']}. It has {max(0, enemy_hp)} HP left.")
            
            if enemy_hp > 0:
                enemy_damage = random.randint(*enemy["Damage"])
                player["HP"] -= enemy_damage
                print(f"The {enemy['name']} attacks you for {enemy_damage} damage. You have {player['HP']} HP left.")
        
        elif action == "run":
            print("You flee the battle!")
            return False

    if player["HP"] > 0:
        print(f"You defeated the {enemy['name']}!")
        player["Experience"] += 10
        print(f"You gain 10 experience. Total experience: {player['Experience']}")
        return True
    else:
        print("You have been defeated...")
        return False

# 게임 마스터 함수
def game_master(player_input, context):
    """
    플레이어 입력과 현재 상황을 기반으로 다음 장면 생성.
    """
    prompt = f"{context}\nPlayer: {player_input}\nGame Master:"
    response = story_generator(prompt, max_length=150, num_return_sequences=1, do_sample=True)
    return response[0]["generated_text"]

# 게임 루프
def trpg_game():
    print("=== Welcome to the Expanded TRPG Game! ===")
    print(game_intro)
    context = game_intro

    while player["HP"] > 0:
        player_input = input("\nYour action: ")
        if player_input.lower() in ["quit", "exit"]:
            print("Thanks for playing! Goodbye!")
            break
        
        # 랜덤 이벤트 발생
        if random.random() < 0.3:  # 30% 확률로 이벤트 발생
            event = random_event()
            print(f"\nEvent: {event}")
            if "boar" in event:
                battle(random.choice(enemies))
            elif "chest" in event:
                player["Gold"] += 10
                print("You gain 10 gold. Total gold:", player["Gold"])
            elif "potion" in event:
                player["HP"] += 20
                print("You gain 20 HP. Total HP:", player["HP"])
            continue

        # 게임 마스터의 응답 생성
        generated_text = game_master(player_input, context)
        context = generated_text
        gm_response = generated_text.split("Game Master:")[-1].strip()
        print(f"\nGame Master: {gm_response}")

# 게임 실행
if __name__ == "__main__":
    trpg_game()
