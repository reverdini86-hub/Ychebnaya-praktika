class DiseaseAdditionModule:
    def __init__(self, disease_handbook_app):
        self.app = disease_handbook_app
    def add_disease_process(self, name, description, symptoms, recommendations):
        print("=== ПРОЦЕСС ДОБАВЛЕНИЯ ЗАБОЛЕВАНИЯ ===")
        if not name or not description:
            print("✗ Ошибка: Название и описание обязательны")
            return False
        print("✓ Все обязательные поля заполнены")
        if self._validate_disease_data(name, description):
            print("✓ Данные прошли проверку")
            try:
                self.app.add_disease(name, description, symptoms, recommendations)
                print("✓ Заболевание успешно добавлено")
                return True
            except Exception as e:
                print(f"✗ Ошибка при сохранении: {e}")
                return False
        else:
            print("✗ Данные не прошли проверку")
            return False
    def _validate_disease_data(self, name, description):
        """Валидация данных заболевания (дополнительная проверка)"""
        return len(name.strip()) >= 2 and len(description.strip()) >= 10
    
    def get_addition_statistics(self):
        """Статистика процесса добавления"""
        return {
            "process_name": "Добавление заболевания",
            "steps": [
                "Проверка заполнения обязательных полей",
                "Валидация данных заболевания", 
                "Сохранение в базу данных"
            ],
            "required_fields": ["Название", "Описание"],
            "validation_rules": [
                "Название: минимум 2 символа",
                "Описание: минимум 10 символов"
            ]
        }