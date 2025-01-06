import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import font
from abc import ABC, abstractmethod

def MiSans(size=12, weight="normal"):
    return font.Font(family="MiSans", size=size, weight=weight)

# 启用高 DPI 支持
def enable_high_dpi_awareness():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print(f"Failed to set DPI awareness: {e}")
        
# 获取屏幕 DPI
def get_screen_dpi(root):
    return root.winfo_fpixels('1i')

# 根据 DPI 调整窗口大小
def adjust_window_size(root, base_width, base_height):
    dpi = get_screen_dpi(root)
    scaling_factor = dpi / 96  # 96 DPI 是标准 DPI
    new_width = int(base_width * scaling_factor)
    new_height = int(base_height * scaling_factor)
    root.geometry(f"{new_width}x{new_height}")

# 定义物品类型类
class ItemType:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

# 定义用户类
class User:
    def __init__(self, username, password, address, contact_info, user_type="user", is_approved=False):
        self.username = username
        self.password = password
        self.address = address
        self.contact_info = contact_info
        self.user_type = user_type
        self.is_approved = is_approved

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "address": self.address,
            "contact_info": self.contact_info,
            "user_type": self.user_type,
            "is_approved": self.is_approved
        }

    @staticmethod
    def from_dict(data):
        return User(
            data["username"],
            data["password"],
            data["address"],
            data["contact_info"],
            data["user_type"],
            data["is_approved"]
        )

# 保存和加载用户信息
def save_users(users, filename="users.json"):
    users_data = [user.to_dict() for user in users]
    with open(filename, "w") as file:
        json.dump(users_data, file, indent=4)

def load_users(filename="users.json"):
    try:
        with open(filename, "r") as file:
            users_data = json.load(file)
            return [User.from_dict(data) for data in users_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise ValueError("文件格式不正确")

# 保存和加载物品类型信息
def save_item_types(item_types, filename="item_types.json"):
    item_types_data = [{"name": it.name, "attributes": it.attributes} for it in item_types]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(item_types_data, file, ensure_ascii=False, indent=4)

def load_item_types(filename="item_types.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            item_types_data = json.load(file)
            return [ItemType(it["name"], it["attributes"]) for it in item_types_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise ValueError("文件格式不正确")

# 定义抽象基类 Item
class Item(ABC):
    def __init__(self, name, description, location, contact_phone, email, added_by, **kwargs):
        self.name = name
        self.description = description
        self.location = location
        self.contact_phone = contact_phone
        self.email = email
        self.added_by = added_by
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def get_details(self):
        pass

    def to_dict(self):
        data = {
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "contact_phone": self.contact_phone,
            "email": self.email,
            "added_by": self.added_by,
            "type": self.__class__.__name__
        }
        for key, value in self.__dict__.items():
            if key not in data:
                data[key] = value
        return data

    @staticmethod
    def from_dict(data):
        item_type = data.get("type")
        if item_type in item_classes:
            item_class = item_classes[item_type]
            args = {
                "name": data["name"],
                "description": data["description"],
                "location": data["location"],
                "contact_phone": data["contact_phone"],
                "email": data["email"],
                "added_by": data["added_by"]
            }
            for attr in item_class.attributes:
                args[attr] = data[attr]
            return item_class(**args)
        else:
            raise ValueError("Unknown item type")

# 动态创建的物品种类类
item_classes = {}

def create_item_class(name, attributes):
    def get_details(self):
        details = (f"物品名称: {self.name}\n"
                   f"物品说明: {self.description}\n"
                   f"所在地址: {self.location}\n"
                   f"联系人手机: {self.contact_phone}\n"
                   f"邮箱: {self.email}\n"
                   f"物品种类: {self.__class__.__name__}\n"
                   f"添加用户名: {self.added_by}\n")
        for attr in attributes:
            details += f"{attr}: {getattr(self, attr)}\n"
        return details

    def to_dict(self):
        data = super(type(self), self).to_dict()
        data.update({attr: getattr(self, attr) for attr in attributes})
        data["type"] = name
        return data

    def from_dict(data):
        args = {
            "name": data["name"],
            "description": data["description"],
            "location": data["location"],
            "contact_phone": data["contact_phone"],
            "email": data["email"],
            "added_by": data["added_by"]
        }
        for attr in attributes:
            args[attr] = data[attr]
        return type(name, (Item,), args)(**args)

    item_class = type(name, (Item,), {
        "__init__": lambda self, name, description, location, contact_phone, email, added_by, **kwargs: Item.__init__(self, name, description, location, contact_phone, email, added_by, **kwargs),
        "get_details": get_details,
        "to_dict": to_dict,
        "from_dict": from_dict,
        "attributes": attributes  # 存储属性列表
    })
    item_classes[name] = item_class
    return item_class

# 主窗口
class MainWindow:
    def __init__(self, root, users, item_types):
        self.root = root
        self.root.title("物品复活软件")
        adjust_window_size(root, 300, 200)
        #self.root.geometry("300x300+300+100")

        self.users = users
        self.item_types = item_types

        # 用户名输入框
        tk.Label(root, text="用户名:", font=MiSans()).pack()
        self.username_entry = tk.Entry(root, font=MiSans(), width=16)
        self.username_entry.pack()

        # 密码输入框
        tk.Label(root, text="密码:", font=MiSans()).pack()
        self.password_entry = tk.Entry(root, font=MiSans(), width=16, show="*")
        self.password_entry.pack()

        # 登录按钮
        self.login_button = tk.Button(root, text="登录", font=MiSans(10), command=self.login_user)
        self.login_button.pack(pady=10)

        # 注册按钮
        self.register_button = tk.Button(root, text="注册", font=MiSans(10), command=self.register_user)
        self.register_button.pack(pady=5)

    def register_user(self):
        RegisterDialog(self.root, self.users)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        for user in self.users:
            if user.username == username and user.password == password and user.is_approved:
                if user.user_type == "admin":
                    self.show_admin_interface(user)
                else:
                    self.show_user_interface(user)
                return
        messagebox.showerror("登录失败", "用户名、密码错误或未批准。")

    def show_admin_interface(self, user):
        self.root.withdraw()  # 隐藏主窗口
        admin_root = tk.Toplevel(self.root)
        admin_root.title("管理员界面")
        AdminInterface(admin_root, self.item_types, self.users)
        admin_root.protocol("WM_DELETE_WINDOW", self.on_close)  # 监听关闭事件

    def show_user_interface(self, user):
        self.root.withdraw()  # 隐藏主窗口
        user_root = tk.Toplevel(self.root)
        user_root.title("用户界面")
        UserInterface(user_root, self.item_types, user)
        user_root.protocol("WM_DELETE_WINDOW", self.on_close)  # 监听关闭事件

    def on_close(self):
        self.root.destroy()  # 销毁主窗口


# 注册对话框
class RegisterDialog:
    def __init__(self, parent, users):
        self.parent = parent
        self.users = users
        self.top = tk.Toplevel(parent)
        self.top.title("注册")
        adjust_window_size(self.top, 300, 200)
        #self.top.geometry("300x300+300+100")

        self.username_var = tk.StringVar(self.top)
        self.password_var = tk.StringVar(self.top)
        self.address_var = tk.StringVar(self.top)
        self.contact_info_var = tk.StringVar(self.top)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.top, text="用户名:", font=MiSans()).grid(row=0, column=0, sticky="e")
        tk.Entry(self.top, textvariable=self.username_var, font=MiSans(), width=16).grid(row=0, column=1, sticky="w")

        tk.Label(self.top, text="密码:", font=MiSans()).grid(row=1, column=0, sticky="e")
        tk.Entry(self.top, textvariable=self.password_var, show="*", font=MiSans(), width=16).grid(row=1, column=1, sticky="w")

        tk.Label(self.top, text="住址:", font=MiSans()).grid(row=2, column=0, sticky="e")
        tk.Entry(self.top, textvariable=self.address_var, font=MiSans(), width=16).grid(row=2, column=1, sticky="w")

        tk.Label(self.top, text="联系方式:", font=MiSans()).grid(row=3, column=0, sticky="e")
        tk.Entry(self.top, textvariable=self.contact_info_var, font=MiSans(), width=16).grid(row=3, column=1, sticky="w")

        tk.Button(self.top, text="注册", command=self.on_register, font=MiSans(10)).grid(row=4, column=0, columnspan=2)

    def on_register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        address = self.address_var.get()
        contact_info = self.contact_info_var.get()

        if not all([username, password, address, contact_info]):
            messagebox.showerror("错误", "请输入所有必填信息")
            return

        user = User(username, password, address, contact_info)
        self.users.append(user)
        save_users(self.users)
        messagebox.showinfo("注册成功", "您的注册申请已提交，等待管理员批准。")
        self.top.destroy()

# 管理员界面
class AdminInterface:
    def __init__(self, root, item_types, users):
        self.root = root
        adjust_window_size(root, 300, 300)
        #self.root.geometry("300x400+300+100")
        self.item_types = item_types
        self.users = users

        self.listbox = tk.Listbox(root, font=MiSans(), width=16, height=10)
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-1>", self.show_item_type_details)

        self.add_button = tk.Button(root, text="添加物品类型", command=self.add_item_type, font=MiSans(10))
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.approve_button = tk.Button(root, text="审核用户", command=self.approve_users, font=MiSans(10))
        self.approve_button.pack(side=tk.LEFT, padx=5)

        self.load_item_types()
        #self.load_users()
        
    def show_item_type_details(self, event):
        try:
            index = self.listbox.curselection()[0]
            item_type = self.item_types[index]
            details = (f"物品种类: {item_type.name}\n"
                       f"物品属性: {', '.join(item_type.attributes)}\n")
            messagebox.showinfo("物品种类详细信息", details)
        except IndexError:
            messagebox.showerror("错误", "请选择一个物品种类")

    def add_item_type(self):
        name = simpledialog.askstring("添加物品类型", "物品类型名称:")
        if not name:
            return

        attributes = simpledialog.askstring("添加物品类型", "物品特有属性（用逗号分隔）:")
        if not attributes:
            return

        attributes = [attr.strip() for attr in attributes.split(",")]
        item_type = ItemType(name, attributes)
        self.item_types.append(item_type)
        self.listbox.insert(tk.END, name)
        save_item_types(self.item_types)
        create_item_class(name, attributes)  # 动态创建新的物品种类类
        
    def load_users(self):
        self.listbox.delete(0, tk.END)
        for user in self.users:
            if not user.is_approved:
                self.listbox.insert(tk.END, user.username)

    def show_user_details(self, event, user_listbox, users):
        try:
            index = user_listbox.curselection()[0]
            username = user_listbox.get(index)
            user = next(u for u in users if u.username == username)
            details = (f"用户名: {user.username}\n"
                       f"密码: {user.password}\n"
                       f"住址: {user.address}\n"
                       f"联系方式: {user.contact_info}\n"
                       f"用户类型: {user.user_type}\n"
                       f"是否批准: {user.is_approved}\n")
            messagebox.showinfo("用户详细信息", details)
        except IndexError:
            messagebox.showerror("错误", "请选择一个用户")

    def approve_users(self):
        top = tk.Toplevel(self.root)
        top.title("审核用户")
        top.geometry("300x300+300+100")

        user_listbox = tk.Listbox(top, font=MiSans(), width=16, height=10)
        user_listbox.pack(pady=10)
        user_listbox.bind("<Double-1>", lambda event: self.show_user_details(event, user_listbox, self.users))  # 绑定双击事件

        for user in self.users:
            if not user.is_approved:
                user_listbox.insert(tk.END, user.username)

        def approve_selected():
            selected_indices = user_listbox.curselection()
            for index in selected_indices:
                username = user_listbox.get(index)
                user = next(u for u in self.users if u.username == username)
                user.is_approved = True
            save_users(self.users)
            user_listbox.delete(0, tk.END)
            self.load_users()
            top.destroy()
            self.load_item_types()

        approve_button = tk.Button(top, text="批准所选用户", font=MiSans(10), command=approve_selected)
        approve_button.pack(pady=10)

        top.mainloop()

    def load_item_types(self):
        for item_type in self.item_types:
            self.listbox.insert(tk.END, item_type.name)

# 用户界面
class UserInterface:
    def __init__(self, root, item_types, user):
        self.root = root
        adjust_window_size(root, 300, 300)
        #self.root.geometry("300x400+300+100")
        self.item_types = item_types
        self.user = user
        self.items = []
        self.filename = "items.json"

        self.listbox = tk.Listbox(root, font=MiSans(), width=16, height=10)
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-1>", self.show_item_details)  # 绑定双击事件

        self.add_button = tk.Button(root, text="添加物品", font=MiSans(10), command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = tk.Button(root, text="删除物品", font=MiSans(10), command=self.delete_item)
        self.delete_button.pack(side=tk.LEFT, padx=10)

        self.find_button = tk.Button(root, text="查找物品", font=MiSans(10), command=self.find_item)
        self.find_button.pack(side=tk.LEFT, padx=10)

        self.load_items()

    def add_item(self):
        top = tk.Toplevel(self.root)
        top.title("添加物品")
        adjust_window_size(top, 300, 300)
        #top.geometry("300x300+300+100")
        

        category_var = tk.StringVar(top)
        #category_var.set(self.item_types[0].name if self.item_types else "")  # 默认值
        category_var.set("请选择")
        tk.Label(top, text="物品种类:", font=MiSans()).grid(row=0, column=0, sticky="e")
        category_option = tk.OptionMenu(top, category_var, *[it.name for it in self.item_types])
        category_option.config(font=MiSans())
        category_option.grid(row=0, column=1, sticky="w")

        name_var = tk.StringVar(top)
        description_var = tk.StringVar(top)
        location_var = tk.StringVar(top)
        contact_phone_var = tk.StringVar(top)
        email_var = tk.StringVar(top)

        name_entry = tk.Entry(top, textvariable=name_var, font=MiSans(), width=16)
        description_entry = tk.Entry(top, textvariable=description_var, font=MiSans(), width=16)
        location_entry = tk.Entry(top, textvariable=location_var, font=MiSans(), width=16)
        contact_phone_entry = tk.Entry(top, textvariable=contact_phone_var, font=MiSans(), width=16)
        email_entry = tk.Entry(top, textvariable=email_var, font=MiSans(), width=16)

        tk.Label(top, text="物品名称:", font=MiSans()).grid(row=1, column=0, sticky="e")
        name_entry.grid(row=1, column=1, sticky="w")

        tk.Label(top, text="物品说明:", font=MiSans()).grid(row=2, column=0, sticky="e")
        description_entry.grid(row=2, column=1, sticky="w")

        tk.Label(top, text="所在地址:", font=MiSans()).grid(row=3, column=0, sticky="e")
        location_entry.grid(row=3, column=1, sticky="w")

        tk.Label(top, text="联系人手机:", font=MiSans()).grid(row=4, column=0, sticky="e")
        contact_phone_entry.grid(row=4, column=1, sticky="w")

        tk.Label(top, text="邮箱:", font=MiSans()).grid(row=5, column=0, sticky="e")
        email_entry.grid(row=5, column=1, sticky="w")

        # 存储属性变量
        attr_vars = {}

        def update_attributes(*args):
            for widget in top.winfo_children():
                if isinstance(widget, tk.Entry) and widget not in [name_entry, description_entry, location_entry, contact_phone_entry, email_entry]:
                    widget.destroy()

            selected_category = category_var.get()
            for item_type in self.item_types:
                if item_type.name == selected_category:
                    row = 6
                    for attr in item_type.attributes:
                        attr_var = tk.StringVar(top)
                        attr_vars[attr] = attr_var  # 存储变量
                        tk.Label(top, text=f"{attr}:", font=MiSans()).grid(row=row, column=0, sticky="e")
                        tk.Entry(top, textvariable=attr_var, name=f"{attr}_var", font=MiSans(), width=16).grid(row=row, column=1, sticky="w")
                        row += 1
                    break

        category_var.trace("w", update_attributes)

        # 动态计算按钮的行号
        row = 6 + len(self.item_types[0].attributes) if self.item_types else 6

        tk.Button(top, text="确定", font=MiSans(10), command=lambda: self.create_item(
            category_var.get(), name_var.get(), description_var.get(), location_var.get(),
            contact_phone_var.get(), email_var.get(), top)).grid(row=row, column=0, columnspan=2)

    def create_item(self, category, name, description, location, contact_phone, email, top):
        item_class = item_classes.get(category)
        if item_class:
            # 获取所有属性输入字段的值
            attributes = {}
            for attr in item_class.attributes:
                attr_var = top.nametowidget(f"{attr}_var")
                if attr_var:
                    attributes[attr] = attr_var.get()
                else:
                    attributes[attr] = ""  # 如果没有找到对应的输入字段，使用默认值

            # 创建物品实例
            item = item_class(name, description, location, contact_phone, email, self.user.username, **attributes)
            self.items.append(item)
            self.listbox.insert(tk.END, name)
            self.save_items()
            top.destroy()
        else:
            messagebox.showerror("错误", "物品种类不匹配")

    def delete_item(self):
        try:
            index = self.listbox.curselection()[0]
            item_name = self.items[index].name
            if messagebox.askyesno("确认删除", f"确定要删除物品 '{item_name}' 吗？"):
                self.items.pop(index)
                self.listbox.delete(index)
                self.save_items()
        except IndexError:
            messagebox.showerror("错误", "请选择要删除的物品")

    def find_item(self):
        top = tk.Toplevel(self.root)
        top.title("查找物品")
        adjust_window_size(top, 300, 100)
        #top.geometry("300x300+300+100")

        category_var = tk.StringVar(top)
        category_var.set("请选择")  # 默认值
        tk.Label(top, text="物品种类:", font=MiSans()).grid(row=0, column=0, sticky="e")
        category_option = tk.OptionMenu(top, category_var, *[it.name for it in self.item_types])
        category_option.config(font=MiSans())
        category_option.grid(row=0, column=1, sticky="w")

        keyword_var = tk.StringVar(top)
        tk.Label(top, text="关键词:", font=MiSans()).grid(row=1, column=0, sticky="e")
        keyword_entry = tk.Entry(top, textvariable=keyword_var, font=MiSans(), width=16)
        keyword_entry.grid(row=1, column=1, sticky="w")

        def on_search():
            category = category_var.get()
            keyword = keyword_var.get()
            if category == "请选择" or not keyword:
                messagebox.showerror("错误", "请选择物品种类并输入关键词")
                return

            found_items = []
            for item in self.items:
                if (item.__class__.__name__ == category and (
                    keyword.lower() in item.name.lower() or 
                    keyword.lower() in item.description.lower() or 
                    keyword.lower() in item.added_by.lower()
                )):
                    found_items.append(item)

            if found_items:
                items_info = ""
                for item in found_items:
                    items_info += item.get_details() + "\n\n"
                messagebox.showinfo("查找结果", items_info)
            else:
                messagebox.showinfo("未找到", "未找到包含该关键词的物品")
            top.destroy()

        tk.Button(top, text="搜索", command=on_search, font=MiSans(10)).grid(row=2, column=0, columnspan=2)
            
    def show_item_details(self, event):
        try:
            index = self.listbox.curselection()[0]
            item = self.items[index]
            details = (f"物品名称: {item.name}\n"
                       f"物品说明: {item.description}\n"
                       f"所在地址: {item.location}\n"
                       f"联系人手机: {item.contact_phone}\n"
                       f"邮箱: {item.email}\n"
                       f"物品种类: {item.__class__.__name__}\n"
                       f"添加用户: {item.added_by}\n")
            for attr in item.__dict__:
                if attr not in ["name", "description", "location", "contact_phone", "email", "added_by"]:
                    details += f"{attr}: {getattr(item, attr)}\n"
            messagebox.showinfo("物品详细信息", details)
        except IndexError:
            messagebox.showerror("错误", "请选择一个物品")

    def save_items(self):
        items_data = [item.to_dict() for item in self.items]
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(items_data, file, ensure_ascii=False, indent=4)

    def load_items(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                items_data = json.load(file)
                self.items = [Item.from_dict(data) for data in items_data]
                self.listbox.delete(0, tk.END)
                for item in self.items:
                    self.listbox.insert(tk.END, item.name)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            messagebox.showerror("错误", "文件格式不正确")

# 主函数
if __name__ == "__main__":
    enable_high_dpi_awareness()
    
    root = tk.Tk()
    root.title("物品复活软件")

    # 初始化物品类型和用户列表
    item_types = load_item_types()
    users = load_users()

    # 为每个物品种类动态创建继承类
    for item_type in item_types:
        create_item_class(item_type.name, item_type.attributes)

    # 主窗口
    app = MainWindow(root, users, item_types)

    root.mainloop()

    # 程序退出时保存用户信息和物品类型信息
    save_users(users)
    save_item_types(item_types)