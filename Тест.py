def test_process_modules():
    class MockApp:
        def add_disease(self, name, description, symptoms, recommendations):
            print(f"Mock: Добавлено заболевание '{name}'")
            return True  
    mock_app = MockApp()
    print("🔐 ТЕСТИРОВАНИЕ МОДУЛЯ РЕГИСТРАЦИИ")
    reg_module = UserRegistrationModule(mock_app)
    reg_module.process_registration_flow()
    print("\n💊 ТЕСТИРОВАНИЕ МОДУЛЯ УПРАВЛЕНИЯ")
    mgmt_module = DiseaseManagementModule(mock_app)
    mgmt_module.process_disease_management_flow(
        "Тестовое заболевание", 
        "Это тестовое описание заболевания для проверки работы модуля",
        "Симптомы тестовые",
        "Рекомендации тестовые"
    )
    print("\n🗑️ ТЕСТИРОВАНИЕ МОДУЛЯ УДАЛЕНИЯ")
    del_module = DiseaseDeletionModule(mock_app)
    del_module.process_deletion_flow(selected_disease_id=1)
    print("\n📊 СТАТИСТИКА ПРОЦЕССОВ:")
    print(reg_module.get_registration_statistics())
    print(mgmt_module.get_management_statistics()) 
    print(del_module.get_deletion_statistics())
if __name__ == "__main__":
    test_process_modules()