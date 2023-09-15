import tkinter as tk  
from tkinter import filedialog  
from question import * 
from tkinter import messagebox
import sys
import time
from tkinter import scrolledtext
from tkinter import *

# 创建Tkinter窗口  
root = tk.Tk()
root.geometry("1000x500")  
root.title("题目爬取工具")  
  
# 创建输入框，用于接收用户输入的关键词  
keyword_entry = tk.Entry(root) 
Label =  Label(keyword_entry, text="标签:", bg="white", width=6) 
keyword_entry.pack()  
  
# 创建下拉框，用于选择题目难度  
difficulty_var = tk.StringVar(root)  
difficulty_var.set("请选择难度") # 默认值  
difficulty_options = ["暂无评定入门", "普及-", "普及/提高-", "普及+/提高", "提高+/省选-", "省选/NOI-", "NOI/NOI+/CTSC"]  
difficulty_dropdown = tk.OptionMenu(root, difficulty_var, *difficulty_options)  
difficulty_dropdown.pack()  
  


# 创建按钮，用于开始爬取题目  
def question():  
    keyword = keyword_entry.get()  
    difficulty = difficulty_var.get()  
    # TODO: 根据关键词和难度去爬取题目  
    pass  
  
start_button = tk.Button(root, text="开始爬取", command=question)  
start_button.pack()  
 
# 运行Tkinter的主循环  
root.mainloop()
