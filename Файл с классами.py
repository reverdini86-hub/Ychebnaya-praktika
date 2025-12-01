import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class DiseaseHandbook:
    def __init__(self, root):
        self.root = root
        self.root.title("Справочник по заболеваниям. Создатель: Анастасия")
        self.root.geometry("800x600")
        self.root.configure(bg="#c0e183")
        self.current_user = None
        self.user_role = None
        self.create_database()
        self.show_auth_screen()
    
    def create_database(self):
        conn = sqlite3.connect('handbook.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT
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
        cursor.execute("SELECT COUNT(*) FROM users WHERE username='doctor'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                          ('doctor', '123', 'doctor', 'Доктор Иванов'))
        cursor.execute("SELECT COUNT(*) FROM users WHERE username='patient'")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                          ('patient', '123', 'patient', 'Пациент Петров'))
        cursor.execute("SELECT COUNT(*) FROM diseases")
        if cursor.fetchone()[0] == 0:
            diseases = [
                ('Грипп', 'Вирусное заболевание', 'Температура, кашель, слабость', 'Покой, питье, лекарства'),
                ('Ангина', 'Воспаление миндалин', 'Боль в горле, температура', 'Антибиотики, полоскание'),
                ('Простуда', 'ОРВИ', 'Насморк, кашель', 'Отдых, витамины')
            ]
            cursor.executemany("INSERT INTO diseases (name, description, symptoms, recommendations) VALUES (?, ?, ?, ?)", diseases)
        conn.commit()
        conn.close()
    
    def show_auth_screen(self):
        self.clear_screen()
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        title_label = tk.Label(main_frame, text="Справочник заболеваний \n Создатель: Анастасия \n Группа:И-2-23-01", 
                              font=('Arial', 24, 'bold'), bg="#f1f1f1", fg='#2c3e50')
        title_label.pack(pady=20)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, pady=20)
        login_frame = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(login_frame, text='Вход')
        tk.Label(login_frame, text="Логин:", bg='#f0f0f0', font=('Arial', 11)).pack(pady=(20, 5))
        self.login_username = tk.Entry(login_frame, width=30, font=('Arial', 11))
        self.login_username.pack(pady=5)
        self.login_username.insert(0, 'doctor') 
        tk.Label(login_frame, text="Пароль:", bg='#f0f0f0', font=('Arial', 11)).pack(pady=(10, 5))
        self.login_password = tk.Entry(login_frame, width=30, show='*', font=('Arial', 11))
        self.login_password.pack(pady=5)
        self.login_password.insert(0, '123')  
        login_btn = tk.Button(login_frame, text="Войти", 
                             command=self.perform_login,
                             bg="#7f34db", fg='white', font=('Arial', 11, 'bold'),
                             width=10, height=1)
        login_btn.pack(pady=20)
        quick_frame = tk.Frame(login_frame, bg='#f0f0f0')
        quick_frame.pack(pady=10)
        tk.Button(quick_frame, text="Войти как врач", 
                 command=lambda: self.quick_login('doctor', '123'),
                 bg='#2ecc71', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(quick_frame, text="Войти как пациент", 
                 command=lambda: self.quick_login('patient', '123'),
                 bg='#e74c3c', fg='white').pack(side=tk.LEFT, padx=5)
        register_frame = tk.Frame(notebook, bg='#f0f0f0')
        notebook.add(register_frame, text='Регистрация')
        fields = [
            ("Логин:", "register_username"),
            ("Пароль:", "register_password"),
            ("ФИО:", "register_fullname")
        ]  
        self.register_entries = {}
        for i, (label_text, key) in enumerate(fields):
            tk.Label(register_frame, text=label_text, bg='#f0f0f0', font=('Arial', 11)).pack(pady=(20 if i==0 else 10, 5))
            entry = tk.Entry(register_frame, width=30, font=('Arial', 11))
            entry.pack(pady=5)
            self.register_entries[key] = entry
        tk.Label(register_frame, text="Роль:", bg='#f0f0f0', font=('Arial', 11)).pack(pady=(10, 5))
        role_frame = tk.Frame(register_frame, bg='#f0f0f0')
        role_frame.pack()
        self.role_var = tk.StringVar(value="patient")
        tk.Radiobutton(role_frame, text="Врач", variable=self.role_var, 
                      value="doctor", bg='#f0f0f0').pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(role_frame, text="Пациент", variable=self.role_var, 
                      value="patient", bg='#f0f0f0').pack(side=tk.LEFT, padx=10)
        register_btn = tk.Button(register_frame, text="Зарегистрироваться", 
                                command=self.perform_register,
                                bg='#9b59b6', fg='white', font=('Arial', 11, 'bold'),
                                width=20, height=2)
        register_btn.pack(pady=20)
    
    def quick_login(self, username, password):
        self.login_username.delete(0, tk.END)
        self.login_password.delete(0, tk.END)
        self.login_username.insert(0, username)
        self.login_password.insert(0, password)
    
    def perform_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        if not username or not password:
            messagebox.showwarning("Ошибка", "Введите логин и пароль")
            return
        try:
            conn = sqlite3.connect('handbook.db')
            cursor = conn.cursor()
            cursor.execute("SELECT username, role, full_name FROM users WHERE username=? AND password=?", 
                         (username, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                self.current_user = user[0] 
                self.user_role = user[1]    
                full_name = user[2]          
                messagebox.showinfo("Успех", f"Добро пожаловать, {full_name}!")
                if self.user_role == "doctor":
                    self.show_doctor_interface()
                else: 
                    self.show_patient_interface()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {str(e)}")

    def perform_register(self):
        username = self.register_entries['register_username'].get().strip()
        password = self.register_entries['register_password'].get().strip()
        fullname = self.register_entries['register_fullname'].get().strip()
        role = self.role_var.get()
        if not username or not password:
            messagebox.showwarning("Ошибка", "Логин и пароль обязательны")
            return
        if len(username) < 3:
            messagebox.showwarning("Ошибка", "Логин должен быть не менее 3 символов")
            return
        if len(password) < 3:
            messagebox.showwarning("Ошибка", "Пароль должен быть не менее 3 символов")
            return
        try:
            conn = sqlite3.connect('handbook.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
                conn.close()
                return
            cursor.execute("INSERT INTO users (username, password, role, full_name) VALUES (?, ?, ?, ?)",
                          (username, password, role, fullname if fullname else f"Новый {role}"))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Регистрация прошла успешно! Теперь войдите в систему.")
            for entry in self.register_entries.values():
                entry.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка регистрации: {str(e)}")
    
    def show_doctor_interface(self):
        self.clear_screen()
        top_frame = tk.Frame(self.root, bg='#2ecc71', height=60)
        top_frame.pack(fill='x')
        top_frame.pack_propagate(False)
        tk.Label(top_frame, text=f"Врач: {self.current_user}", 
                font=('Arial', 14, 'bold'), bg='#2ecc71', fg='white').pack(side=tk.LEFT, padx=20)
        
        tk.Button(top_frame, text="Выйти", command=self.show_auth_screen,
                 bg='#e74c3c', fg='white').pack(side=tk.RIGHT, padx=20)
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        left_frame = tk.LabelFrame(main_frame, text="Добавить заболевание", 
                                  font=('Arial', 12, 'bold'), bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill='y', padx=(0, 10))
        fields = [
            ("Название:", "add_name"),
            ("Описание:", "add_desc"),
            ("Симптомы:", "add_symptoms"),
            ("Рекомендации:", "add_recommend")
        ]
        self.add_entries = {}
        for i, (label_text, key) in enumerate(fields):
            tk.Label(left_frame, text=label_text, bg='#f0f0f0', anchor='w').pack(pady=(10 if i==0 else 5, 0), padx=10, anchor='w')
            if key in ['add_desc', 'add_symptoms', 'add_recommend']:
                entry = tk.Text(left_frame, width=30, height=3, font=('Arial', 10))
            else:
                entry = tk.Entry(left_frame, width=30, font=('Arial', 10))
            entry.pack(padx=10, pady=(0, 10))
            self.add_entries[key] = entry
        tk.Button(left_frame, text="Добавить заболевание", 
                 command=self.add_disease,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack(pady=10, padx=10, fill='x')
        right_frame = tk.LabelFrame(main_frame, text="Список заболеваний", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        right_frame.pack(side=tk.RIGHT, fill='both', expand=True)
        columns = ("ID", "Название", "Описание")
        self.disease_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.disease_tree.heading(col, text=col)
            self.disease_tree.column(col, width=100)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.disease_tree.yview)
        self.disease_tree.configure(yscrollcommand=scrollbar.set)
        self.disease_tree.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        tk.Button(right_frame, text="Удалить выбранное", 
                 command=self.delete_disease,
                 bg='#e74c3c', fg='white').pack(pady=5)
        self.load_diseases()
    
    def show_patient_interface(self):
        self.clear_screen()
        top_frame = tk.Frame(self.root, bg='#3498db', height=60)
        top_frame.pack(fill='x')
        top_frame.pack_propagate(False)
        tk.Label(top_frame, text=f"Пациент: {self.current_user}", 
                font=('Arial', 14, 'bold'), bg='#3498db', fg='white').pack(side=tk.LEFT, padx=20)
        tk.Button(top_frame, text="Выйти", command=self.show_auth_screen,
                 bg='#e74c3c', fg='white').pack(side=tk.RIGHT, padx=20)
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        tk.Label(main_frame, text="Справочник заболеваний", 
                font=('Arial', 16, 'bold'), bg='#f0f0f0').pack(pady=(0, 20))
        columns = ("ID", "Название", "Описание", "Симптомы", "Рекомендации")
        self.disease_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=20)
        for col in columns:
            self.disease_tree.heading(col, text=col)
            self.disease_tree.column(col, width=120)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.disease_tree.yview)
        self.disease_tree.configure(yscrollcommand=scrollbar.set)
        self.disease_tree.pack(side=tk.LEFT, fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.load_diseases()
    
    def add_disease(self):
        try:
            name = self.add_entries['add_name'].get().strip() if isinstance(self.add_entries['add_name'], tk.Entry) else self.add_entries['add_name'].get("1.0", tk.END).strip()
            desc = self.add_entries['add_desc'].get("1.0", tk.END).strip()
            symptoms = self.add_entries['add_symptoms'].get("1.0", tk.END).strip()
            recommend = self.add_entries['add_recommend'].get("1.0", tk.END).strip()
            if not name or not desc:
                messagebox.showwarning("Ошибка", "Название и описание обязательны")
                return
            conn = sqlite3.connect('handbook.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO diseases (name, description, symptoms, recommendations) VALUES (?, ?, ?, ?)",
                          (name, desc, symptoms, recommend))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Заболевание добавлено")
            if isinstance(self.add_entries['add_name'], tk.Entry):
                self.add_entries['add_name'].delete(0, tk.END)
            else:
                self.add_entries['add_name'].delete("1.0", tk.END)
            for key in ['add_desc', 'add_symptoms', 'add_recommend']:
                self.add_entries[key].delete("1.0", tk.END)
            self.load_diseases()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить заболевание: {str(e)}")
    
    def delete_disease(self):
        selected = self.disease_tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите заболевание для удаления")
            return
        disease_id = self.disease_tree.item(selected[0])['values'][0]
        if not messagebox.askyesno("Подтверждение", "Удалить выбранное заболевание?"):
            return
        try:
            conn = sqlite3.connect('handbook.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM diseases WHERE id=?", (disease_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Заболевание удалено")
            self.load_diseases()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить заболевание: {str(e)}")
    
    def load_diseases(self):
        for item in self.disease_tree.get_children():
            self.disease_tree.delete(item)
        try:
            conn = sqlite3.connect('handbook.db')
            cursor = conn.cursor()
            if self.user_role == "doctor":
                cursor.execute("SELECT id, name, description FROM diseases ORDER BY name")
                for disease in cursor.fetchall():
                    self.disease_tree.insert("", tk.END, values=disease)
            else:
                cursor.execute("SELECT id, name, description, symptoms, recommendations FROM diseases ORDER BY name")
                for disease in cursor.fetchall():
                    self.disease_tree.insert("", tk.END, values=disease)
            conn.close()
        except Exception as e:
            print(f"Ошибка загрузки заболеваний: {e}")
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiseaseHandbook(root)
    root.mainloop()
