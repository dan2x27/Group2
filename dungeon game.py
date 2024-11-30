import random
import pickle

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []

    def __str__(self):
        return f"Player: {self.name}, Health: {self.health}, Inventory: {', '.join(self.inventory) if self.inventory else 'None'}"

class Enemy:
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    def __str__(self):
        return f"Enemy: {self.name}, Health: {self.health}, Attack Power: {self.attack_power}"

class Room:
    def __init__(self, description):
        self.description = description
        self.contents = []

    def __str__(self):
        return f"Room: {self.description}, Contents: {', '.join([str(item) for item in self.contents]) if self.contents else 'Empty'}"

class DungeonCrawler:
    def __init__(self):
        self.rooms = self.generate_dungeon()
        self.player = None
        self.current_room_index = 0

    def generate_dungeon(self):
        descriptions = [
            "A dark and musty chamber",
            "A room filled with glittering treasures",
            "A damp cave with eerie noises",
            "A hallway with flickering torches",
            "A mysterious room with strange symbols on the walls"
        ]
        rooms = []
        for description in descriptions:
            room = Room(description)
            if random.random() < 0.5:
                room.contents.append(Enemy(f"Enemy-{random.randint(1, 100)}", random.randint(20, 50), random.randint(5, 15)))
            if random.random() < 0.5:
                room.contents.append(f"Treasure-{random.randint(1, 100)}")
            rooms.append(room)
        return rooms

    def start_game(self):
        print("Welcome to the Dungeon Crawler Adventure!")
        name = input("Enter your character's name: ")
        self.player = Player(name)
        print(f"Hello, {self.player.name}! Your adventure begins now!")
        self.main_menu()

    def main_menu(self):
        while self.player.health > 0:
            print("\nMain Menu")
            print("1. Move to the next room")
            print("2. View player stats")
            print("3. Save progress")
            print("4. Load progress")
            print("5. Exit game")
            choice = input("Choose an option: ")

            if choice == "1":
                self.move_room()
            elif choice == "2":
                print(self.player)
            elif choice == "3":
                self.save_progress()
            elif choice == "4":
                self.load_progress()
            elif choice == "5":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Try again.")

    def move_room(self):
        if self.current_room_index >= len(self.rooms):
            print("You have cleared all the rooms. Congratulations!")
            return

        current_room = self.rooms[self.current_room_index]
        print(f"You enter: {current_room.description}")

        for content in current_room.contents[:]:
            if isinstance(content, Enemy):
                self.fight_enemy(content)
                if self.player.health <= 0:
                    print("You have been defeated. Game over.")
                    return
            elif isinstance(content, str):
                print(f"You found a {content}!")
                self.player.inventory.append(content)
                current_room.contents.remove(content)

        print("Room cleared!")
        self.current_room_index += 1

    def fight_enemy(self, enemy):
        print(f"A wild {enemy.name} appears!")
        while enemy.health > 0 and self.player.health > 0:
            print(f"{enemy.name} attacks you for {enemy.attack_power} damage!")
            self.player.health -= enemy.attack_power
            print(f"Your health: {self.player.health}")
            if self.player.health <= 0:
                break

            attack = random.randint(10, 20)
            print(f"You attack {enemy.name} for {attack} damage!")
            enemy.health -= attack

        if enemy.health <= 0:
            print(f"You defeated {enemy.name}!")

    def save_progress(self):
        with open("savefile.pkl", "wb") as f:
            pickle.dump(self, f)
        print("Game saved!")

    @staticmethod
    def load_progress():
        try:
            with open("savefile.pkl", "rb") as f:
                game = pickle.load(f)
            print("Game loaded!")
            game.main_menu()
        except FileNotFoundError:
            print("No save file found.")

if __name__ == "__main__":
    game = DungeonCrawler()
    game.start_game()
