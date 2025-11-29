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
        self.create_database()
        self.current_user = None
        self.user_role = None
        self.show_login_screen()

    def create_database(self):
        """Создание базы данных и таблиц"""
        conn = sqlite3.connect('disease_handbook.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT,
                passport TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diseases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                symptoms TEXT,
                recommendations TEXT
            )
        ''')
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)", 
                          ("Анастасия", "123", "doctor", "Усова Анастасия Андреевна"))
            cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)", 
                          ("patient", "123", "patient", "Петров Пётр Петрович"))
            
        cursor.execute("SELECT COUNT(*) FROM diseases")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO diseases (name, description, symptoms, recommendations) VALUES (?, ?, ?, ?)", 
                          ("Грипп. Тестовое заболевание", "Острое инфекцион заболевание дыхательных путей", "Высокая температура, головная боль", "Постельный режим, обильное питье"))
            cursor.execute("INSERT INTO diseases (name, description, symptoms, recommendations) VALUES (?, ?, ?, ?)", 
                          ("Ангина. Тестовое заболевание", "Воспаление небных миндалин", "Боль в горле, температура", "Антибиотики, полоскание горла"))
        conn.commit()
        conn.close()
    
    def show_login_screen(self):
        """Экран входа в систему"""
        self.clear_screen()
        
        login_frame = tk.Frame(self.root, bg='#E6E6FA')
        login_frame.pack(expand=True)
        
        tk.Label(login_frame, text="Справочник по заболеваниям. " \
        "\nСоздатель: Анастасия. \nГруппа: И-2-23-01", font=('Arial', 16, 'bold'), 
                bg='#E6E6FA', fg='#4B0082').pack(pady=20)

        tk.Label(login_frame, text="Логин:", bg='#E6E6FA').pack()
        username_entry = tk.Entry(login_frame, width=30)
        username_entry.pack(pady=5)
        tk.Label(login_frame, text="Пароль:", bg='#E6E6FA').pack()
        password_entry = tk.Entry(login_frame, width=30, show="*")
        password_entry.pack(pady=5)
        username_entry.insert(0, "doctor")
        password_entry.insert(0, "123")
        tk.Button(login_frame, text="Войти", command=lambda: self.login(
            username_entry.get(), password_entry.get()), 
                 bg='#9370DB', fg='white').pack(pady=10)
        
        test_frame = tk.Frame(login_frame, bg='#E6E6FA')
        test_frame.pack(pady=10)
        tk.Button(test_frame, text="Войти как врач", command=lambda: self.login("doctor", "123"),
                 bg='#32CD32', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(test_frame, text="Войти как пациент", command=lambda: self.login("patient", "123"),
                 bg='#4169E1', fg='white').pack(side=tk.LEFT, padx=5)
    def login(self, username, password):
        """Авторизация пользователя"""
        conn = sqlite3.connect('disease_handbook.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            self.current_user = user[1]  
            self.user_role = user[3]     
            if self.user_role == "doctor":
                self.show_doctor_interface()
            else:
                self.show_patient_interface()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
    
    def show_doctor_interface(self):
        """Интерфейс врача/администратора"""
        self.clear_screen()
        
        header_frame = tk.Frame(self.root, bg='#32CD32')
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(header_frame, text=f"Режим врача: {self.current_user}", 
                font=('Arial', 14, 'bold'), bg='#32CD32', fg='white').pack(pady=10)
        add_frame = tk.LabelFrame(self.root, text="Добавить новое заболевание", 
                                 bg='#E6E6FA', fg='#4B0082')
        add_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(add_frame, text="Название:", bg='#E6E6FA').grid(row=0, column=0, sticky='w', padx=5, pady=2)
        name_entry = tk.Entry(add_frame, width=40)
        name_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(add_frame, text="Описание:", bg='#E6E6FA').grid(row=1, column=0, sticky='w', padx=5, pady=2)
        desc_entry = tk.Entry(add_frame, width=40)
        desc_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(add_frame, text="Симптомы:", bg='#E6E6FA').grid(row=2, column=0, sticky='w', padx=5, pady=2)
        symptoms_entry = tk.Entry(add_frame, width=40)
        symptoms_entry.grid(row=2, column=1, padx=5, pady=2)
        tk.Label(add_frame, text="Рекомендации:", bg='#E6E6FA').grid(row=3, column=0, sticky='w', padx=5, pady=2)
        rec_entry = tk.Entry(add_frame, width=40)
        rec_entry.grid(row=3, column=1, padx=5, pady=2)
        tk.Button(add_frame, text="Добавить заболевание", 
                 command=lambda: self.add_disease(name_entry.get(), desc_entry.get(), 
                                                symptoms_entry.get(), rec_entry.get()),
                 bg='#9370DB', fg='white').grid(row=4, column=0, columnspan=2, pady=10)
        list_frame = tk.LabelFrame(self.root, text="Список заболеваний", 
                                  bg='#E6E6FA', fg='#4B0082')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        columns = ("ID", "Название", "Описание", "Симптомы", "Рекомендации")
        self.disease_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.disease_tree.heading(col, text=col)
            self.disease_tree.column(col, width=100)
        self.disease_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Button(list_frame, text="Удалить выбранное заболевание", 
                 command=self.delete_disease, bg='#FF4500', fg='white').pack(pady=5)
        tk.Button(self.root, text="Выйти", command=self.show_login_screen,
                 bg='#696969', fg='white').pack(pady=10)
        self.load_diseases()
    
    def show_patient_interface(self):
        """Интерфейс пациента"""
        self.clear_screen()
        header_frame = tk.Frame(self.root, bg='#4169E1')
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(header_frame, text=f"Режим пациента: {self.current_user}", 
                font=('Arial', 14, 'bold'), bg='#4169E1', fg='white').pack(pady=10)
        list_frame = tk.LabelFrame(self.root, text="Справочник заболеваний", 
                                  bg='#E6E6FA', fg='#4B0082')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        columns = ("ID", "Название", "Описание", "Симптомы", "Рекомендации")
        self.disease_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.disease_tree.heading(col, text=col)
            self.disease_tree.column(col, width=100)
        self.disease_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        tk.Button(self.root, text="Выйти", command=self.show_login_screen,
                 bg='#696969', fg='white').pack(pady=10)
        self.load_diseases()
    
    def add_disease(self, name, description, symptoms, recommendations):
        """Добавление нового заболевания"""
        if not name or not description:
            messagebox.showwarning("Предупреждение", "Название и описание обязательны!")
            return
        conn = sqlite3.connect('disease_handbook.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO diseases (name, description, symptoms, recommendations)
            VALUES (?, ?, ?, ?)
        ''', (name, description, symptoms, recommendations))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", "Заболевание успешно добавлено!")
        self.load_diseases()
    def delete_disease(self):
        """Удаление выбранного заболевания"""
        selected_item = self.disease_tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите заболевание для удаления!")
            return
        disease_id = self.disease_tree.item(selected_item[0])['values'][0]
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить это заболевание?"):
            conn = sqlite3.connect('disease_handbook.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM diseases WHERE id=?", (disease_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Заболевание успешно удалено!")
            self.load_diseases()
    
    def load_diseases(self):
        """Загрузка списка заболеваний"""
        for item in self.disease_tree.get_children():
            self.disease_tree.delete(item)
        conn = sqlite3.connect('disease_handbook.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM diseases")
        diseases = cursor.fetchall()
        conn.close()
        for disease in diseases:
            self.disease_tree.insert("", tk.END, values=disease)
    
    def clear_screen(self):
        """Очистка экрана"""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiseaseHandbook(root)

    root.mainloop()
