import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

class DiseaseHandbook:
    def __init__(self, root):
        self.root = root
        self.root.title("Справочник по заболеваниям. Создатель: Анастасия")
        self.root.configure(bg='#E6E6FA')  
        self.root.geometry("800x600")
        self.start_time = datetime.datetime.now()
        self.registration_module = UserRegistrationModule(self)
        self.management_module = DiseaseManagementModule(self) 
        self.deletion_module = DiseaseDeletionModule(self)
        self.create_database()
        self.current_user = None
        self.user_role = None
        self.show_login_screen()
        
    def get_process_report(self):
        """Генерация отчета по всем процессам согласно схеме"""
        report = {
            "registration": self.registration_module.get_registration_statistics(),
            "management": self.management_module.get_management_statistics(),
            "deletion": self.deletion_module.get_deletion_statistics(),
            "system_info": {
                "start_time": self.start_time,
                "current_user": self.current_user,
                "user_role": self.user_role
            }
        }
        return report
if __name__ == "__main__":
    root = tk.Tk()
    app = DiseaseHandbook(root)
    root.mainloop()