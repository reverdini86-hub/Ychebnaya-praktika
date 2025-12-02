import json
import os

class UserManager:
    def __init__(self, test_mode=False):
        if test_mode:
            self.users_file = "test_users.json"
        else:
            self.users_file = "users.json"
        self.users = self._load_users()
        self.current_user = None
    
    def _load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._create_default_users()
        else:
            return self._create_default_users()
    
    def _create_default_users(self):
        default_users = {
            "doctor": {"password": "123", "role": "врач", "full_name": "Усова Анастасия"},
            "patient": {"password": "123", "role": "пациент", "full_name": "Петров Петр"}
        }
        self._save_users(default_users)
        return default_users
    
    def _save_users(self, users_data=None):
        if users_data is None:
            users_data = self.users
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    def register_user(self, username, password, role):
        if username in self.users:
            return False, "Пользователь с таким логином уже существует"
        if not username or not password:
            return False, "Логин и пароль обязательны"
        self.users[username] = {
            "password": password,
            "role": role,
            "full_name": f"Новый {role}"
        }
        self._save_users()
        return True, "Регистрация успешна"
    
    def login_user(self, username, password):
        if username not in self.users:
            return False, "Пользователь не найден"
        if self.users[username]["password"] != password:
            return False, "Неверный пароль"
        self.current_user = {
            "username": username,
            "role": self.users[username]["role"],
            "full_name": self.users[username]["full_name"]
        }
        return True, f"Вход успешен! Роль: {self.users[username]['role']}"
    
    def get_current_user(self):
        return self.current_user
    
def main_program():
    user_manager = UserManager()
    print("$" * 60)
    print("CИСТЕМА РЕГИСТРАЦИИ/ВХОДА")
    print("$" * 60)
    while True:
        print("\n1. Вход")
        print("2. Регистрация")
        print("3. Показать пользователей")
        print("4. Запустить тесты")
        print("5. Выход")
        choice = input("\nВыберите действие (1-5): ")
        if choice == "1":
            print("\n--- ВХОД ---")
            username = input("Логин: ")
            password = input("Пароль: ")
            success, message = user_manager.login_user(username, password)
            print(f"\nРезультат: {message}")
            if success:
                current_user = user_manager.get_current_user()
                print(f"Добро пожаловать, {current_user['full_name']}!")
        elif choice == "2":
            print("\n--- РЕГИСТРАЦИЯ ---")
            username = input("Придумайте логин: ")
            password = input("Придумайте пароль: ")
            print("\nРоли: 1) Врач, 2) Пациент")
            role_choice = input("Выберите роль (1 или 2): ")
            role = "врач" if role_choice == "1" else "пациент"
            success, message = user_manager.register_user(username, password, role)
            print(f"\nРезультат: {message}")
            if success:
                print("Регистрация завершена! Теперь вы можете войти.")
        elif choice == "3":
            print("\n--- ПОЛЬЗОВАТЕЛИ ---")
            if user_manager.users:
                for username, data in user_manager.users.items():
                    print(f"Логин: {username}, Роль: {data['role']}")
            else:
                print("Пользователей нет")
        elif choice == "4":
            run_tests()
        elif choice == "5":
            print("Выход из программы")
            break
        else:
            print("Неверный выбор, попробуйте снова")

def run_tests():
    """Запуск тестов"""
    print("\n" + "=" * 60)
    print(" ТЕСТИРОВАНИЕ")
    print("=" * 60)
    test_manager = UserManager(test_mode=True)
    tests = [
        ("Регистрация нового", test_manager.register_user("test1", "pass1", "врач")),
        ("Дубликат логина", test_manager.register_user("test1", "pass2", "пациент")),
        ("Успешный вход", test_manager.login_user("test1", "pass1")),
        ("Неверный пароль", test_manager.login_user("test1", "wrong")),
        ("Несуществующий", test_manager.login_user("ghost", "pass")),
    ]
    for test_name, (success, message) in tests:
        if success or ("уже существует" in message or "неверный" in message or "не найден" in message):
            print(f" {test_name}: {message}")
        else:
            print(f" {test_name}: {message}")
    if os.path.exists("test_users.json"):
        os.remove("test_users.json")
    print("\n Тесты завершены!")

if __name__ == "__main__":
    print("=" * 60)
    print("Программа входа или регистрации. Тестовый режим. Создатель: Анастасия")
    print("=" * 60)
    print("\nВыберите режим:")
    print("1. Запустить основную программу")
    print("2. Запустить тесты")
    mode = input("\nВведите 1 или 2: ")
    if mode == "1":
        main_program()
    elif mode == "2":
        run_tests()
    else:
        print("Запускаю основную программу")
        main_program()