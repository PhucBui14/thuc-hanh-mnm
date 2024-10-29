import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk, Label, Button, Entry, messagebox, Text, Scrollbar, RIGHT, Y, X, HORIZONTAL, BOTTOM, Frame

class StudentReportApp:
    def __init__(self, master):
        self.master = master
        master.title("Student Report App")

        self.file_path = None
        self.df = None

        # Label
        self.label = Label(master, text="Chọn file CSV:")
        self.label.pack()

        # Button to select file
        self.select_file_button = Button(master, text="Chọn File", command=self.load_file)
        self.select_file_button.pack()

        # Scrollbar for text area
        self.scrollbar_y = Scrollbar(master)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)

        self.scrollbar_x = Scrollbar(master, orient=HORIZONTAL)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        # Text area to display CSV content
        self.text_area = Text(master, height=20, width=120, wrap='none', 
                              yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        self.text_area.pack()

        self.scrollbar_y.config(command=self.text_area.yview)
        self.scrollbar_x.config(command=self.text_area.xview)

        # Input fields for new data (Lớp và các loại điểm)
        self.create_input_fields()

        # Input field for class selection for plotting
        self.plot_class_label = Label(master, text="Nhập lớp để vẽ biểu đồ:")
        self.plot_class_label.pack()

        self.plot_class_entry = Entry(master)
        self.plot_class_entry.pack()

        # Button to add new data
        self.add_data_button = Button(master, text="Thêm Thông Tin Mới", command=self.add_data)
        self.add_data_button.pack()

        # Button to plot
        self.plot_button = Button(master, text="Vẽ Biểu Đồ", command=self.plot_data)
        self.plot_button.pack()

        # Button to clear data
        self.clear_button = Button(master, text="Xóa Dữ Liệu", command=self.clear_data)
        self.clear_button.pack()

    def create_input_fields(self):
        self.labels_and_entries = {}
        # Các trường thông tin khác ngoại trừ STT
        fields = ['Mã lớp', 'Số SV', 'Loại A+', 'Loại A', 'Loại B+', 'Loại B', 
                  'Loại C+', 'Loại C', 'Loại D+', 'Loại D', 'Loại F', 'L1', 'L2', 'TX1', 'TX2', 'Cuối kỳ']

        # Tạo hai Frame để chia các trường nhập liệu thành 2 hàng
        input_frame_top = Frame(self.master)
        input_frame_top.pack()

        input_frame_bottom = Frame(self.master)
        input_frame_bottom.pack()

        # Chia các trường thành 2 hàng: hàng đầu tiên và hàng thứ hai
        for i, field in enumerate(fields):
            field_frame = Frame(input_frame_top if i < len(fields) // 2 else input_frame_bottom)  # Chia thành 2 phần
            field_frame.pack(side='left', padx=5, pady=5)

            label = Label(field_frame, text=field)
            label.pack()

            entry = Entry(field_frame)
            entry.pack()

            self.labels_and_entries[field] = entry

    def load_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            try:
                self.df = pd.read_csv(self.file_path)  # Bỏ index_col=0
                messagebox.showinfo("Thông báo", "Đã tải file thành công!")
                
                # Hiển thị nội dung CSV trong text_area
                self.text_area.delete(1.0, "end")  # Xóa nội dung cũ
                self.text_area.insert("end", self.df.to_string())  # Hiển thị nội dung mới

            except pd.errors.ParserError:
                messagebox.showerror("Lỗi", "Lỗi khi phân tích cú pháp file CSV. Vui lòng kiểm tra định dạng file.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

    def add_data(self):
        if self.df is not None:
            # Thu thập dữ liệu từ các trường đầu vào
            new_data = {}
            for field, entry in self.labels_and_entries.items():
                new_data[field] = entry.get()

            # Kiểm tra xem các trường quan trọng có được nhập không
            if all(new_data.values()):
                new_row = pd.DataFrame([new_data])
                
                # Thêm dữ liệu mới vào DataFrame
                self.df = pd.concat([self.df, new_row], ignore_index=True)

                # Cập nhật lại STT (Số thứ tự) cho toàn bộ dữ liệu
                self.df.insert(0, 'STT', range(1, len(self.df) + 1))

                # Ghi lại vào file CSV
                self.df.to_csv(self.file_path, index=False)
                messagebox.showinfo("Thông báo", "Thêm thông tin mới thành công!")

                # Cập nhật text_area với dữ liệu mới
                self.text_area.delete(1.0, "end")
                self.text_area.insert("end", self.df.to_string())
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin hợp lệ!")

    def plot_data(self):
        if self.df is not None:
            selected_class = self.plot_class_entry.get()  # Lấy lớp được nhập
            if selected_class in self.df['Mã lớp'].values:
                # Lọc dữ liệu của lớp được chọn
                class_data = self.df[self.df['Mã lớp'] == selected_class]

                # Các cột điểm
                diemA = class_data['Loại A'].astype(int).values
                diemBc = class_data['Loại B+'].astype(int).values
                diemC = class_data['Loại C'].astype(int).values
                diemF = class_data['Loại F'].astype(int).values

                # Vẽ biểu đồ điểm của lớp đó
                x_values = ['Loại A', 'Loại B+', 'Loại C', 'Loại F']  # Các nhãn cho biểu đồ
                y_values = [diemA[0], diemBc[0], diemC[0], diemF[0]]  # Giá trị tương ứng

                plt.bar(x_values, y_values, color=['red', 'green', 'blue', 'orange'])
                plt.xlabel('Loại điểm')
                plt.ylabel('Số lượng sinh viên')
                plt.title(f'Biểu đồ điểm của lớp {selected_class}')
                plt.show()
            else:
                messagebox.showerror("Lỗi", f"Lớp {selected_class} không tồn tại trong dữ liệu!")

        else:
            messagebox.showerror("Lỗi", "Vui lòng tải file CSV trước khi vẽ biểu đồ!")

    def clear_data(self):
        # Xóa toàn bộ dữ liệu trong DataFrame và cập nhật giao diện
        if self.df is not None:
            self.df = pd.DataFrame()  # Xóa toàn bộ dữ liệu
            self.text_area.delete(1.0, "end")  # Xóa nội dung hiển thị
            messagebox.showinfo("Thông báo", "Dữ liệu đã được xóa thành công!")

if __name__ == "__main__":
    root = Tk()
    app = StudentReportApp(root)
    root.mainloop()
 