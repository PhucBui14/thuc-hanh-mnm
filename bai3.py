import tkinter as tk
from tkinter import Toplevel, messagebox
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Hàm tính toán chu vi và diện tích hình 2D
def calculate_2d_shape(shape, params):
    if shape == "Hình vuông":
        side = params['side']
        perimeter = 4 * side
        area = side ** 2
    elif shape == "Hình chữ nhật":
        length = params['length']
        width = params['width']
        perimeter = 2 * (length + width)
        area = length * width
    elif shape == "Hình tròn":
        radius = params['radius']
        perimeter = 2 * np.pi * radius
        area = np.pi * radius ** 2
    elif shape == "Tam giác vuông":
        base = params['base']
        height = params['height']
        perimeter = base + height + np.sqrt(base**2 + height**2)
        area = 0.5 * base * height
    else:
        raise ValueError("Hình không hợp lệ")
    return perimeter, area

# Hàm vẽ hình 2D
def draw_2d_shape(shape, params):
    plt.figure()
    if shape == "Hình vuông":
        side = params['side']
        square = np.array([[0, 0], [0, side], [side, side], [side, 0], [0, 0]])
        plt.plot(square[:, 0], square[:, 1], label='Hình vuông')
    elif shape == "Hình chữ nhật":
        length = params['length']
        width = params['width']
        rectangle = np.array([[0, 0], [0, width], [length, width], [length, 0], [0, 0]])
        plt.plot(rectangle[:, 0], rectangle[:, 1], label='Hình chữ nhật')
    elif shape == "Hình tròn":
        radius = params['radius']
        theta = np.linspace(0, 2 * np.pi, 100)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        plt.plot(x, y, label='Hình tròn')
    elif shape == "Tam giác vuông":
        base = params['base']
        height = params['height']
        triangle = np.array([[0, 0], [base, 0], [0, height], [0, 0]])
        plt.plot(triangle[:, 0], triangle[:, 1], label='Tam giác vuông')

    plt.title(f"Vẽ {shape}", fontsize=14)
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.grid()
    plt.axis('equal')
    plt.legend()
    plt.show()

# Hàm tính toán thể tích hình 3D
def calculate_3d_shape(shape, params):
    if shape == "Hình cầu":
        radius = params['radius']
        volume = (4/3) * np.pi * radius ** 3
    elif shape == "Hình trụ":
        radius = params['radius']
        height = params['height']
        volume = np.pi * radius ** 2 * height
    elif shape == "Hình hộp chữ nhật":
        length = params['length']
        width = params['width']
        height = params['height']
        volume = length * width * height
    else:
        raise ValueError("Hình không hợp lệ")
    return volume

# Hàm vẽ hình 3D
def draw_3d_shape(shape, params):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    if shape == "Hình cầu":
        radius = params['radius']
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = radius * np.outer(np.cos(u), np.sin(v))
        y = radius * np.outer(np.sin(u), np.sin(v))
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z, color='b', alpha=0.5)

    elif shape == "Hình trụ":
        radius = params['radius']
        height = params['height']
        z = np.linspace(0, height, 100)
        theta = np.linspace(0, 2 * np.pi, 100)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x = radius * np.cos(theta_grid)
        y = radius * np.sin(theta_grid)
        ax.plot_surface(x, y, z_grid, color='r', alpha=0.5)

    elif shape == "Hình hộp chữ nhật":
        length = params['length']
        width = params['width']
        height = params['height']

        # Định nghĩa các điểm của hình hộp
        vertices = np.array([[0, 0, 0], [length, 0, 0], [length, width, 0], [0, width, 0],
                             [0, 0, height], [length, 0, height], [length, width, height], [0, width, height]])

        # Định nghĩa các mặt của hình hộp
        faces = [[vertices[j] for j in [0, 1, 2, 3]],  # Mặt dưới
                 [vertices[j] for j in [4, 5, 6, 7]],  # Mặt trên
                 [vertices[j] for j in [0, 1, 5, 4]],  # Mặt bên
                 [vertices[j] for j in [1, 2, 6, 5]],  # Mặt bên
                 [vertices[j] for j in [2, 3, 7, 6]],  # Mặt bên
                 [vertices[j] for j in [3, 0, 4, 7]]]  # Mặt bên

        # Vẽ các mặt của hình hộp
        ax.add_collection3d(Poly3DCollection(faces, facecolors='g', linewidths=1, edgecolors='r', alpha=.25))

    ax.set_title(f"Vẽ {shape}", fontsize=14)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

# Hàm xử lý khi chọn hình 2D và mở cửa sổ nhập liệu
def open_shape_input_window(shape):
    top = Toplevel()
    top.title(f"Nhập thông số cho {shape}")

    params = {}

    def validate_input(entry):
        try:
            value = float(entry.get())
            return value
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập một số hợp lệ.")
            return None

    if shape == "Hình vuông":
        tk.Label(top, text="Cạnh:", font=('Arial', 12)).pack(pady=5)
        entry_side = tk.Entry(top, font=('Arial', 12))
        entry_side.pack(pady=5)

        def calculate_and_draw():
            side = validate_input(entry_side)
            if side is not None:
                params['side'] = side
                perimeter, area = calculate_2d_shape(shape, params)
                result_label.config(text=f"Chu vi: {perimeter:.2f}, Diện tích: {area:.2f}")
                draw_2d_shape(shape, params)

    elif shape == "Hình chữ nhật":
        tk.Label(top, text="Chiều dài:", font=('Arial', 12)).pack(pady=5)
        entry_length = tk.Entry(top, font=('Arial', 12))
        entry_length.pack(pady=5)

        tk.Label(top, text="Chiều rộng:", font=('Arial', 12)).pack(pady=5)
        entry_width = tk.Entry(top, font=('Arial', 12))
        entry_width.pack(pady=5)

        def calculate_and_draw():
            length = validate_input(entry_length)
            width = validate_input(entry_width)
            if length is not None and width is not None:
                params['length'] = length
                params['width'] = width
                perimeter, area = calculate_2d_shape(shape, params)
                result_label.config(text=f"Chu vi: {perimeter:.2f}, Diện tích: {area:.2f}")
                draw_2d_shape(shape, params)

    elif shape == "Hình tròn":
        tk.Label(top, text="Bán kính:", font=('Arial', 12)).pack(pady=5)
        entry_radius = tk.Entry(top, font=('Arial', 12))
        entry_radius.pack(pady=5)

        def calculate_and_draw():
            radius = validate_input(entry_radius)
            if radius is not None:
                params['radius'] = radius
                perimeter, area = calculate_2d_shape(shape, params)
                result_label.config(text=f"Chu vi: {perimeter:.2f}, Diện tích: {area:.2f}")
                draw_2d_shape(shape, params)

    elif shape == "Tam giác vuông":
        tk.Label(top, text="Cạnh đáy:", font=('Arial', 12)).pack(pady=5)
        entry_base = tk.Entry(top, font=('Arial', 12))
        entry_base.pack(pady=5)

        tk.Label(top, text="Chiều cao:", font=('Arial', 12)).pack(pady=5)
        entry_height = tk.Entry(top, font=('Arial', 12))
        entry_height.pack(pady=5)

        def calculate_and_draw():
            base = validate_input(entry_base)
            height = validate_input(entry_height)
            if base is not None and height is not None:
                params['base'] = base
                params['height'] = height
                perimeter, area = calculate_2d_shape(shape, params)
                result_label.config(text=f"Chu vi: {perimeter:.2f}, Diện tích: {area:.2f}")
                draw_2d_shape(shape, params)

    # Nút tính toán
    btn_calculate = tk.Button(top, text="Tính toán và vẽ", command=calculate_and_draw, font=('Arial', 12))
    btn_calculate.pack(pady=10)

    result_label = tk.Label(top, text="", font=('Arial', 12))
    result_label.pack(pady=10)

# Hàm xử lý khi chọn hình 3D và mở cửa sổ nhập liệu
def open_shape_input_window_3d(shape):
    top = Toplevel()
    top.title(f"Nhập thông số cho {shape}")

    params = {}

    def validate_input(entry):
        try:
            value = float(entry.get())
            return value
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập một số hợp lệ.")
            return None

    if shape == "Hình cầu":
        tk.Label(top, text="Bán kính:", font=('Arial', 12)).pack(pady=5)
        entry_radius = tk.Entry(top, font=('Arial', 12))
        entry_radius.pack(pady=5)

        def calculate_and_draw():
            radius = validate_input(entry_radius)
            if radius is not None:
                params['radius'] = radius
                volume = calculate_3d_shape(shape, params)
                result_label.config(text=f"Thể tích: {volume:.2f}")
                draw_3d_shape(shape, params)

    elif shape == "Hình trụ":
        tk.Label(top, text="Bán kính:", font=('Arial', 12)).pack(pady=5)
        entry_radius = tk.Entry(top, font=('Arial', 12))
        entry_radius.pack(pady=5)

        tk.Label(top, text="Chiều cao:", font=('Arial', 12)).pack(pady=5)
        entry_height = tk.Entry(top, font=('Arial', 12))
        entry_height.pack(pady=5)

        def calculate_and_draw():
            radius = validate_input(entry_radius)
            height = validate_input(entry_height)
            if radius is not None and height is not None:
                params['radius'] = radius
                params['height'] = height
                volume = calculate_3d_shape(shape, params)
                result_label.config(text=f"Thể tích: {volume:.2f}")
                draw_3d_shape(shape, params)

    elif shape == "Hình hộp chữ nhật":
        tk.Label(top, text="Chiều dài:", font=('Arial', 12)).pack(pady=5)
        entry_length = tk.Entry(top, font=('Arial', 12))
        entry_length.pack(pady=5)

        tk.Label(top, text="Chiều rộng:", font=('Arial', 12)).pack(pady=5)
        entry_width = tk.Entry(top, font=('Arial', 12))
        entry_width.pack(pady=5)

        tk.Label(top, text="Chiều cao:", font=('Arial', 12)).pack(pady=5)
        entry_height = tk.Entry(top, font=('Arial', 12))
        entry_height.pack(pady=5)

        def calculate_and_draw():
            length = validate_input(entry_length)
            width = validate_input(entry_width)
            height = validate_input(entry_height)
            if length is not None and width is not None and height is not None:
                params['length'] = length
                params['width'] = width
                params['height'] = height
                volume = calculate_3d_shape(shape, params)
                result_label.config(text=f"Thể tích: {volume:.2f}")
                draw_3d_shape(shape, params)

    # Nút tính toán
    btn_calculate = tk.Button(top, text="Tính toán và vẽ", command=calculate_and_draw, font=('Arial', 12))
    btn_calculate.pack(pady=10)

    result_label = tk.Label(top, text="", font=('Arial', 12))
    result_label.pack(pady=10)

# Cửa sổ chọn loại hình 2D
def open_shape_selection_window():
    top = Toplevel()
    top.title("Chọn Loại Hình 2D")

    label_select = tk.Label(top, text="Chọn loại hình:", font=('Arial', 14))
    label_select.pack(pady=10)

    shapes = ["Hình vuông", "Hình chữ nhật", "Hình tròn", "Tam giác vuông"]

    for shape in shapes:
        btn_shape = tk.Button(top, text=shape, command=lambda s=shape: open_shape_input_window(s), font=('Arial', 12))
        btn_shape.pack(pady=5)

# Cửa sổ chọn loại hình 3D
def open_shape_selection_window_3d():
    top = Toplevel()
    top.title("Chọn Loại Hình 3D")

    label_select = tk.Label(top, text="Chọn loại hình:", font=('Arial', 14))
    label_select.pack(pady=10)

    shapes_3d = ["Hình cầu", "Hình trụ", "Hình hộp chữ nhật"]

    for shape in shapes_3d:
        btn_shape = tk.Button(top, text=shape, command=lambda s=shape: open_shape_input_window_3d(s), font=('Arial', 12))
        btn_shape.pack(pady=5)

# Cửa sổ chọn chế độ vẽ
def open_mode_selection_window():
    top = Toplevel()
    top.title("Chọn Chế Độ Vẽ Hình")

    label_select = tk.Label(top, text="Chọn chế độ vẽ hình:", font=('Arial', 14))
    label_select.pack(pady=10)

    def open_2d_selection():
        top.destroy()  # Đóng cửa sổ chọn chế độ
        open_shape_selection_window()  # Mở cửa chọn hình 2D

    def open_3d_selection():
        top.destroy()  # Đóng cửa sổ chọn chế độ
        open_shape_selection_window_3d()  # Mở cửa chọn hình 3D
    
    btn_2d = tk.Button(top, text="Vẽ Hình 2D", command=open_2d_selection, font=('Arial', 14))
    btn_2d.pack(pady=10)

    btn_3d = tk.Button(top, text="Vẽ Hình 3D", command=open_3d_selection, font=('Arial', 14))
    btn_3d.pack(pady=10)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Phần Mềm Học Tập Hình Học")
root.geometry("400x300")

# Nút mở cửa sổ chọn chế độ vẽ
btn_select_mode = tk.Button(root, text="Chọn Chế Độ Vẽ", command=open_mode_selection_window, font=('Arial', 14))
btn_select_mode.pack(pady=20)

# Chạy vòng lặp chính
root.mainloop()
