import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Hàm tính đạo hàm
def calculate_derivative(function_str, variable):
    var = sp.symbols(variable)
    function = sp.sympify(function_str)
    derivative = sp.diff(function, var)
    return derivative

# Hàm tính nguyên hàm có cận
def calculate_integral(function_str, lower_limit, upper_limit, variable):
    var = sp.symbols(variable)
    function = sp.sympify(function_str)
    integral = sp.integrate(function, (var, lower_limit, upper_limit))
    return integral

# Hàm vẽ đồ thị
def plot_function(function_str, x_range, variable):
    x = np.linspace(x_range[0], x_range[1], 100)
    var = sp.symbols(variable)
    y = [float(sp.N(sp.sympify(function_str).subs(var, val))) for val in x]
    
    plt.plot(x, y, label=function_str)
    plt.title("Đồ Thị Hàm Số", fontsize=14)
    plt.xlabel(variable, fontsize=12)
    plt.ylabel("f(" + variable + ")", fontsize=12)
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.grid()
    plt.legend()
    plt.show()

# Hàm xử lý tính đạo hàm
def on_calculate_derivative():
    function_str = entry_function.get()
    variable = variable_var.get()
    if not function_str:
        messagebox.showerror("Lỗi", "Vui lòng nhập hàm số.")
        return
    try:
        derivative = calculate_derivative(function_str, variable)
        result_label.config(text=f"Đạo hàm: {derivative}")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm xử lý tính nguyên hàm
def on_calculate_integral():
    function_str = entry_function.get()
    lower_limit = entry_lower_limit.get()
    upper_limit = entry_upper_limit.get()
    variable = variable_var.get()
    
    if not function_str or not lower_limit or not upper_limit:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin (hàm số và cận).")
        return
    
    try:
        lower_limit = float(lower_limit)
        upper_limit = float(upper_limit)
        integral = calculate_integral(function_str, lower_limit, upper_limit, variable)
        result_label.config(text=f"Nguyên hàm: {integral}")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập cận dưới và cận trên hợp lệ.")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm xử lý vẽ đồ thị
def on_plot_function():
    function_str = entry_function.get()
    variable = variable_var.get()
    if not function_str:
        messagebox.showerror("Lỗi", "Vui lòng nhập hàm số.")
        return
    try:
        plot_function(function_str, (-10, 10), variable)  # Vẽ trong khoảng -10 đến 10
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm xóa dữ liệu đã nhập
def clear_inputs():
    entry_function.delete(0, tk.END)
    entry_lower_limit.delete(0, tk.END)
    entry_upper_limit.delete(0, tk.END)
    result_label.config(text="")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng Dụng Giải Tích")
root.geometry("500x600")  # Kích thước lớn hơn

# Thiết lập màu nền
root.configure(bg="#f0f0f0")

# Nhập hàm số
label_function = tk.Label(root, text="Nhập hàm số f(x):", bg="#f0f0f0", font=('Arial', 14))
label_function.pack(pady=10)
entry_function = tk.Entry(root, width=40, font=('Arial', 14))
entry_function.pack(pady=5)

# Chọn biến
variable_var = tk.StringVar(value='x')  # Giá trị mặc định là 'x'
label_variable = tk.Label(root, text="Chọn biến:", bg="#f0f0f0", font=('Arial', 14))
label_variable.pack(pady=10)

radio_x = tk.Radiobutton(root, text="x", variable=variable_var, value='x', bg="#f0f0f0", font=('Arial', 14))
radio_y = tk.Radiobutton(root, text="y", variable=variable_var, value='y', bg="#f0f0f0", font=('Arial', 14))
radio_x.pack(pady=5)
radio_y.pack(pady=5)

# Nút tính đạo hàm
btn_derivative = tk.Button(root, text="Tính Đạo Hàm", command=on_calculate_derivative, font=('Arial', 14), bg="#4CAF50", fg="white")
btn_derivative.pack(pady=10)

# Nút tính nguyên hàm
label_lower_limit = tk.Label(root, text="Cận dưới:", bg="#f0f0f0", font=('Arial', 14))
label_lower_limit.pack(pady=5)
entry_lower_limit = tk.Entry(root, width=10, font=('Arial', 14))
entry_lower_limit.pack(pady=5)

label_upper_limit = tk.Label(root, text="Cận trên:", bg="#f0f0f0", font=('Arial', 14))
label_upper_limit.pack(pady=5)
entry_upper_limit = tk.Entry(root, width=10, font=('Arial', 14))
entry_upper_limit.pack(pady=5)

btn_integral = tk.Button(root, text="Tính Nguyên Hàm", command=on_calculate_integral, font=('Arial', 14), bg="#2196F3", fg="white")
btn_integral.pack(pady=10)

# Nút vẽ đồ thị
btn_plot = tk.Button(root, text="Vẽ Đồ Thị", command=on_plot_function, font=('Arial', 14), bg="#FF9800", fg="white")
btn_plot.pack(pady=10)

# Nút xóa dữ liệu
btn_clear = tk.Button(root, text="Xóa Dữ Liệu", command=clear_inputs, font=('Arial', 14), bg="#f44336", fg="white")
btn_clear.pack(pady=10)

# Khu vực hiển thị kết quả
result_label = tk.Label(root, text="", font=('Arial', 16), bg="#f0f0f0")
result_label.pack(pady=20)

# Chạy vòng lặp chính
root.mainloop()
