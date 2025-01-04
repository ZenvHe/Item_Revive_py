import json
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from abc import ABC, abstractmethod

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
    with open(filename, "w") as file:
        json.dump(item_types_data, file, indent=4)

def load_item_types(filename="item_types.json"):
    try:
        with open(filename, "r") as file:
            item_types_data = json.load(file)
            return [ItemType(it["name"], it["attributes"]) for it in item_types_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        raise ValueError("文件格式不正确")

# 定义抽象基类 Item
class Item(ABC):
    def __init__(self, name, description, location, contact_phone, email):
        self.name = name
        self.description = description
        self.location = location
        self.contact_phone = contact_phone
        self.email = email

    @abstractmethod
    def get_details(self):
        pass

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "contact_phone": self.contact_phone,
            "email": self.email
        }

    @staticmethod
    def from_dict(data):
        item_type = data.get("type")
        if item_type == "food":
            return FoodItem.from_dict(data)
        elif item_type == "book":
            return BookItem.from_dict(data)
        else:
            raise ValueError("Unknown item type")

# 定义食品类物品 FoodItem
class FoodItem(Item):
    def __init__(self, name, description, location, contact_phone, email, expiration_date, quantity):
        super().__init__(name, description, location, contact_phone, email)
        self.expiration_date = expiration_date
        self.quantity = quantity

    def get_details(self):
        return (f"物品名称: {self.name}\n"
                f"物品说明: {self.description}\n"
                f"所在地址: {self.location}\n"
                f"联系人手机: {self.contact_phone}\n"
                f"邮箱: {self.email}\n"
                f"保质期: {self.expiration_date}\n"
                f"数量: {self.quantity}")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "food",
            "expiration_date": self.expiration_date,
            "quantity": self.quantity
        })
        return data

    @staticmethod
    def from_dict(data):
        return FoodItem(
            data["name"],
            data["description"],
            data["location"],
            data["contact_phone"],
            data["email"],
            data["expiration_date"],
            data["quantity"]
        )

# 定义书籍类物品 BookItem
class BookItem(Item):
    def __init__(self, name, description, location, contact_phone, email, author, publisher):
        super().__init__(name, description, location, contact_phone, email)
        self.author = author
        self.publisher = publisher

    def get_details(self):
        return (f"物品名称: {self.name}\n"
                f"物品说明: {self.description}\n"
                f"所在地址: {self.location}\n"
                f"联系人手机: {self.contact_phone}\n"
                f"邮箱: {self.email}\n"
                f"作者: {self.author}\n"
                f"出版社: {self.publisher}")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "type": "book",
            "author": self.author,
            "publisher": self.publisher
        })
        return data

    @staticmethod
    def from_dict(data):
        return BookItem(
            data["name"],
            data["description"],
            data["location"],
            data["contact_phone"],
            data["email"],
            data["author"],
            data["publisher"]
        )
    
class RegisterDialog:
    def __init__(self, parent, users):
        self.parent = parent
        self.users = users
        self.top = tk.Toplevel(parent)
        self.top.title("注册")

        self.username_var = tk.StringVar(self.top)
        self.password_var = tk.StringVar(self.top)
        self.address_var = tk.StringVar(self.top)
        self.contact_info_var = tk.StringVar(self.top)

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.top, text="用户名:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.top, textvariable=self.username_var).grid(row=0, column=1, sticky="w")

        tk.Label(self.top, text="密码:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.top, textvariable=self.password_var, show="*").grid(row=1, column=1, sticky="w")

        tk.Label(self.top, text="住址:").grid(row=2, column=0, sticky="e")
        tk.Entry(self.top, textvariable=self.address_var).grid(row=2, column=1, sticky="w")

        tk.Label(self.top, text="联系方式:").grid(row=3, column=0, sticky="e")
        tk.Entry(self.top, textvariable=self.contact_info_var).grid(row=3, column=1, sticky="w")

        tk.Button(self.top, text="注册", command=self.on_register).grid(row=4, column=0, columnspan=2)

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

class MainWindow:
    def __init__(self, root, users, item_types):
        self.root = root
        self.root.title("物品管理系统")

        self.users = users
        self.item_types = item_types

        # 用户名输入框
        tk.Label(root, text="用户名:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        # 密码输入框
        tk.Label(root, text="密码:").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        # 登录按钮
        self.login_button = tk.Button(root, text="登录", command=self.login_user)
        self.login_button.pack(pady=10)

        # 注册按钮
        self.register_button = tk.Button(root, text="注册", command=self.register_user)
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
        AdminInterface(admin_root, self.item_types)
        admin_root.protocol("WM_DELETE_WINDOW", self.on_close_admin)  # 监听关闭事件

    def show_user_interface(self, user):
        self.root.withdraw()  # 隐藏主窗口
        user_root = tk.Toplevel(self.root)
        user_root.title("用户界面")
        UserInterface(user_root, self.item_types)
        user_root.protocol("WM_DELETE_WINDOW", self.on_close_user)  # 监听关闭事件

    def on_close_admin(self):
        self.root.destroy()  # 重新显示主窗口

    def on_close_user(self):
        self.root.destroy()  # 重新显示主窗口

    def manage_item_types(self):
        AdminInterface(self.root, self.item_types)

# 管理员界面
class AdminInterface:
    def __init__(self, root, item_types):
        self.root = root
        self.item_types = item_types

        self.listbox = tk.Listbox(root)
        self.listbox.pack(pady=10)

        self.add_button = tk.Button(root, text="添加物品类型", command=self.add_item_type)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.modify_button = tk.Button(root, text="修改物品类型", command=self.modify_item_type)
        self.modify_button.pack(side=tk.LEFT, padx=5)

        self.load_item_types()

    def add_item_type(self):
        name = simpledialog.askstring("添加物品类型", "物品类型名称:")
        if not name:
            return

        attributes = simpledialog.askstring("添加物品类型", "物品属性（用逗号分隔）:")
        if not attributes:
            return

        attributes = [attr.strip() for attr in attributes.split(",")]
        item_type = ItemType(name, attributes)
        self.item_types.append(item_type)
        self.listbox.insert(tk.END, name)
        save_item_types(self.item_types)

    def modify_item_type(self):
        try:
            index = self.listbox.curselection()[0]
            item_type = self.item_types[index]

            name = simpledialog.askstring("修改物品类型", "物品类型名称:", initialvalue=item_type.name)
            if not name:
                return

            attributes = simpledialog.askstring("修改物品类型", "物品属性（用逗号分隔）:", initialvalue=", ".join(item_type.attributes))
            if not attributes:
                return

            attributes = [attr.strip() for attr in attributes.split(",")]
            item_type.name = name
            item_type.attributes = attributes
            self.listbox.delete(index)
            self.listbox.insert(index, name)
            save_item_types(self.item_types)
        except IndexError:
            messagebox.showerror("错误", "请选择要修改的物品类型")

    def load_item_types(self):
        for item_type in self.item_types:
            self.listbox.insert(tk.END, item_type.name)

# 主窗口类
class UserInterface:
    def __init__(self, root, item_types):
        self.root = root
        self.root.title("物品复活软件")
        #self.user = user
        self.item_types = item_types

        self.items = []
        self.filename = "items.json"

        self.listbox = tk.Listbox(root)
        self.listbox.pack(pady=10)

        self.add_button = tk.Button(root, text="添加物品", command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(root, text="删除物品", command=self.delete_item)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.show_button = tk.Button(root, text="显示物品列表", command=self.show_items)
        self.show_button.pack(side=tk.LEFT, padx=5)

        self.find_button = tk.Button(root, text="查找物品", command=self.find_item)
        self.find_button.pack(side=tk.LEFT, padx=5)

        self.load_items()

    def add_item(self):
        category = self.choose_category()
        if category:
            self.create_item_dialog(category)

    def choose_category(self):
        top = tk.Toplevel(self.root)
        top.title("选择物品类别")

        category_var = tk.StringVar(top)
        category_var.set("食品")  # 默认值

        tk.Label(top, text="请选择物品类别:").pack()
        category_option = tk.OptionMenu(top, category_var, "食品", "书籍")
        category_option.pack()

        def on_ok():
            top.destroy()
            return category_var.get()

        tk.Button(top, text="确定", command=on_ok).pack()
        top.wait_window()  # 等待窗口关闭
        return category_var.get()

    def create_item_dialog(self, category):
        if category.lower() == "食品":
            self.create_food_item_dialog()
        elif category.lower() == "书籍":
            self.create_book_item_dialog()

    def create_food_item_dialog(self):
        top = tk.Toplevel(self.root)
        top.title("添加食品")

        name_var = tk.StringVar(top)
        description_var = tk.StringVar(top)
        location_var = tk.StringVar(top)
        contact_phone_var = tk.StringVar(top)
        email_var = tk.StringVar(top)
        expiration_date_var = tk.StringVar(top)
        quantity_var = tk.StringVar(top)

        tk.Label(top, text="物品名称:").grid(row=0, column=0, sticky="e")
        tk.Entry(top, textvariable=name_var).grid(row=0, column=1, sticky="w")

        tk.Label(top, text="物品说明:").grid(row=1, column=0, sticky="e")
        tk.Entry(top, textvariable=description_var).grid(row=1, column=1, sticky="w")

        tk.Label(top, text="所在地址:").grid(row=2, column=0, sticky="e")
        tk.Entry(top, textvariable=location_var).grid(row=2, column=1, sticky="w")

        tk.Label(top, text="联系人手机:").grid(row=3, column=0, sticky="e")
        tk.Entry(top, textvariable=contact_phone_var).grid(row=3, column=1, sticky="w")

        tk.Label(top, text="邮箱:").grid(row=4, column=0, sticky="e")
        tk.Entry(top, textvariable=email_var).grid(row=4, column=1, sticky="w")

        tk.Label(top, text="保质期:").grid(row=5, column=0, sticky="e")
        tk.Entry(top, textvariable=expiration_date_var).grid(row=5, column=1, sticky="w")

        tk.Label(top, text="数量:").grid(row=6, column=0, sticky="e")
        tk.Entry(top, textvariable=quantity_var).grid(row=6, column=1, sticky="w")

        tk.Button(top, text="确定", command=lambda: self.create_food_item(
            name_var.get(), description_var.get(), location_var.get(),
            contact_phone_var.get(), email_var.get(), expiration_date_var.get(),
            int(quantity_var.get()), top)).grid(row=7, column=0, columnspan=2)

    def create_food_item(self, name, description, location, contact_phone, email, expiration_date, quantity, top):
        item = FoodItem(name, description, location, contact_phone, email, expiration_date, quantity)
        self.items.append(item)
        self.listbox.insert(tk.END, name)
        self.save_items()
        top.destroy()

    def create_book_item_dialog(self):
        top = tk.Toplevel(self.root)
        top.title("添加书籍")

        name_var = tk.StringVar(top)
        description_var = tk.StringVar(top)
        location_var = tk.StringVar(top)
        contact_phone_var = tk.StringVar(top)
        email_var = tk.StringVar(top)
        author_var = tk.StringVar(top)
        publisher_var = tk.StringVar(top)

        tk.Label(top, text="物品名称:").grid(row=0, column=0, sticky="e")
        tk.Entry(top, textvariable=name_var).grid(row=0, column=1, sticky="w")

        tk.Label(top, text="物品说明:").grid(row=1, column=0, sticky="e")
        tk.Entry(top, textvariable=description_var).grid(row=1, column=1, sticky="w")

        tk.Label(top, text="所在地址:").grid(row=2, column=0, sticky="e")
        tk.Entry(top, textvariable=location_var).grid(row=2, column=1, sticky="w")

        tk.Label(top, text="联系人手机:").grid(row=3, column=0, sticky="e")
        tk.Entry(top, textvariable=contact_phone_var).grid(row=3, column=1, sticky="w")

        tk.Label(top, text="邮箱:").grid(row=4, column=0, sticky="e")
        tk.Entry(top, textvariable=email_var).grid(row=4, column=1, sticky="w")

        tk.Label(top, text="作者:").grid(row=5, column=0, sticky="e")
        tk.Entry(top, textvariable=author_var).grid(row=5, column=1, sticky="w")

        tk.Label(top, text="出版社:").grid(row=6, column=0, sticky="e")
        tk.Entry(top, textvariable=publisher_var).grid(row=6, column=1, sticky="w")

        tk.Button(top, text="确定", command=lambda: self.create_book_item(
            name_var.get(), description_var.get(), location_var.get(),
            contact_phone_var.get(), email_var.get(), author_var.get(),
            publisher_var.get(), top)).grid(row=7, column=0, columnspan=2)

    def create_book_item(self, name, description, location, contact_phone, email, author, publisher, top):
        item = BookItem(name, description, location, contact_phone, email, author, publisher)
        self.items.append(item)
        self.listbox.insert(tk.END, name)
        self.save_items()
        top.destroy()

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

    def show_items(self):
        items_info = ""
        for item in self.items:
            items_info += item.get_details() + "\n\n"
        messagebox.showinfo("物品列表", items_info)

    def find_item(self):
        keyword = simpledialog.askstring("查找物品", "请输入关键词:")
        if not keyword:
            return

        found_items = []
        for item in self.items:
            if keyword.lower() in item.name.lower():
                found_items.append(item)

        if found_items:
            items_info = ""
            for item in found_items:
                items_info += item.get_details() + "\n\n"
            messagebox.showinfo("查找结果", items_info)
        else:
            messagebox.showinfo("未找到", "未找到包含该关键词的物品")

    def save_items(self):
        items_data = [item.to_dict() for item in self.items]
        with open(self.filename, "w") as file:
            json.dump(items_data, file, indent=4)

    def load_items(self):
        try:
            with open(self.filename, "r") as file:
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
    root = tk.Tk()
    root.title("物品管理系统")

    # 初始化物品类型和用户列表
    item_types = load_item_types()
    users = load_users()

    # 主窗口
    app = MainWindow(root, users, item_types)

    root.mainloop()

    # 程序退出时保存用户信息和物品类型信息
    save_users(users)
    save_item_types(item_types)