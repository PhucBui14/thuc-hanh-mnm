import tkinter as tk
import numpy as np
from tkinter import messagebox

# Hàm kiểm tra chỉ cho phép nhập số (bao gồm cả số thực)
def validate_float_input(P):
    if P == "" or P == "-":  # Cho phép chuỗi trống (xóa nhập liệu) hoặc dấu trừ (âm)
        return False  # Không cho phép để trống
    try:
        float(P)  # Cố gắng chuyển đổi P sang số thực
        return True
    except ValueError:
        return False

# Hàm xử lý để tạo các ô nhập hệ số
def create_input_fields():
    global entries  # Sử dụng biến toàn cục để giữ các ô nhập liệu
    try:
        num_eqns = int(entry_num_eqns.get())  # Lấy số phương trình
        num_vars = int(entry_num_vars.get())  # Lấy số ẩn
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số phương trình và số ẩn hợp lệ.")
        return

    # Xóa các ô nhập liệu cũ
    for widget in frame_inputs.winfo_children():
        widget.destroy()

    entries = []  # Danh sách để lưu các ô nhập hệ số
    for i in range(num_eqns):
        row = []
        for j in range(num_vars + 1):  # +1 để có cột giá trị sau dấu "="
            entry = tk.Entry(frame_inputs, width=8, font=('Arial', 14), justify='center', validate="key", validatecommand=(vcmd, "%P"))
            entry.grid(row=i, column=j, padx=5, pady=5)
            row.append(entry)
        entries.append(row)

# Hàm kiểm tra nếu các ô nhập liệu để trống
def are_entries_filled():
    return all(entry.get() for row in entries for entry in row)

# Hàm giải hệ phương trình
def solve_system():
    if not are_entries_filled():  # Kiểm tra nếu có ô để trống
        messagebox.showerror("Lỗi", "Tất cả các ô nhập liệu phải được điền.")
        return

    try:
        num_eqns = int(entry_num_eqns.get())
        num_vars = int(entry_num_vars.get())

        if not entries:
            messagebox.showerror("Lỗi", "Vui lòng tạo các ô nhập hệ số trước khi giải.")
            return

        # Tạo ma trận hệ số và vector hằng số
        A = []
        B = []

        for i in range(num_eqns):
            row = []
            for j in range(num_vars):
                row.append(float(entries[i][j].get()))
            A.append(row)
            B.append(float(entries[i][num_vars].get()))

        A = np.array(A)
        B = np.array(B)

        # Kiểm tra số nghiệm
        rank_A = np.linalg.matrix_rank(A)
        augmented_matrix = np.hstack((A, B.reshape(-1, 1)))
        rank_augmented = np.linalg.matrix_rank(augmented_matrix)

        if rank_A != rank_augmented:
            messagebox.showerror("Kết quả", "Hệ phương trình vô nghiệm.")
        elif rank_A < num_vars:
            messagebox.showinfo("Kết quả", "Hệ phương trình có vô số nghiệm.")
        else:
            X = np.linalg.solve(A, B)
            result = "\n".join([f"x{i + 1} = {X[i]:.2f}" for i in range(len(X))])
            messagebox.showinfo("Kết quả", result)

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập các hệ số và giá trị hợp lệ.")
    except np.linalg.LinAlgError:
        messagebox.showerror("Lỗi", "Hệ phương trình không có nghiệm hoặc có vô số nghiệm.")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Giải Hệ Phương Trình Bằng Ma Trận")
root.geometry("600x500")  # Kích thước cửa sổ

# Đặt màu nền
root.configure(bg="#f0f0f0")

# Xác định hàm kiểm tra cho các ô nhập chỉ cho phép số
vcmd = root.register(validate_float_input)

# Nhãn và ô nhập cho số phương trình và số ẩn
label_num_eqns = tk.Label(root, text="Số phương trình:", font=('Arial', 14), bg="#f0f0f0")
label_num_eqns.grid(row=0, column=0, padx=10, pady=10, sticky='e')
entry_num_eqns = tk.Entry(root, validate="key", validatecommand=(vcmd, "%P"), font=('Arial', 14))
entry_num_eqns.grid(row=0, column=1, padx=10, pady=10)

label_num_vars = tk.Label(root, text="Số ẩn:", font=('Arial', 14), bg="#f0f0f0")
label_num_vars.grid(row=1, column=0, padx=10, pady=10, sticky='e')
entry_num_vars = tk.Entry(root, validate="key", validatecommand=(vcmd, "%P"), font=('Arial', 14))
entry_num_vars.grid(row=1, column=1, padx=10, pady=10)

# Nút tạo ô nhập hệ số
btn_create_fields = tk.Button(root, text="Tạo ô nhập hệ số", command=create_input_fields, font=('Arial', 14), bg="#4CAF50", fg="white")
btn_create_fields.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

# Khung để chứa các ô nhập hệ số
frame_inputs = tk.Frame(root, bg="#f0f0f0")
frame_inputs.grid(row=3, column=0, columnspan=2, pady=10)

# Nút giải hệ phương trình
btn_solve = tk.Button(root, text="Giải hệ phương trình", command=solve_system, font=('Arial', 14), bg="#2196F3", fg="white")
btn_solve.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

# Chạy vòng lặp chính của giao diện
root.mainloop()
