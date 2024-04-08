import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename  # 用来获取用户文件路径
from PIL import ImageTk, Image  # 用来读取图片
import re
from tkinter import messagebox
from src.base.Interface import Interface


class Match:
    root = None  # 主窗口

    # 下面是左侧的组件
    left_frm = None  # 左侧内容框架
    left_title_label = None  # 左侧标题标签
    left_img_label = None  # 用于显示完整图片
    left_match_btn = None  # 一键读取车牌号
    left_details_btn = None  # 逐步读取车牌号
    # file_path = askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
    # file_path = None  # 用于保存图片路径

    # 下面是右侧组件列表
    right_frm = None  # 右侧内容框架
    right_title_label = None  # 右侧标题标签
    right_img_label = None  # 显示右侧车牌所在图片
    right_remind_label = None
    right_plate_label = None  # 显示右侧车牌识别结果
    right_query_btn = None  # 查询车主信息按钮
    right_register_btn = None  # 等级车牌信息按钮

    # 其他变量
    file_path = None  # 用于保存图片路径
    photo_image = None

    def __init__(self, master=None):
        self.root = master
        self.root.title("车牌识别系统")
        self.root.geometry("860x500+100+100")
        self.root.resizable(False, False)
        self.var_plate_number = tk.StringVar()
        self.create_gui()

    def menu_import_file(self):
        """
        导入图片并且显示到左侧初始图片框中.
        :return:
        """
        # 暂时隐藏内容
        self.root.withdraw()
        # 弹出搜索框获取图片地址
        self.file_path = askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])

        if self.file_path:
            print(f"file path: {self.file_path}")
            try:
                photo = Image.open(self.file_path)
                photo = photo.resize((300, 300))  # 先调整大小
                self.photo_image = ImageTk.PhotoImage(photo)  # 保存引用，防止被回收
                self.left_img_label.config(image=self.photo_image)
            except Exception as e:
                print(f"Error loading image: {e}")
            # 再次显示主窗口
            self.root.deiconify()
        else:
            # 如果用户取消了操作，则直接显示窗口，不进行任何图片加载操作
            self.root.deiconify()

    def menu_register_user_info(self):
        """
        登记用户信息
        :return:
        """

        def if_right_info():
            """ 用来测试数据是否正确 """
            pattern_username = r'^[a-zA-Z0-9]{3,16}$'  # 用户名：3-16位字符，其中每个字符都可以是大小写字母、数字。
            pattern_phone = r'1\d{10}'  # 电话号：以数字“1”开头，后面紧跟着10个数字的字符串。
            pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # 邮箱地址
            # 利用正则表达式检测数据内容
            # 检查用户名规范
            print(f"username:{username.get()}")
            print(f"username-result:{re.match(pattern_username, username.get())}")
            print(f"phone:{phone.get()}")
            print(f"email:{email.get()}")
            if re.match(pattern_username, username.get()) is None:
                messagebox.showwarning("用户名不规范", "请输入3-16位大小写字母或者下换线的组合作为用户名")
                return False
            # 检查电话号码规范
            if re.match(pattern_phone, phone.get()) is None:
                messagebox.showwarning("电话号码不规范", "请输入正确的11位电话号码")
                return False
            if re.match(pattern_email, email.get()) is None:
                messagebox.showwarning("邮箱格式不规范", "请输入正确的邮箱地址")
                return False

        def commit_info():
            # 先判断数据是否正确
            if not if_right_info():
                return
            # TODO: 调用DAO层，操作数据库

        """ 接下来是保存信息的变量 """
        username = tk.StringVar()
        gender = tk.StringVar()
        org = tk.StringVar()
        phone = tk.StringVar()
        email = tk.StringVar()

        top_register_user = tk.Toplevel()
        top_register_user.title("用户信息登记")
        top_register_user.geometry("400x300+100+100")
        top_register_user.resizable(False, False)
        top_register_user.transient(self.root)
        top_register_user.grab_set()  # 禁止回到主窗体操作

        """ 接下来创建信息登记表 """
        info_label_style = ttk.Style()
        info_label_style.configure("userInfo.TLabel", font=("微软雅黑", 12))
        user_name_label = ttk.Label(top_register_user, text="      用户名：", style="userInfo.TLabel")
        user_gender_label = ttk.Label(top_register_user, text="        性别：", style="userInfo.TLabel")
        user_org_label = ttk.Label(top_register_user, text="  所属组织：", style="userInfo.TLabel")
        user_phone_label = ttk.Label(top_register_user, text="电话号码:", style="userInfo.TLabel")
        user_email_label = ttk.Label(top_register_user, text="  电子邮箱：", style="userInfo.TLabel")
        # 全部grid布局
        user_name_label.grid(row=0, column=0, padx=(50, 20), pady=(20, 5))
        user_gender_label.grid(row=1, column=0, padx=(50, 20), pady=5)
        user_org_label.grid(row=2, column=0, padx=(50, 20), pady=5)
        user_phone_label.grid(row=3, column=0, padx=(50, 20), pady=5)
        user_email_label.grid(row=4, column=0, padx=(50, 20), pady=5)
        # 全部输入框
        info_entry_style = ttk.Style()
        info_entry_style.configure("userInfoEntry.TEntry")
        user_name_entry = ttk.Entry(top_register_user, textvariable=username, style="userInfoEntry.TEntry")
        user_gender_entry = ttk.Entry(top_register_user, textvariable=gender, style="userInfoEntry.TEntry")
        user_org_entry = ttk.Entry(top_register_user, textvariable=org, style="userInfoEntry.TEntry")
        user_phone_entry = ttk.Entry(top_register_user, textvariable=phone, style="userInfoEntry.TEntry")
        user_email_entry = ttk.Entry(top_register_user, textvariable=email, style="userInfoEntry.TEntry")
        # 全部grid
        user_name_entry.grid(row=0, column=1, padx=(5, 10), pady=(20, 5))
        user_gender_entry.grid(row=1, column=1, padx=(5, 10), pady=5)
        user_org_entry.grid(row=2, column=1, padx=(5, 10), pady=5)
        user_phone_entry.grid(row=3, column=1, padx=(5, 10), pady=5)
        user_email_entry.grid(row=4, column=1, padx=(5, 10), pady=5)
        # 创建测试和提交按钮
        btn_style = ttk.Style()
        btn_style.configure("userRegisterBtn.TButton", font=("微软雅黑", 10), width=10, height=2)
        test_btn = ttk.Button(top_register_user, text="测试数据合法性", command=if_right_info,
                              style="userRegisterBtn.TButton")
        submit_btn = ttk.Button(top_register_user, text="提交数据", command=commit_info,
                                style="userRegisterBtn.TButton")
        test_btn.grid(row=5, column=1, padx=5, pady=5, ipady=2, ipadx=10)
        submit_btn.grid(row=6, column=1, padx=5, pady=5, ipady=2, ipadx=10)

    def menu_register_plate_info(self):
        """
        用来登记车牌信息
        :return:
        """
        pnum = tk.StringVar()
        remark = tk.StringVar()

        top_register_plate = tk.Toplevel()
        top_register_plate.title("牌照信息登记")
        top_register_plate.geometry("400x300+100+100")
        top_register_plate.resizable(False, False)
        top_register_plate.transient(self.root)
        top_register_plate.grab_set()  # 禁止

        # 创建组件
        virtual_label = tk.Label(top_register_plate)
        virtual_label.grid(row=0, pady=(5, 0))
        label_style = ttk.Style()
        label_style.configure("plateRegisterStyle.TLabel", font=("微软雅黑", 13))
        label_plate_num = ttk.Label(top_register_plate, text="牌照号码：", style="plateRegisterStyle.TLabel")  # 标签组件
        label_plate_remark = ttk.Label(top_register_plate, text="备注信息：", style="plateRegisterStyle.TLabel")  # 标签组件
        label_plate_num.grid(row=1, column=0, sticky="news", padx=25, pady=10)
        label_plate_remark.grid(row=2, column=0, sticky="news", padx=25, pady=5)
        entry_plate_num = ttk.Entry(top_register_plate)
        text_plate_remark = tk.Text(top_register_plate, width=30, height=5)
        entry_plate_num.grid(row=1, column=1, sticky="news", padx=10, pady=10)
        text_plate_remark.grid(row=2, column=1, sticky="news", padx=10, pady=10)

        # 创建按钮
        btn_style = ttk.Style()
        # 注意，这里的样式是用户信息提交页面的按钮样式，直接拿过来用了。
        btn_check = ttk.Button(top_register_plate, text="检查信息有效性", style="btnStyle.TButton")
        btn_submit = ttk.Button(top_register_plate, text="提交信息", style="btnStyle.TButton")
        btn_check.grid(row=3, column=1, pady=10)
        btn_submit.grid(row=4, column=1)

    def menu_query_userinfo(self):
        """
        搜索用户信息界面
        :return:
        """
        """ 接下来是保存信息的变量 """
        local_uid = tk.StringVar()  # 用uid搜索用户信息
        local_username = tk.StringVar()
        local_gender = tk.StringVar()
        local_org = tk.StringVar()
        local_phone = tk.StringVar()
        local_email = tk.StringVar()
        """ 测试代码:用来测试信息展示 """
        local_username.set("username")
        local_gender.set("female")
        local_org.set("所属组织")
        local_phone.set("15703417063")
        local_email.set("zhanghaotian0824@163.com")
        """ 下面开始创建子窗口 """
        top_query_userinfo = tk.Toplevel()
        top_query_userinfo.title("用户信息搜索")
        top_query_userinfo.geometry("400x300+100+100")
        top_query_userinfo.resizable(False, False)
        top_query_userinfo.transient(self.root)
        top_query_userinfo.grab_set()  # 禁止回到主窗体操作
        """ 下面开始创建组件 """
        # 创建信息展示组件的标签部分
        query_userinfo_style = ttk.Style()
        query_userinfo_style.configure("queryUserInfoLabel.TLabel", font=("微软雅黑", 13))
        label_uname_info = ttk.Label(top_query_userinfo, text="    用户名：", style="queryUserInfoLabel.TLabel")
        label_gender_info = ttk.Label(top_query_userinfo, text="      性别：", style="queryUserInfoLabel.TLabel")
        label_org_info = ttk.Label(top_query_userinfo, text="所属组织：", style="queryUserInfoLabel.TLabel")
        label_phone_info = ttk.Label(top_query_userinfo, text="联系电话：", style="queryUserInfoLabel.TLabel")
        label_email_info = ttk.Label(top_query_userinfo, text="联系邮箱：", style="queryUserInfoLabel.TLabel")
        label_uname_info.grid(row=0, column=0, padx=(50, 5), pady=(20, 5))
        label_gender_info.grid(row=1, column=0, padx=(50, 5), pady=5)
        label_org_info.grid(row=2, column=0, padx=(50, 5), pady=5)
        label_phone_info.grid(row=3, column=0, padx=(50, 5), pady=5)
        label_email_info.grid(row=4, column=0, padx=(50, 5), pady=5)
        # 创建信息展示组件的信息部分
        query_userinfo_data_style = ttk.Style()
        query_userinfo_data_style.configure("queryUserInfoDataLabel.TLabel", font=("微软雅黑", 13),
                                            background="white", relief="groove", borderwidth=1, width=20)
        label_uname_data = ttk.Label(top_query_userinfo, textvariable=local_username,
                                     style="queryUserInfoDataLabel.TLabel")
        label_gender_data = ttk.Label(top_query_userinfo, textvariable=local_gender,
                                      style="queryUserInfoDataLabel.TLabel")
        label_org_data = ttk.Label(top_query_userinfo, textvariable=local_org, style="queryUserInfoDataLabel.TLabel")
        label_phone_data = ttk.Label(top_query_userinfo, textvariable=local_phone,
                                     style="queryUserInfoDataLabel.TLabel")
        label_email_data = ttk.Label(top_query_userinfo, textvariable=local_email,
                                     style="queryUserInfoDataLabel.TLabel")
        label_uname_data.grid(row=0, column=1, padx=5, pady=(20, 5))
        label_gender_data.grid(row=1, column=1, padx=5, pady=5)
        label_org_data.grid(row=2, column=1, padx=5, pady=5)
        label_phone_data.grid(row=3, column=1, padx=5, pady=5)
        label_email_data.grid(row=4, column=1, padx=5, pady=5)
        # 创建搜索框(搜索框放在最下面)
        label_query_info = ttk.Label(top_query_userinfo, text="输入uid", style="queryUserInfoLabel.TLabel")
        style_entry_query = ttk.Style()
        style_entry_query.configure("queryUserInfoDataEntry.TEntry")
        entry_query_userinfo = ttk.Entry(top_query_userinfo, textvariable=local_uid,
                                         style="queryUserInfoDataEntry.TEntry")
        label_query_info.grid(row=5, column=0, padx=5)
        entry_query_userinfo.grid(row=5, column=1, padx=5)
        # 创建按钮
        btn_query_userinfo = ttk.Button(top_query_userinfo, text="搜索", command="")  # TODO:完成搜索功能
        btn_query_userinfo.grid(row=6, column=1, pady=(10, 0))

    def menu_about_product(self):
        """
        显示产品信息
        :return:
        """
        # 创建子窗口
        top_about_product = tk.Toplevel()
        top_about_product.title("关于产品")
        top_about_product.geometry("400x300+100+100")
        top_about_product.resizable(False, False)
        top_about_product.transient(self.root)
        top_about_product.grab_set()  # 禁止回到主窗体操作
        # 创建组件
        win11_logo = Image.open('../product_img/win11_logo.png')
        new_width = 300
        print(f"new width = {new_width}")
        new_height = int(win11_logo.height * (new_width / win11_logo.width))
        resized_win11_logo = win11_logo.resize((new_width, new_height))
        win11_logo = ImageTk.PhotoImage(resized_win11_logo)
        label_title_logo = tk.Label(top_about_product, image=win11_logo)
        label_title_logo.image = win11_logo
        label_title_logo.pack()
        # 模拟一个分割线
        frm_dividing_line = tk.Frame(top_about_product, borderwidth=1, relief='groove', height=2)
        frm_dividing_line.pack(fill="x", padx=10, pady=10)
        # 创建描述标签
        str_info = "本产品作用于\n张浩田的“校园电动车车牌识别”毕业设计\n请勿用于无关场合。"
        label_info = tk.Label(top_about_product, text=str_info, justify='left', font=("微软雅黑", 13))
        label_info.pack(pady=(20, 0))

    def menu_query_plate(self):
        """
        检索车牌信息
        :return:
        """
        # 创建本地变量
        local_pnum = tk.StringVar()
        local_remark = tk.StringVar()
        # 创建子窗口
        top_query_plate = tk.Toplevel()
        top_query_plate.title("用户信息搜索")
        top_query_plate.geometry("400x300+100+100")
        top_query_plate.resizable(False, False)
        top_query_plate.transient(self.root)
        top_query_plate.grab_set()  # 禁止回到主窗体操作
        # 创建信息标签
        style_mark_plate = ttk.Style()
        style_mark_plate.configure("queryPlateMarkLabelStyle.TLabel", font=("微软雅黑", 13))
        label_mark_plate = ttk.Label(top_query_plate, text="牌照号码: ", style="queryPlateMarkLabelStyle.TLabel")
        label_mark_remark = ttk.Label(top_query_plate, text="数据库备注: ", style="queryPlateMarkLabelStyle.TLabel")
        label_mark_plate.grid(row=0, column=0, padx=(50, 5), pady=(20, 5))
        label_mark_remark.grid(row=1, column=0, padx=(50, 5), pady=5)
        style_show_plate = ttk.Style()
        style_show_plate.configure("queryPlateShowLabelStyle.TLabel", font=("微软雅黑", 13),
                                   background="white", relief="groove", borderwidth=1, width=20)
        label_show_plate = ttk.Label(top_query_plate, textvariable=local_pnum, style="queryPlateShowLabelStyle.TLabel")
        label_show_remark = ttk.Label(top_query_plate, textvariable=local_remark,
                                      style="queryPlateShowLabelStyle.TLabel")
        label_show_plate.grid(row=0, column=1, padx=5, pady=(20, 5))
        label_show_remark.grid(row=1, column=1, padx=5, pady=5)
        # 创建搜索按钮
        label_query_by_pnum = ttk.Label(top_query_plate, text="输入车牌号码:")
        entry_query_by_pnum = ttk.Entry(top_query_plate, textvariable=local_pnum, width=20)
        btn_query_by_pnum = ttk.Button(top_query_plate, text="搜索", command="")
        label_query_by_pnum.grid(row=2, column=0, padx=5, pady=5)
        entry_query_by_pnum.grid(row=2, column=1, padx=5, pady=5)
        btn_query_by_pnum.grid(row=3, column=1, padx=5, pady=5)

    def create_menubar(self):
        """ 创建顶部菜单栏的函数
        """
        """ 创建顶部菜单栏 """
        total_menubar = tk.Menu(self.root)
        self.root.config(menu=total_menubar)
        """ 创建“文件”菜单 """
        file_menu = tk.Menu(total_menubar, tearoff=0)  # 创建“文件”菜单
        total_menubar.add_cascade(label="文件", menu=file_menu)  # 在总菜单中添加级联菜单
        file_menu.add_command(label="导入图片", command=self.menu_import_file)  # 在级联菜单中添加子按钮
        """ 创建“登记”菜单 """
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_cascade(label="登记", menu=register_menu)
        register_menu.add_command(label="登记用户信息", command=self.menu_register_user_info)
        register_menu.add_command(label="登记车牌信息", command=self.menu_register_plate_info)
        """ 创建“检索”菜单 """
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_cascade(label="检索", menu=register_menu)
        register_menu.add_command(label="检索用户信息", command=self.menu_query_userinfo)
        register_menu.add_command(label="检索车牌信息", command=self.menu_query_plate)
        # register_menu.add_command(label="检索人车关系")
        """ 创建“修改”菜单 
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_cascade(label="修改", menu=register_menu)
        register_menu.add_command(label="修改用户信息")
        register_menu.add_command(label="修改车牌信息")
        """
        # register_menu.add_command(label="修改人车关系")
        """ 创建“删除”菜单 
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_cascade(label="删除", menu=register_menu)
        register_menu.add_command(label="删除用户信息")
        register_menu.add_command(label="删除车牌信息")
        register_menu.add_command(label="删除人车关系")
        """
        """ 创建“绑定”菜单 
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_cascade(label="绑定", menu=register_menu)
        register_menu.add_command(label="绑定人车关系")
        """
        """ 创建“绑定”菜单 """
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_command(label="关于(产品)", command=self.menu_about_product)

    def fun_identify(self):
        """
        用来调用统一接口的一键识别函数
        :return:
        """
        # 创建接口对象
        interface = Interface()
        identify_ret = interface.interface_identify(self.file_path)
        print(identify_ret)

    def create_gui(self):
        """ 创建全部gui组件 """
        """ 创建菜单组件 """
        self.create_menubar()  # 调用函数创建顶部菜单栏
        """ 创建其他组件 """
        # 创建左右框架
        side_frm_style = ttk.Style()
        # side_frm_style.configure("sideFrame.TFrame", width="50%", height="100%",
        #                          borderwidth=1, relief="groove")
        side_frm_style.configure("sideFrame.TFrame", width="50%", height="100%")
        self.left_frm = ttk.Frame(self.root, style="sideFrame.TFrame")
        self.right_frm = ttk.Frame(self.root, style="sideFrame.TFrame")
        self.left_frm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Separator(self.root, orient="vertical").pack(fill="y", side=tk.LEFT)
        self.right_frm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建左右标题标签
        title_label_style = ttk.Style()
        title_label_style.configure("titleLabel.TLabel", font=("微软雅黑", 18))
        self.left_title_label = ttk.Label(self.left_frm, text="原始图片", style="titleLabel.TLabel")
        self.right_title_label = ttk.Label(self.right_frm, text="识别结果", style="titleLabel.TLabel")
        self.left_title_label.pack(side=tk.TOP, pady=(30, 10))
        self.right_title_label.pack(side=tk.TOP, pady=(30, 10))
        # 创建左右图片显示标签
        left_shown_img = Image.open("../product_img/app_logo.jpg")  # 加载图片
        left_shown_img = ImageTk.PhotoImage(left_shown_img.resize((300, 300)))
        left_img_style = ttk.Style()
        left_img_style.configure("leftImgLabel.TLabel", width="350", height="350",
                                 borderwidth=1, relief="groove")
        self.left_img_label = ttk.Label(self.left_frm, image=left_shown_img, style="leftImgLabel.TLabel")
        self.left_img_label.image = left_shown_img
        self.left_img_label.pack(pady=(10, 0))
        # 创建右侧图片
        right_shown_img = Image.open("../product_img/app_logo.jpg")
        right_shown_img = ImageTk.PhotoImage(right_shown_img.resize((300, 150)))
        right_img_style = ttk.Style()
        right_img_style.configure("rightImgLabel.TLabel", width="300", height="150",
                                  borderwidth=1, relief="groove")
        self.right_img_label = ttk.Label(self.right_frm, image=right_shown_img, style="rightImgLabel.TLabel")
        self.right_img_label.image = right_shown_img
        self.right_img_label.pack(pady=(10, 0))
        # 创建右侧复制字符提示内容
        self.right_remind_label = tk.Label(self.right_frm, text="双击复制牌照号码", font=("微软雅黑", 12, 'italic'))
        self.right_remind_label.pack(pady=(30, 0))
        # 创建右侧车牌号码显示框(Label模拟)
        self.var_plate_number.set("M28199")
        self.right_plate_label = tk.Label(self.right_frm, textvariable=self.var_plate_number,
                                          font=("Consolas", 14), background="white", relief="groove",
                                          width=20, height=2)
        self.right_plate_label.pack(pady=(20, 0))
        # 创建左侧按钮样式
        btn_style = ttk.Style()
        btn_style.configure("btnStyle.TButton", font=("微软雅黑", 12), width=13)
        # 创建左侧"一键识别"按钮
        self.left_match_btn = ttk.Button(self.left_frm, text="一键识别", style="btnStyle.TButton",
                                         command=self.fun_identify)
        self.left_match_btn.pack(pady=(0, 0), side=tk.LEFT, padx=(75, 0))
        # 创建左侧"详细信息"按钮
        self.left_details_btn = ttk.Button(self.left_frm, text="展示细节", style="btnStyle.TButton")
        self.left_details_btn.pack(pady=(0, 0), side=tk.LEFT, padx=(25, 0))
        # 创建右侧"查找车主"按钮
        self.right_query_btn = ttk.Button(self.right_frm, text="查找车主", style="btnStyle.TButton")
        self.right_query_btn.pack(side=tk.LEFT, padx=(70, 0), pady=(50, 27))
        # 创建右侧"登记车牌"按钮
        self.right_register_btn = ttk.Button(self.right_frm, text="登记车牌", style="btnStyle.TButton")
        self.right_register_btn.pack(side=tk.LEFT, padx=(25, 0), pady=(50, 27))
