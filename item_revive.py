import json
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

class Item:
    def __init__(self, name, description, contact_info):
        self.name = name
        self.description = description
        self.contact_info = contact_info

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "contact_info": self.contact_info
        }

    @staticmethod
    def from_dict(data):
        return Item(data["name"], data["description"], data["contact_info"])

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("物品复活软件")

        self.items = []
        self.filename = "items.json"  # 默认保存文件名

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

        self.load_items()  # 在初始化时加载物品列表

    def add_item(self):
        name = simpledialog.askstring("添加物品", "物品名称:")
        if not name:
            return

        description = simpledialog.askstring("添加物品", "物品描述:")
        if not description:
            return

        contact_info = simpledialog.askstring("添加物品", "联系人信息:")
        if not contact_info:
            return

        item = Item(name, description, contact_info)
        self.items.append(item)
        self.listbox.insert(tk.END, name)
        self.save_items()  # 添加物品后自动保存

    def delete_item(self):
        try:
            index = self.listbox.curselection()[0]
            self.items.pop(index)
            self.listbox.delete(index)
            self.save_items()  # 删除物品后自动保存
        except IndexError:
            messagebox.showerror("错误", "请选择要删除的物品")

    def show_items(self):
        items_info = ""
        for item in self.items:
            items_info += f"名称: {item.name}\n描述: {item.description}\n联系人信息: {item.contact_info}\n\n"
        messagebox.showinfo("物品列表", items_info)

    def find_item(self):
        name = simpledialog.askstring("查找物品", "物品名称:")
        if not name:
            return

        for item in self.items:
            if item.name == name:
                messagebox.showinfo("物品信息", f"名称: {item.name}\n描述: {item.description}\n联系人信息: {item.contact_info}")
                return
        messagebox.showinfo("未找到", "未找到该物品")

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
            pass  # 如果文件不存在，忽略错误
        except json.JSONDecodeError:
            messagebox.showerror("错误", "文件格式不正确")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
