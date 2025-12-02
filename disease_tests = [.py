import json
import os

class DiseaseManager:
    def __init__(self, test_mode=False):
        if test_mode:
            self.diseases_file = "test_diseases.json"
        else:
            self.diseases_file = "diseases.json"
        self.diseases = self._load_diseases()
    
    def _load_diseases(self):
        if os.path.exists(self.diseases_file):
            try:
                with open(self.diseases_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_diseases(self):
        with open(self.diseases_file, 'w', encoding='utf-8') as f:
            json.dump(self.diseases, f, ensure_ascii=False, indent=2)
    
    def add_disease(self, name, description, symptoms, recommendations):
        if not name or not description:
            return False, "Название и описание обязательны"
        name = name.strip()
        description = description.strip()
        if len(name) < 2:
            return False, "Название должно быть не менее 2 символов"
        for disease in self.diseases:
            if disease['name'].lower() == name.lower():
                return False, "Болезнь с таким названием уже существует"
        new_disease = {
            "name": name,
            "description": description,
            "symptoms": symptoms.strip() if symptoms else "",
            "recommendations": recommendations.strip() if recommendations else ""
        }
        self.diseases.append(new_disease)
        self._save_diseases()
        return True, "Болезнь успешно добавлена"
    
    def show_all_diseases(self):
        if not self.diseases:
            print("\nСписок болезней пуст")
            return
        print("\n=== СПИСОК БОЛЕЗНЕЙ ===")
        for i, disease in enumerate(self.diseases, 1):
            print(f"\n{i}. {disease['name']}")
            print(f"   Описание: {disease['description']}")
            if disease['symptoms']:
                print(f"   Симптомы: {disease['symptoms']}")
            if disease['recommendations']:
                print(f"   Рекомендации: {disease['recommendations']}")

def run_tests():
    """Только 2 теста: 1) успешное добавление, 2) дубликат"""
    print("\n" + "=" * 50)
    print(" ТЕСТИРОВАНИЕ (2 теста)")
    print("=" * 50)
    test_manager = DiseaseManager(test_mode=True)
    print("\n ТЕСТ 1: Успешное добавление болезни")
    success, message = test_manager.add_disease("Грипп", "Вирусное заболевание", "Температура", "Отдых")
    if success:
        print(f" УСПЕХ: {message}")
        test1 = True
    else:
        print(f" ОШИБКА: {message}")
        test1 = False
    print("\n ТЕСТ 2: Попытка добавить дубликат")
    success, message = test_manager.add_disease("Грипп", "Другое описание", "Симптомы", "Лечение")
    if not success and "уже существует" in message:
        print(f" УСПЕХ: {message}")
        test2 = True
    else:
        print(f" ОШИБКА: {message}")
        test2 = False
    print("\n" + "-" * 50)
    print(" ИТОГИ:")
    print(f"Тест 1: {' Пройден' if test1 else 'Провален'}")
    print(f"Тест 2: {' Пройден' if test2 else 'Провален'}")
    if os.path.exists("test_diseases.json"):
        os.remove("test_diseases.json")
    print("=" * 50)
    return test1 and test2

def main():
    disease_manager = DiseaseManager()
    while True:
        print("\n:=) СИСТЕМА УЧЕТА БОЛЕЗНЕЙ (=:")
        print("1. Добавить болезнь")
        print("2. Показать все болезни")
        print("3. Запустить тесты (2 теста)")
        print("4. Выход")
        choice = input("Выберите действие (1-4): ")
        if choice == "1":
            print("\n--- ДОБАВЛЕНИЕ БОЛЕЗНИ ---")
            name = input("Название: ")
            description = input("Описание: ")
            symptoms = input("Симптомы (не обязательно): ")
            recommendations = input("Рекомендации (не обязательно): ")
            success, message = disease_manager.add_disease(name, description, symptoms, recommendations)
            print(f"\nРезультат: {message}")
        elif choice == "2":
            disease_manager.show_all_diseases()
        elif choice == "3":
            run_tests()
        elif choice == "4":
            print("Выход из системы")
            break
        else:
            print("Неверный выбор")
if __name__ == "__main__":
    print("=" * 50)
    print("СИСТЕМА ДОБАВЛЕНИЯ БОЛЕЗНЕЙ")
    print("=" * 50)
    main()