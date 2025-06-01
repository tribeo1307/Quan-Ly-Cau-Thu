import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from PIL import Image, ImageTk


JSON_FILE = 'CauThu.json'
USERS_FILE = 'users.json'


def read_data(file):
    if os.path.exists(file) and os.path.getsize(file) > 0:
        with open(file, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def write_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class PlayerManager:
    def __init__(self, root):
        self.root = root
        self.root.title('Quản Lý Cầu Thủ Manchester United')
        self.root.geometry("800x600")

        self.players = read_data(JSON_FILE)
        self.users = read_data(USERS_FILE)

        self.current_user = None
        self.login_window()

    def login_window(self):
       
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.root, padx=50, pady=50)
        login_frame.pack(expand=True)

        mu_label = tk.Label(login_frame, text='Manchester United', font=('Arial', 24, 'bold'), fg='red')
        mu_label.grid(row=0, column=0, columnspan=2, pady=(0, 30)) # Đặt ở hàng 0, phía trên các trường nhập liệu

        tk.Label(login_frame, text='Tên Đăng Nhập:', font=('Arial', 12)).grid(row=1, column=0, pady=10, sticky='w')
        self.username_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
        self.username_entry.grid(row=1, column=1, pady=10)

        tk.Label(login_frame, text='Mật Khẩu:', font=('Arial', 12)).grid(row=2, column=0, pady=10, sticky='w')
        self.password_entry = tk.Entry(login_frame, show='*', font=('Arial', 12), width=30)
        self.password_entry.grid(row=2, column=1, pady=10)

        tk.Button(login_frame, text='Đăng Nhập', command=self.login, font=('Arial', 12), bg='#4CAF50', fg='white', width=15).grid(row=3, columnspan=2, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        found_user = False
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                self.current_user = user
                found_user = True
                self.show_main_interface()
                break
            
        if not found_user:
            messagebox.showerror('Lỗi', 'Tên đăng nhập hoặc mật khẩu không đúng!')

    def show_main_interface(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()

        
        button_frame = tk.Frame(self.root, pady=10)
        button_frame.pack(fill='x')

        
        tk.Button(button_frame, text='Đăng Xuất', command=self.logout, font=('Arial', 10), bg='#FF5733', fg='white').pack(side=tk.RIGHT, padx=10)

        
        self.btn_view_all = tk.Button(button_frame, text='Xem Tất Cả Cầu Thủ', command=lambda: self.load_players(category='all'), font=('Arial', 10), bg='#007BFF', fg='white')
        self.btn_view_all.pack(side=tk.LEFT, padx=5)

        
        self.btn_forwards = tk.Button(button_frame, text='Xem Tiền Đạo', command=lambda: self.load_players(category='Tiền Đạo'), font=('Arial', 10), bg='#007BFF', fg='white')
        self.btn_forwards.pack(side=tk.LEFT, padx=5)

        self.btn_midfielders = tk.Button(button_frame, text='Xem Tiền Vệ', command=lambda: self.load_players(category='Tiền Vệ'), font=('Arial', 10), bg='#007BFF', fg='white')
        self.btn_midfielders.pack(side=tk.LEFT, padx=5)

        self.btn_defenders = tk.Button(button_frame, text='Xem Hậu Vệ', command=lambda: self.load_players(category='Hậu Vệ'), font=('Arial', 10), bg='#007BFF', fg='white')
        self.btn_defenders.pack(side=tk.LEFT, padx=5)

        self.btn_goalkeepers = tk.Button(button_frame, text='Xem Thủ Môn', command=lambda: self.load_players(category='Thủ Môn'), font=('Arial', 10), bg='#007BFF', fg='white')
        self.btn_goalkeepers.pack(side=tk.LEFT, padx=5)


        
        if self.current_user and self.current_user['role'] == 'admin':
            self.btn_create = tk.Button(button_frame, text='Thêm Cầu Thủ MU', command=self.create_player, font=('Arial', 10), bg='#28A745', fg='white')
            self.btn_create.pack(side=tk.LEFT, padx=5)

            self.btn_update = tk.Button(button_frame, text='Cập Nhật Cầu Thủ MU', command=self.update_player, font=('Arial', 10), bg='#FFC107', fg='black')
            self.btn_update.pack(side=tk.LEFT, padx=5)

            self.btn_delete = tk.Button(button_frame, text='Xóa Cầu Thủ MU', command=self.delete_player, font=('Arial', 10), bg='#DC3545', fg='white')
            self.btn_delete.pack(side=tk.LEFT, padx=5)

        
        columns = ("No", "Name", "Jersey", "Position", "Nationality", "Team")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        
        self.tree.heading("No", text="STT")
        self.tree.heading("Name", text="Tên Cầu Thủ")
        self.tree.heading("Jersey", text="Số Áo")
        self.tree.heading("Position", text="Vị Trí")
        self.tree.heading("Nationality", text="Quốc Tịch")
        self.tree.heading("Team", text="Đội Bóng")

        
        self.tree.column("No", width=50, anchor='center')
        self.tree.column("Name", width=180, anchor='w')
        self.tree.column("Jersey", width=80, anchor='center')
        self.tree.column("Position", width=120, anchor='center')
        self.tree.column("Nationality", width=120, anchor='center')
        self.tree.column("Team", width=150, anchor='center')

        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

       
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        
        self.load_players(category='all')

    def logout(self):
        self.current_user = None
        messagebox.showinfo('Thông báo', 'Bạn đã đăng xuất!')
        self.login_window()

    def load_players(self, category=None):
        
        for row in self.tree.get_children():
            self.tree.delete(row)
            
       
        position_mapping = {
            'Tiền Đạo': ['ST', 'LW', 'RW', 'SS'],
            'Tiền Vệ': ['CM', 'AM', 'DM', 'RM', 'LM'],
            'Hậu Vệ': ['CB', 'RB', 'LB'],
            'Thủ Môn': ['GK']
        }

       
        mu_players = [p for p in self.players if p.get('team') == 'Manchester United']
        
        
        if category and category != 'all':
            
            allowed_positions = position_mapping.get(category, [])
            
            mu_players = [p for p in mu_players if p.get('position', '').upper() in allowed_positions]
            
      
        for i, player in enumerate(mu_players):
            self.tree.insert("", "end", values=(
                i + 1,
                player.get('name', ''),
                player.get('jersey', ''),
                player.get('position', ''), 
                player.get('nationality', ''),
                player.get('team', '')
            ))

    def create_player(self):
        name = simpledialog.askstring('Thêm Cầu Thủ MU', 'Nhập tên cầu thủ:')
        if name is None: return

        jersey = simpledialog.askinteger('Thêm Cầu Thủ MU', 'Nhập số áo:')
        if jersey is None: return
            
       
        current_mu_players = [p for p in self.players if p.get('team') == 'Manchester United']
        if any(p['jersey'] == jersey for p in current_mu_players):
            messagebox.showerror("Lỗi", f"Số áo {jersey} đã tồn tại trong đội Manchester United. Vui lòng chọn số khác.")
            return

        
        position = simpledialog.askstring('Thêm Cầu Thủ MU', 'Nhập vị trí (ví dụ: ST, CM, CB, GK):')
        if position is None: return

        nationality = simpledialog.askstring('Thêm Cầu Thủ MU', 'Nhập quốc tịch:')
        if nationality is None: return
            
        
        team = "Manchester United"

        
        if name and jersey is not None and position and nationality:
            new_player = {
                'name': name,
                'jersey': jersey,
                'position': position.upper(), 
                'nationality': nationality,
                'team': team
            }
            self.players.append(new_player)
            write_data(JSON_FILE, self.players)
            self.load_players(category='all') 
            messagebox.showinfo('Thông báo', 'Cầu thủ đã được thêm vào Manchester United thành công!')
        else:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập đầy đủ thông tin cầu thủ.')

    def update_player(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn một cầu thủ để cập nhật.')
            return

        selected_jersey = self.tree.item(selected_item, 'values')[2]
            
        original_player_index = -1
        for i, p in enumerate(self.players):
            if p.get('jersey') == int(selected_jersey) and p.get('team') == 'Manchester United':
                original_player_index = i
                break
            
        if original_player_index == -1:
            messagebox.showerror("Lỗi", "Không tìm thấy cầu thủ gốc để cập nhật.")
            return

        player = self.players[original_player_index]

        name = simpledialog.askstring('Cập Nhật Cầu Thủ MU', 'Nhập tên mới:', initialvalue=player.get('name', ''))
        if name is None: return

        jersey = simpledialog.askinteger('Cập Nhật Cầu Thủ MU', 'Nhập số áo mới:', initialvalue=player.get('jersey', ''))
        if jersey is None: return
            
       
        for i, p in enumerate(self.players):
            if i != original_player_index and p.get('jersey') == jersey and p.get('team') == 'Manchester United':
                messagebox.showerror("Lỗi", f"Số áo {jersey} đã tồn tại trong đội Manchester United. Vui lòng chọn số khác.")
                return

        
        position = simpledialog.askstring('Cập Nhật Cầu Thủ MU', 'Nhập vị trí mới (ví dụ: ST, CM, CB, GK):', initialvalue=player.get('position', ''))
        if position is None: return

        nationality = simpledialog.askstring('Cập Nhật Cầu Thủ MU', 'Nhập quốc tịch mới:', initialvalue=player.get('nationality', ''))
        if nationality is None: return

        team = "Manchester United" 

        
        if name and jersey is not None and position and nationality:
            self.players[original_player_index] = {
                'name': name,
                'jersey': jersey,
                'position': position.upper(), 
                'nationality': nationality,
                'team': team
            }
            write_data(JSON_FILE, self.players)
            self.load_players(category='all') 
            messagebox.showinfo('Thông báo', 'Cầu thủ đã được cập nhật thành công!')
        else:
            messagebox.showwarning('Cảnh báo', 'Vui lòng nhập đầy đủ thông tin cầu thủ.')

    def delete_player(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning('Cảnh báo', 'Vui lòng chọn một cầu thủ để xóa.')
            return

        confirm = messagebox.askyesno('Xác nhận', 'Bạn có chắc chắn muốn xóa cầu thủ này khỏi Manchester United không?')
        if confirm:
            selected_jersey = self.tree.item(selected_item, 'values')[2]
                
            original_player_index = -1
            for i, p in enumerate(self.players):
                if p.get('jersey') == int(selected_jersey) and p.get('team') == 'Manchester United':
                    original_player_index = i
                    break
                
            if original_player_index == -1:
                messagebox.showerror("Lỗi", "Không tìm thấy cầu thủ gốc để xóa.")
                return

            deleted_player_name = self.players[original_player_index]['name']
            self.players.pop(original_player_index)
            write_data(JSON_FILE, self.players)
            self.load_players(category='all') 
            messagebox.showinfo('Thông báo', f'Cầu thủ "{deleted_player_name}" đã được xóa khỏi Manchester United thành công!')


if __name__ == '__main__':
    root = tk.Tk()
    app = PlayerManager(root)
    root.mainloop()
