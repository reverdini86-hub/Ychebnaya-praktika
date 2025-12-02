import json
import os

class DiseaseDeleter:
    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.diseases_file = "diseases.json" if not test_mode else "test_diseases.json"
        self.diseases = self._load_diseases()
    
    def _load_diseases(self):
        if os.path.exists(self.diseases_file):
            try:
                with open(self.diseases_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._create_default_diseases()
        else:
            return self._create_default_diseases()
    
    def _create_default_diseases(self):
        default_diseases = [
            {"name": "Грипп", "description": "Вирусное заболевание", 
             "symptoms": "Температура, кашель", "recommendations": "Покой, питье"},
            {"name": "Ангина", "description": "Воспаление миндалин", 
             "symptoms": "Боль в горле", "recommendations": "Антибиотики"},
            {"name": "Бронхит", "description": "Воспаление бронхов", 
             "symptoms": "Кашель", "recommendations": "Ингаляции"},
            {"name": "Гастрит", "description": "Воспаление желудка", 
             "symptoms": "Боль в животе", "recommendations": "Диета"},
            {"name": "Мигрень", "description": "Головная боль", 
             "symptoms": "Сильная боль", "recommendations": "Покой"}
        ]
        if not self.test_mode:
            self._save_diseases(default_diseases)
        return default_diseases
    
    def _save_diseases(self, diseases_list=None):
        if diseases_list is None:
            diseases_list = self.diseases
        with open(self.diseases_file, 'w', encoding='utf-8') as f:
            json.dump(diseases_list, f, ensure_ascii=False, indent=2)
    
    def show_diseases(self):
        if not self.diseases:
            print("\nСписок болезней пуст")
            return
        print("\n" + "=" * 50)
        print("СПИСОК БОЛЕЗНЕЙ")
        print("=" * 50)
        for i, disease in enumerate(self.diseases, 1):
            print(f"\n{i}. {disease['name']}")
            print(f"   Описание: {disease['description']}")
            print(f"   Симптомы: {disease['symptoms']}")
            print(f"   Рекомендации: {disease['recommendations']}")
    
    def delete_disease(self, number):
        if number < 1 or number > len(self.diseases):
            return False, "Ошибка: нет такой болезни"
        deleted_name = self.diseases[number-1]['name']
        self.diseases.pop(number-1)
        self._save_diseases()
        return True, f"Болезнь '{deleted_name}' удалена!"
    
    def get_disease_count(self):
        return len(self.diseases)
    
def run_deleter_tests():
    print("\n" + "=" * 50)
    print(" ТЕСТИРОВАНИЕ УДАЛЕНИЯ БОЛЕЗНЕЙ (2 теста)")
    print("=" * 50)
    deleter = DiseaseDeleter(test_mode=True)
    initial_count = deleter.get_disease_count()
    print(f"Начальное количество болезней: {initial_count}")
    print("\n ТЕСТ 1: Успешное удаление болезни")
    success, message = deleter.delete_disease(1)  
    if success and "Грипп" in message and "удалена" in message:
        print(f" УСПЕХ: {message}")
        print(f"   Болезней осталось: {deleter.get_disease_count()}")
        test1 = True
    else:
        print(f" ОШИБКА: {message}")
        test1 = False
    print("\n ТЕСТ 2: Попытка удалить несуществующую болезнь")
    success, message = deleter.delete_disease(10) 
    if not success and "нет такой" in message.lower():
        print(f" УСПЕХ: {message}")
        test2 = True
    else:
        print(f" ОШИБКА: {message}")
        test2 = False
    print("\n" + "-" * 50)
    print(" РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"Тест 1 (удаление): {' Пройден' if test1 else 'Провален'}")
    print(f"Тест 2 (несуществующая): {' Пройден' if test2 else 'Провален'}")
    if os.path.exists("test_diseases.json"):
        os.remove("test_diseases.json")
    print("=" * 50)
    return test1 and test2

def main_deleter_system():
    deleter = DiseaseDeleter()
    while True:
        print("\n" + "=" * 50)
        print("  СИСТЕМА УДАЛЕНИЯ БОЛЕЗНЕЙ")
        print("=" * 50)
        print("1. Посмотреть список болезней")
        print("2. Удалить болезнь")
        print("3. Показать количество болезней")
        print("4. Запустить тесты (2 теста)")
        print("5. Выйти")
        choice = input("\nВыберите действие (1-5): ")
        if choice == "1":
            deleter.show_diseases()
        elif choice == "2":
            deleter.show_diseases()
            if deleter.get_disease_count() == 0:
                print("\nСписок болезней пуст, нечего удалять!")
                continue
            try:
                num = int(input("\nВведите номер болезни для удаления: "))
                success, message = deleter.delete_disease(num)
                print(f"\nРезультат: {message}")
                if success:
                    print(f"Осталось болезней: {deleter.get_disease_count()}")
            except ValueError:
                print("\nОшибка! Введите число")
            except Exception as e:
                print(f"\nОшибка: {e}")
        elif choice == "3":
            count = deleter.get_disease_count()
            print(f"\nВсего болезней в системе: {count}")
        elif choice == "4":
            run_deleter_tests()
        elif choice == "5":
            print("\nВыход из системы...")
            print("Создатель: Анастасия")
            break
        else:
            print("\nНеверный выбор. Пожалуйста, выберите от 1 до 5.")

if __name__ == "__main__":
    print("=" * 50)
    print("СИСТЕМА УДАЛЕНИЯ БОЛЕЗНЕЙ С ТЕСТАМИ")
    print("=" * 50)
    print("\nВыберите режим запуска:")
    print("1. Основная программа")
    print("2. Запустить только тесты")
    mode = input("\nВведите 1 или 2: ")
    if mode == "1":
        main_deleter_system()
    elif mode == "2":
        run_deleter_tests()
    else:
        print("Неверный выбор. Запускаю основную программу...")
        main_deleter_system()