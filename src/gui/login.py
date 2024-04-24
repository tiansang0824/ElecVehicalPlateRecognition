import tkinter as tk
from tkinter import ttk

from tkinter import messagebox
import re

from src.base.Interface import Interface
from src.gui.Match import Match


class Login:
    frm = None
    label_title = None  # 标题按钮
    label_username = None  # 用户名提示标签
    label_password = None  # 密码提示标签
    entry_username = None  # 用户名输入框
    entry_password = None  # 密码输入框
    txt_username = None  # 获取输入的用户名
    txt_password = None  # 获取输入的密码
    btn_ok = None  # ok按钮
    btn_quit = None  # 退出按钮

    #####################
    admin_username: str = None

    def __init__(self, master=None):
        self.root = master
        self.root.title("管理员登录")
        self.root.geometry("400x300+150+150")
        self.root.resizable(False, False)
        self.root.attributes("-toolwindow", False)
        self.txt_username = tk.StringVar()
        self.txt_password = tk.StringVar()
        self.create_login()

    def login_ok(self):
        """
        OK 按钮的触发动作
        :return:
        """
        """ 获取输入 """
        username = self.entry_username.get()
        password = self.entry_password.get()
        print(f"test_code: username: {username}, password: {password}")
        """ 判断数据合法性 """
        if username == "" or password == "":  # 先判断空数据
            print("yes, they are None")
            messagebox.showwarning("None Input", "Please enter ur username and password!")
            return
        # 接下来判断数据是否符合用户名和密码要求
        re_username = r'^[a-zA-Z][a-zA-Z0-9]{3,16}$'  # 3-16位字符，大写或者小写字母开头，全部由字母和数字组成。
        re_password = r'^[\da-zA-Z]{6,12}$'  # 6-12位字符，可以是数字或者字母。
        match_username = re.match(re_username, username)
        match_password = re.match(re_password, password)
        if not match_username or not match_password:
            messagebox.showerror("error data", "Please check ur format.")
            return
        # 输入无误，接下来检查数据库
        interface = Interface()  # 创建接口
        existed_user = interface.interface_login(username, password)  # 判断用户是否存在
        if existed_user:
            self.admin_username = username
            self.frm.destroy()
            Match(master=self.root, admin_user = self.admin_username)
        else:
            messagebox.showerror("用户不存在", "用户不存在，检查输入数据！")

    def login_quit(self):
        """
        取消按钮的功能，直接退出程序
        :return:
        """
        messagebox.showinfo("quit", "close the window")
        self.frm.destroy()
        self.root.destroy()

    def register_admin(self):
        """
        注册用户按钮
        :return:
        """
        """ 获取输入 """
        username = self.entry_username.get()
        password = self.entry_password.get()
        print(f"test_code: username: {username}, password: {password}")
        """ 判断数据合法性 """
        if username == "" or password == "":  # 先判断空数据
            print("yes, they are None")
            messagebox.showwarning("None Input", "Please enter ur username and password!")
            return
        # 接下来判断数据是否符合用户名和密码要求
        re_username = r'^[a-zA-Z][a-zA-Z0-9]{3,16}$'  # 3-16位字符，大写或者小写字母开头，全部由字母和数字组成。
        re_password = r'^[\da-zA-Z]{6,12}$'  # 6-12位字符，可以是数字或者字母。
        match_username = re.match(re_username, username)
        match_password = re.match(re_password, password)
        if not match_username or not match_password:
            messagebox.showerror("error data", "Please check ur format.")
            return
        # 输入无误，接下来调用interface检查用户是否存在
        interface = Interface()
        admin_exists = interface.check_admin_exists(username)
        if admin_exists:
            messagebox.showinfo("用户已存在", "用户已存在，请直接登录")
        else:
            # 在这个分支里面，目标用户不存在，创建用户
            insert_ret = interface.insert_admin([username, password])
            if insert_ret:
                messagebox.showinfo("添加成功", "管理员用户添加成功")
            else:
                messagebox.showinfo("添加失败", "信息添加失败，请重试")

    def create_login(self):
        """ 创建总框架，方便卸载登录界面 """
        self.frm = tk.Frame(self.root)
        self.frm.pack()

        label_style = ttk.Style()
        label_style.configure("titleStyle.TLabel", font=("微软雅黑", 18, "bold"))
        self.label_title = ttk.Label(self.frm, text="管理员登录", style="titleStyle.TLabel")
        self.label_title.pack(pady=(20, 10))

        """ 用户名部分 """
        frm_username = ttk.Frame(self.frm)
        frm_username.pack(fill="x", padx=(80, 80), pady=(12, 12))
        label_username_style = ttk.Style()
        label_username_style.configure("TLabel", font=("微软雅黑", 12))
        self.label_username = ttk.Label(frm_username, text="用户名：", style="TLabel")
        self.label_username.pack(side="left")
        self.entry_username = ttk.Entry(frm_username, textvariable=self.txt_username)
        self.entry_username.pack(side="right")

        """ 密码部分 """
        frm_password = ttk.Frame(self.frm)
        frm_password.pack(fill="x", padx=(80, 80), pady=(12, 12))
        label_password_style = ttk.Style()
        label_password_style.configure("TLabel", font=("微软雅黑", 12))
        self.label_password = ttk.Label(frm_password, text="密  码：", style="TLabel")
        self.label_password.pack(side="left")
        self.entry_password = tk.Entry(frm_password, show="*", textvariable=self.txt_password)
        self.entry_password.pack(side="right")

        """ 按钮部分 """
        # 创建框架
        frm_btn = ttk.Frame(self.frm)
        frm_btn.pack(fill="x", padx=(80, 80), pady=10)
        # 创建按钮样式
        style_btn = ttk.Style()
        style_btn.configure("TButton", font=("微软雅黑", 10), width=8, height=1)
        # 创建按钮
        self.btn_ok = ttk.Button(frm_btn, text="确认", style="TButton", command=self.login_ok)
        self.btn_quit = ttk.Button(frm_btn, text="注册", style="TButton", command=self.register_admin)
        self.btn_quit.pack(side="right")
        self.btn_ok.pack(side="right", padx=(10, 10))
