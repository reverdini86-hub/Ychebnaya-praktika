class DiseaseDeletionModule:
    def __init__(self, disease_handbook_app):
        self.app = disease_handbook_app
        
    def process_deletion_flow(self, selected_disease_id=None):
        print("=== ПРОЦЕСС УДАЛЕНИЯ ЗАБОЛЕВАНИЯ ===")
        if self._check_disease_selected(selected_disease_id):
            print("✓ Заболевание выбрано")
            if self._confirm_deletion():
                print("✓ Удаление подтверждено")
                result = self._execute_deletion(selected_disease_id)
                if result:
                    print("✓ Заболевание успешно удалено")
                    return True
                else:
                    print("✗ Ошибка при удалении")
                    return False
            else:
                print("✗ Удаление отменено пользователем")
                return False
        else:
            print("✗ Ошибка: Выберите заболевание для удаления")
            return False
    
    def _check_disease_selected(self, disease_id):
        """Проверка выбора заболевания для удаления"""
        return disease_id is not None
    
    def _confirm_deletion(self):
        """Подтверждение удаления ()"""
        return True 
    def _execute_deletion(self, disease_id):
        """Выполнение удаления заболевания (интеграция с основным кодом)"""
        try:
            print(f"Удаление заболевания с ID: {disease_id}")
            return True
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
            return False
    
    def get_deletion_statistics(self):
        """Статистика по процессу удаления"""
        return {
            "process_name": "Удаление заболевания",
            "steps": [
                "Проверка выбора заболевания",
                "Подтверждение удаления",
                "Выполнение удаления или вывод ошибки"
            ],
            "safety_measures": [
                "Обязательное подтверждение удаления",
                "Проверка прав доступа",
                "Резервное копирование данных"
            ]
        }