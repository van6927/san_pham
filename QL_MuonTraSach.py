import pyodbc
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

win =Tk()
conn_str = (
    "Driver={SQL Server};"
    "Server=VÂN\DANGVAN;" 
    "Database=QLMTSTV;"
    "Trusted_Connection=yes"
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

def dangNhap():
    DangNhap = user_entry.get()
    MatKhau = Password_entry.get()
    query = f"SELECT * FROM Users WHERE Username = ? AND Password = ?"
    cursor.execute(query, (DangNhap, MatKhau))
    row = cursor.fetchone()
    if len(MatKhau) < 8:
        messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 8 ký tự.")
        return
    if row:
        messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
        open_main_window()#sau khi đăng nhập thành công thì sẽ mở cửa sổ main_window
        win.destroy()#sau khi mở cửa sổ mới thì đóng cửa sổ đăng nhập
    else:
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")

def open_main_window():
    win2 = Tk()
    win2.title("Phần mềm quản lý mượn trả sách")
    win2.config(background='#008b8b')
    win2.geometry("510x400+650+300")
    Label(win2, text='PHẦN MỀM QUẢN LÝ MƯỢN TRẢ SÁCH', fg='#ffffff', bg='#5f9ea0', font=('cambria', 16, "bold"),width=90).pack()
    QL_Sach = Button(win2, text='Quản lý thông tin sách', command=open_ql_Sach, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=30)
    QL_Sach.place(x=130, y=100)

    QL_TBD = Button(win2, text='Quản lý thẻ bạn đọc', command=open_ql_csvc_TBD, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=30)
    QL_TBD.place(x=130, y=140)

    QL_Muon = Button(win2, text='Quản lý mượn sách', command=open_ql_muontra, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=30)
    QL_Muon.place(x=130, y=180)

    QL_Tra = Button(win2, text='Quản lý trả sách', command=open_ql_tra, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=30)
    QL_Tra.place(x=130, y=220)


#Phần bắt đầu giao diện quản lý sách
def open_ql_Sach():
    def hien_thi():
        for item in tree.get_children():
            tree.delete(item)

        for item in cursor.execute("SELECT * FROM Sach"):
            if len(item) >= 6:  # Kiểm tra xem tuple 'item' có đủ 6 phần tử không
                tree.insert("", 0, text=item[0], values=(item[1], item[2], item[3], item[4], item[5]))

    def tim():
        tim_value = tim_entry.get()  # Lấy giá trị từ tim_entry

        for item in tree.get_children():
            tree.delete(item)

        query = f"SELECT * FROM Sach WHERE BookID = '{tim_value}'"
        for item in cursor.execute(query):
            if len(item) >= 6:
                tree.insert("", 0, text=item[0], values=(item[1], item[2], item[3], item[4], item[5]))

    def them():
        BookID = MS_entry.get()
        Ten = TS_entry.get()
        TacGia = TG_entry.get()
        TheLoai = TL_combobox.get()
        SoLuong = SL_entry.get()
        TinhTrang = TT_combobox.get()
        while len(BookID) != 4:
            messagebox.showerror("Lỗi", "Mã sách phải có đúng 4 ký tự")
            return

        cursor.execute(
            f"INSERT INTO Sach (BookID, Ten, TacGia, TinhTrang, SoLuong, TheLoai) VALUES ('{BookID}', '{Ten}', '{TacGia}', '{TinhTrang}'"
            f",'{SoLuong}','{TheLoai}')")
        conn.commit()
        messagebox.showinfo("Thành công", "Sách đã được thêm thành công.")
        hien_thi()

    def sua():
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            BookID = MS_entry.get()
            Ten = TS_entry.get()
            TacGia = TG_entry.get()
            TheLoai = TL_combobox.get()
            SoLuong = SL_entry.get()
            TinhTrang = TT_combobox.get()

            cursor.execute(
                f"UPDATE Sach SET BookID='{BookID}', Ten='{Ten}', TacGia='{TacGia}', TinhTrang='{TinhTrang}'"
            f", SoLuong='{SoLuong}', TheLoai='{TheLoai}'WHERE BookID='{tree.item(selected_item)['text']}'")
            messagebox.showinfo("Thành công", "Sửa thành công.")
            conn.commit()
            hien_thi()

    def xoa():
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            cursor.execute(f"DELETE FROM Sach WHERE BookID ='{tree.item(selected_item)['text']}'")
            conn.commit()
            messagebox.showinfo("Thành công", "Sách đã được xóa thành công.")
            hien_thi()
            # Clear the entries
            MS_entry.delete(0, END)
            TS_entry.delete(0, END)
            TG_entry.delete(0, END)
            SL_entry.delete(0, END)
            TL_combobox.delete(0, END)
            TT_combobox.delete(0, END)

    def on_select(event):
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            values = tree.item(selected_item)['values']

            MS_entry.delete(0, END)
            MS_entry.insert(0, tree.item(selected_item)['text'])

            TS_entry.delete(0, END)
            TS_entry.insert(0, values[0])

            TG_entry.delete(0, END)
            TG_entry.insert(0, values[1])

            TT_combobox.delete(0, END)
            TT_combobox.insert(0, values[2])

            SL_entry.delete(0, END)
            SL_entry.insert(0, values[3])

            TL_combobox.delete(0, END)
            TL_combobox.insert(0, values[4])



    winQL_Sach = Tk()
    winQL_Sach.geometry("900x550+400+200")  # đặt kích thước cửa sổ giao diện
    winQL_Sach.config(bg='#008b8b')
    winQL_Sach.title('Quản lý thông tin sách')

    Label(winQL_Sach, text='PHẦN MỀM QUẢN LÝ MƯỢN TRẢ SÁCH', fg='#ffffff', bg='#008b8b', font=('cambria', 16, "bold"),
          width=60).place(x=0, y=0)
    Label(winQL_Sach, text='Thông tin sách:', fg='#ffffff', bg='#008b8b', font=('cambria', 13, "bold")).place(x=20, y=50)
    Label(winQL_Sach, text='Mã sách:',fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=100)
    Label(winQL_Sach, text='Tên sách:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=150)
    Label(winQL_Sach, text='Tác giả:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=200)
    Label(winQL_Sach, text='Thể loại:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=379, y=100)
    Label(winQL_Sach, text='Tình trạng:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=379, y=200)
    Label(winQL_Sach, text="Nhập mã sách cần tìm:", fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=310)
    tim_entry = Entry(winQL_Sach, width=35)
    tim_entry.place(x=388, y=312, height=25)
    Label(winQL_Sach, text="Số lượng:", fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=379, y=150)

    SL_entry = Entry(winQL_Sach, width=30)
    SL_entry.place(x=499, y=151, height=25)

    MS_entry = Entry(winQL_Sach, width=30)
    MS_entry.place(x=130, y=101, height=25)

    TS_entry = Entry(winQL_Sach, width=30)
    TS_entry.place(x=130, y=151, height=25)

    TG_entry = Entry(winQL_Sach, width=30)
    TG_entry.place(x=130, y=202, height=25)

    TL_combobox = ttk.Combobox(winQL_Sach, values=["Tâm lý", "Toán Học", "Pháp Luật", "Tôn Giáo", "Tiểu Thuyết", "Thơ", "Giáo Trình", "Lịch Sử"], width=27)
    TL_combobox.place(x=499, y=101, height=25)

    TT_combobox= ttk.Combobox(winQL_Sach, values=["Còn", "Hết"], width=27)
    TT_combobox.place(x=499, y=201, height=25)



    btn1 = Button(winQL_Sach, text='Thêm', command=them, cursor="hand2", font=('cambria', 11), fg='#ffffff', bg='#5f9ea0',  width=8)
    btn1.place(x=22, y=255)
    btn2 = Button(winQL_Sach, text='Sửa', command=sua, cursor="hand2", font=('cambria', 11), fg='#ffffff', bg='#5f9ea0',width=8)
    btn2.place(x=122, y=255)
    btn3 = Button(winQL_Sach, text='Xóa', command=xoa, cursor="hand2", font=('cambria', 11), fg='#ffffff', bg='#5f9ea0', width=8)
    btn3.place(x=222, y=255)
    btn4 = Button(winQL_Sach, text='Tìm kiếm', command=tim, cursor="hand2", font=('cambria', 11), fg='#ffffff', bg='#5f9ea0', width=8)
    btn4.place(x=588, y=309)
    btn5 = Button(winQL_Sach, text='Thoát', command=open_main_window, cursor="hand2", font=('cambria', 11), fg='#ffffff', bg='#5f9ea0', width=8)
    btn5.place(x=740, y=309)
    tree = ttk.Treeview(winQL_Sach)
    tree["columns"] = ("1", "2", "3", "4", "5")
    tree.column("#0", width=150, minwidth=150)
    tree.column("1", width=150, minwidth=150)
    tree.column("2", width=150, minwidth=150)
    tree.column("3", width=150, minwidth=150)
    tree.column("4", width=150, minwidth=150)
    tree.column("5", width=150, minwidth=150)
    tree.heading("#0", text="Mã sách", anchor=W)
    tree.heading("1", text="Tên sách", anchor=W)
    tree.heading("2", text="Tác giả", anchor=W)
    tree.heading("3", text="Tình trạng", anchor=W)
    tree.heading("4", text="Số Lượng", anchor=W)
    tree.heading("5", text="Thể Loại", anchor=W)
    tree.place(x=0, y=365)
    tree.bind("<<TreeviewSelect>>", on_select)  # khi ấn vào 1 dòng trong bảng treeview sẽ tự động điền thông tin từng cột trong bảng treeview vào từng entry tương ứng
    hien_thi()


#Phần bắt đầu giao diện quản lý thẻ bạn đọc
def open_ql_csvc_TBD():
    def hien_thi():
        for item in tree.get_children():
            tree.delete(item)

        for item in cursor.execute("SELECT * FROM TBD"):
            if len(item) >= 7:  # Kiểm tra xem tuple 'item' có đủ 7 phần tử không
                tree.insert("", 0, text=item[0], values=(item[1], item[2], item[3], item[4], item[5], item[6]))

    def tim():
        tim_value = tim_entry1.get()  # Lấy giá trị từ tim_entry1

        for item in tree.get_children():
            tree.delete(item)

        query = f"SELECT * FROM TBD WHERE IDTheDoc = '{tim_value}'"
        for item in- cursor.execute(query):
            if len(item) >= 7:
                tree.insert("", 0, text=item[0], values=(item[1], item[2], item[3], item[4], item[5], item[6]))

    def them():
        IDTheDoc = MTD_entry.get()
        HoTen = HT_entry.get()
        Lop = L_entry.get()
        DiaChi = DC_entry.get()
        NgaySinh = NS_date.get()
        NgayDangKi = NDK_date.get()
        NgayHetHan = NHH_date.get()

        while len(IDTheDoc) != 4:
            messagebox.showerror("Lỗi", "Mã thẻ phải có đúng 4 ký tự")
            return
        cursor.execute(
            f"INSERT INTO TBD (IDTheDoc, HoTen, Lop, DiaChi, NgaySinh, NgayDangKi, NgayHetHanThe) VALUES ('{IDTheDoc}', '{HoTen}'"
            f", '{Lop}', '{DiaChi}', '{NgaySinh}', '{NgayDangKi}', '{NgayHetHan}')")
        conn.commit()
        messagebox.showinfo("Thành công", "Thẻ đã được thêm thành công.")
        hien_thi()

    def sua():
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            IDTheDoc = MTD_entry.get()
            HoTen = HT_entry.get()
            Lop = L_entry.get()
            DiaChi = DC_entry.get()
            NgaySinh = NS_date.get()
            NgayDangKi = NDK_date.get()
            NgayHetHan = NHH_date.get()

            cursor.execute(
                f"UPDATE TBD SET IDTheDoc='{IDTheDoc}', HoTen='{HoTen}', Lop='{Lop}', DiaChi='{DiaChi}'"
            f", NgaySinh='{NgaySinh}', NgayDangKi='{NgayDangKi}', NgayHetHanThe='{NgayHetHan}' WHERE IDTheDoc='{tree.item(selected_item)['text']}'")
            conn.commit()
            messagebox.showinfo("Thành công", "Sửa thành công.")
            hien_thi()

    def xoa():
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            cursor.execute(f"DELETE FROM TBD WHERE IDTheDoc ='{tree.item(selected_item)['text']}'")
            conn.commit()
            messagebox.showinfo("Thành công", "Thẻ đã được xóa thành công.")
            hien_thi()
            # Clear the entries
            MTD_entry.delete(0, END)
            HT_entry.delete(0, END)
            L_entry.delete(0, END)
            DC_entry.delete(0, END)
            NS_date.delete(0, END)
            NDK_date.delete(0, END)
            NHH_date.delete(0, END)


    def on_select(event):
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            values = tree.item(selected_item)['values']

            MTD_entry.delete(0, END)
            MTD_entry.insert(0, tree.item(selected_item)['text'])

            HT_entry.delete(0, END)
            HT_entry.insert(0, values[0])

            L_entry.delete(0, END)
            L_entry.insert(0, values[1])

            DC_entry.delete(0, END)
            DC_entry.insert(0, values[2])

            NS_date.delete(0, END)
            NS_date.insert(0, values[3])

            NDK_date.delete(0, END)
            NDK_date.insert(0, values[4])

            NHH_date.delete(0, END)
            NHH_date.insert(0, values[5])

    winQL_TBD = Tk()
    winQL_TBD.geometry("1050x550+400+200")  # đặt kích thước cửa sổ giao diện
    winQL_TBD.config(background='#008b8b')

    Label(winQL_TBD, text='PHẦN MỀM QUẢN LÝ MƯỢN TRẢ SÁCH', fg='#ffffff', bg='#008b8b', font=('cambria', 16, "bold"),
          width=90).pack()
    Label(winQL_TBD, text='Thông tin thẻ bạn đọc:', fg='#ffffff', bg='#008b8b', font=('cambria', 13, "bold")).place(
        x=20, y=50)
    Label(winQL_TBD, text='Mã thẻ:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=100)
    Label(winQL_TBD, text='Họ tên:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=150)
    Label(winQL_TBD, text='Ngày đăng kí:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=379, y=100)
    Label(winQL_TBD, text='Ngày hết hạn:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=379, y=150)
    Label(winQL_TBD, text='Ngày sinh:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=379, y=200)
    Label(winQL_TBD, text='Lớp:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=747, y=100)
    Label(winQL_TBD, text='Địa chỉ:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=200)
    Label(winQL_TBD, text="Tìm kiếm theo mã thẻ:", fg='#ffffff', bg='#008b8b', font=('cambria', 13, "bold")).place(x=20, y=310)

    tim_entry1 = Entry(winQL_TBD, width=35)
    tim_entry1.place(x=388, y=312, height=25)
    MTD_entry = Entry(winQL_TBD, width=30)
    HT_entry = Entry(winQL_TBD, width=30)
    L_entry = Entry(winQL_TBD, width=30)
    DC_entry = Entry(winQL_TBD, width=30)
    NS_date = DateEntry(winQL_TBD,width=30,bg="darkblue",fg="white",year=2000)
    NDK_date = DateEntry(winQL_TBD,width=30,bg="darkblue",fg="white",year=2023)
    NHH_date = DateEntry(winQL_TBD,width=30,bg="darkblue",fg="white",year=2023)

    MTD_entry.place(x=130, y=101, height=25)
    HT_entry.place(x=130, y=151, height=25)
    L_entry.place(x=849, y=101, height=25)
    DC_entry.place(x=130, y=202, height=25)
    NS_date.place(x=499, y=201, height=25)
    NDK_date.place(x=499, y=101, height=25)
    NHH_date.place(x=499, y=151, height=25)
    
    btn1 = Button(winQL_TBD, text='Thêm', command=them, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=10)
    btn1.place(x=22, y=255)
    btn2 = Button(winQL_TBD, text='Sửa', command=sua, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=10)
    btn2.place(x=122, y=255)
    btn3 = Button(winQL_TBD, text='Xóa', command=xoa, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=10)
    btn3.place(x=222, y=255)
    btn4 = Button(winQL_TBD, text='Tìm', command=tim, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=10)
    btn4.place(x=588, y=309)
    btn5 = Button(winQL_TBD, text='Thoát', command=open_main_window, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white',
                  width=10)
    btn5.place(x=940, y=309)

    tree = ttk.Treeview(winQL_TBD)
    tree["columns"] = ("1", "2", "3", "4", "5", "6")
    tree.column("#0", width=150, minwidth=150)
    tree.column("1", width=150, minwidth=150)
    tree.column("2", width=150, minwidth=150)
    tree.column("3", width=150, minwidth=150)
    tree.column("4", width=150, minwidth=150)
    tree.column("5", width=150, minwidth=150)
    tree.column("6", width=150, minwidth=150)
    tree.heading("#0", text="Mã thẻ", anchor=W)
    tree.heading("1", text="Họ tên", anchor=W)
    tree.heading("2", text="Lớp", anchor=W)
    tree.heading("3", text="Địa chỉ", anchor=W)
    tree.heading("4", text="Ngày sinh", anchor=W)
    tree.heading("5", text="Ngày đăng kí", anchor=W)
    tree.heading("6", text="Ngày hết hạn", anchor=W)
    tree.bind("<<TreeviewSelect>>", on_select)  # khi ấn vào 1 dòng trong bảng treeview sẽ tự động điền thông tin từng cột trong bảng treeview vào từng entry tương ứng
    hien_thi()
    tree.place(x=0, y=365)

#Phần bắt đầu giao diện mượn
def open_ql_muontra():
    def hien_thi():
        for item in tree.get_children():
            tree.delete(item)

        for item in cursor.execute("SELECT * FROM QLMT"):
            if len(item) >= 5:  # Kiểm tra xem tuple 'item' có đủ 5 phần tử không
                tree.insert("", 0, text=item[0], values=(item[1], item[2], item[3], item[4]))

    def them():

        MaMTS = MMTS_entry.get()
        IDTheDoc = MTD_entry.get()
        BookID = MS_entry.get()
        NgayMuon = NM_date.get()
        SoLuongMuon = SL_entry.get()
        while len(MaMTS) != 4:
            messagebox.showerror("Lỗi", "Mã phiếu phải có đúng 4 ký tự")
            return
        cursor.execute(
            f"INSERT INTO QLMT (MaMTS, IDTheDoc, BookID, NgayMuon, SoLuongMuon) VALUES ('{MaMTS}', '{IDTheDoc}', '{BookID}', '{NgayMuon}', '{SoLuongMuon}')")
        conn.commit()
        messagebox.showinfo("Thành công", "Phiếu đã được thêm thành công.")
        hien_thi()

    def sua():
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            MaMTS = MMTS_entry.get()
            IDTheDoc = MTD_entry.get()
            BookID = MS_entry.get()
            NgayMuon = NM_date.get()
            SoLuongMuon = SL_entry.get()

            cursor.execute(
                f"UPDATE QLMT SET MaMTS='{MaMTS}', IDTheDoc='{IDTheDoc}', BookID='{BookID}', NgayMuon='{NgayMuon}'"
                f", SoLuongMuon='{SoLuongMuon}' WHERE MaMTS='{tree.item(selected_item)['text']}'")
            conn.commit()
            messagebox.showinfo("Thành công", "Sửa thành công.")
            hien_thi()

    def xoa():
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            cursor.execute(f"DELETE FROM QLMT WHERE MaMTS ='{tree.item(selected_item)['text']}'")
            conn.commit()
            messagebox.showinfo("Thành công", "Phiếu đã được xóa thành công.")
            hien_thi()
            # Clear the entries
            MMTS_entry.delete(0, END)
            MTD_entry.delete(0, END)
            MS_entry.delete(0, END)
            NM_date.delete(0, END)
            SL_entry.delete(0, END)

    def on_select(event):
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            values = tree.item(selected_item)['values']

            MMTS_entry.delete(0, END)
            MMTS_entry.insert(0, tree.item(selected_item)['text'])

            MTD_entry.delete(0, END)
            MTD_entry.insert(0, values[0])

            MS_entry.delete(0, END)
            MS_entry.insert(0, values[1])

            NM_date.delete(0, END)
            NM_date.insert(0, values[2])

            SL_entry.delete(0, END)
            SL_entry.insert(0, values[3])


    winQL_Muon = Tk()
    winQL_Muon.geometry("750x550+400+200")  # đặt kích thước cửa sổ giao diện
    winQL_Muon.config(background='#008b8b')

    Label(winQL_Muon, text='PHẦN MỀM QUẢN LÝ MƯỢN TRẢ SÁCH', fg='#ffffff', bg='#008b8b', font=('cambria', 16, "bold"),
          width=90).pack()
    Label(winQL_Muon, text='Thông tin mượn sách:', fg='#ffffff', bg='#008b8b', font=('cambria', 13, "bold")).place(
        x=20, y=50)
    Label(winQL_Muon, text='Mã phiếu mượn:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=100)
    Label(winQL_Muon, text='Mã thẻ đọc:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=150)
    Label(winQL_Muon, text='Ngày mượn:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=379, y=100)
    Label(winQL_Muon, text='Số lượng mượn:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=379, y=150)
    Label(winQL_Muon, text='Mã sách:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=200)

    MMTS_entry = Entry(winQL_Muon, width=30)
    MTD_entry = Entry(winQL_Muon, width=30)
    MS_entry = Entry(winQL_Muon, width=30)
    NM_date = DateEntry(winQL_Muon,width=30,bg="darkblue",fg="white",year=2023)
    SL_entry = Entry(winQL_Muon, width=30)

    MMTS_entry.place(x=145, y=101, height=25)
    MTD_entry.place(x=145, y=151, height=25)
    MS_entry.place(x=145, y=202, height=25)
    NM_date.place(x=499, y=101, height=25)
    SL_entry.place(x=499, y=151, height=25)

    btn1 = Button(winQL_Muon, text='Thêm', command=them, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=10)
    btn1.place(x=22, y=255)
    btn2 = Button(winQL_Muon, text='Sửa', command=sua, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=10)
    btn2.place(x=122, y=255)
    btn3 = Button(winQL_Muon, text='Xóa', command=xoa, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=10)
    btn3.place(x=222, y=255)
    btn5 = Button(winQL_Muon, text='Thoát', command=open_main_window, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=10)
    btn5.place(x=640, y=309)

    tree = ttk.Treeview(winQL_Muon)
    tree["columns"] = ("1", "2", "3", "4")
    tree.column("#0", width=150, minwidth=150)
    tree.column("1", width=150, minwidth=150)
    tree.column("2", width=150, minwidth=150)
    tree.column("3", width=150, minwidth=150)
    tree.column("4", width=150, minwidth=150)
    tree.heading("#0", text="Mã phiếu mượn", anchor=W)
    tree.heading("1", text="Mã thẻ đọc", anchor=W)
    tree.heading("2", text="Mã sách", anchor=W)
    tree.heading("3", text="Ngày mượn", anchor=W)
    tree.heading("4", text="Số lượng", anchor=W)
    tree.bind("<<TreeviewSelect>>", on_select)  # khi ấn vào 1 dòng trong bảng treeview sẽ tự động điền thông tin từng cột trong bảng treeview vào từng entry tương ứng
    hien_thi()
    tree.place(x=0, y=365)
#Phần bắt đầu giao diện trả
def open_ql_tra():
    def hien_thi():
        for item in tree.get_children():
            tree.delete(item)

        for item in cursor.execute("SELECT * FROM QLMT"):
            if len(item) >= 3:  # Kiểm tra xem tuple 'item' có đủ 7 phần tử không
                tree.insert("", 0, text=item[0], values=(item[1], item[2], item[3], item[4], item[5], item[6]))

    def tim():
        tim_value = tim_entry2.get()  # Lấy giá trị từ tim_entry2

        for item in tree.get_children():
            tree.delete(item)

        query = f"SELECT * FROM QLMT WHERE MaMTS = '{tim_value}'"
        for item in cursor.execute(query):
            if len(item) >= 7:
                tree.insert("", 0, text=item[0], values=(item[1], item[2], item[3], item[4], item[5], item[6]))
    def sua():
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            NgayTra = NT_date.get()
            GhiChu = GC_entry.get()

            cursor.execute(
                f"UPDATE QLMT SET NgayTra='{NgayTra}', GhiChu='{GhiChu}' WHERE MaMTS='{tree.item(selected_item)['text']}'")
            conn.commit()
            messagebox.showinfo("Thành công", "Cập nhập thành công.")
            hien_thi()

    def xoa():
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            cursor.execute(f"DELETE FROM QLMT WHERE MaMTS ='{tree.item(selected_item)['text']}'")
            conn.commit()
            messagebox.showinfo("Thành công", "Xóa thành công.")
            hien_thi()
            # Clear the entries
            NT_date.delete(0, END)
            GC_entry.delete(0, END)

    def on_select(event):
        selected_items = tree.selection()
        if selected_items:  # Kiểm tra xem có hàng nào được chọn không
            selected_item = selected_items[0]
            values = tree.item(selected_item)['values']

            NT_date.delete(0, END)
            NT_date.insert(0, values[5])

            GC_entry.delete(0, END)
            GC_entry.insert(0, values[6])

    winQL_Tra = Tk()
    winQL_Tra.geometry("1300x550+400+200")  # đặt kích thước cửa sổ giao diện
    winQL_Tra.config(background='#008b8b')

    Label(winQL_Tra, text='PHẦN MỀM QUẢN LÝ MƯỢN TRẢ SÁCH', fg='#ffffff', bg='#008b8b', font=('cambria', 16, "bold"),
          width=90).pack()
    Label(winQL_Tra, text='Thông tin trả sách:', fg='#ffffff', bg='#008b8b', font=('cambria', 13, "bold")).place(x=20,
                                                                                                                 y=50)
    Label(winQL_Tra, text='Mã phiếu mượn:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=20, y=100)
    Label(winQL_Tra, text='Ngày trả:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=500, y=100)
    Label(winQL_Tra, text='Ghi Chú:', fg='#ffffff', bg='#008b8b', font=('cambria', 13)).place(x=900, y=100)

    MMTS_entry = Entry(winQL_Tra, width=30)
    GC_entry = Entry(winQL_Tra, width=30)
    NT_date = DateEntry(winQL_Tra, width=30, bg="darkblue", fg="white", year=2023)

    GC_entry.place(x=1000, y=101, height=25)
    NT_date.place(x=600, y=101, height=25)

    tim_entry2 = Entry(winQL_Tra, width=35)
    tim_entry2.place(x=145, y=101, height=25)

    btn2 = Button(winQL_Tra, text='Cập nhập', command=sua, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white',
                  width=10)
    btn2.place(x=122, y=309)
    btn3 = Button(winQL_Tra, text='Xóa', command=xoa, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white',
                  width=10)
    btn3.place(x=222, y=309)

    btn4 = Button(winQL_Tra, text='Tìm', command=tim, cursor="hand2", font=('cambria', 11), bg='#5f9ea0', fg='white', width=10)
    btn4.place(x=359, y=101)
    btn5 = Button(winQL_Tra, text='Thoát', command=open_main_window, cursor="hand2", font=('cambria', 11), bg='#5f9ea0',
                  fg='white', width=10)
    btn5.place(x=900, y=309)

    tree = ttk.Treeview(winQL_Tra)
    tree["columns"] = ("1", "2", "3", "4", "5", "6")
    tree.heading("#0", text="Mã phiếu mượn", anchor=W)
    tree.heading("1", text="Mã thẻ đọc", anchor=W)
    tree.heading("2", text="Mã sách", anchor=W)
    tree.heading("3", text="Ngày mượn", anchor=W)
    tree.heading("4", text="Số lượng mượn", anchor=W)
    tree.heading("5", text="Ngày trả", anchor=W)
    tree.heading("6", text="Ghi chú", anchor=W)
    tree.bind("<<TreeviewSelect>>",
              on_select)  # khi ấn vào 1 dòng trong bảng treeview sẽ tự động điền thông tin từng cột trong bảng treeview vào từng entry tương ứng
    hien_thi()
    tree.place(x=0, y=365)

#Bắt đầu giao diện đăng nhập
win.title('Đăng nhập')  # đặt tên cửa sổ
win.geometry("700x450+600+250")  # đặt kích thước cửa sổ giao diện
win.config(background='#008b8b')

tk.Label(win, text='ĐĂNG NHẬP', fg='#ffffff', bg='#008b8b', font=('cambria', 35, "bold")).place(x=230, y=50)
tk.Label(win, text='Tên đăng nhập:', fg='#ffffff', bg='#008b8b', font=('cambria', 13, "bold")).place(x=200, y=130)
user_entry = tk.Entry(win, width=50)
user_entry.place(x=200, y=160, height=35)

tk.Label(win, text='Mật khẩu:', fg='#ffffff', bg='#008b8b', font=('cambria', 13, "bold")).place(x=200, y=210)
Password_entry = tk.Entry(win, width=50, show='*')
Password_entry.place(x=200, y=240, height=35)
btn2 = tk.Button(win, text='Đăng nhập', command=dangNhap, font=('cambria', 13, "bold"), cursor="hand2", bg='#5f9ea0', fg='white', width=29)
btn2.place(x=200, y=318, height=35)

#Kết thúc giao diện đăng nhập
win.mainloop()
