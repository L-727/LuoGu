# 导入系统模块，提供对系统功能的访问  
import sys  
# 导入时间模块，提供对时间的访问和控制  
import time  
# 从tkinter库中导入所有模块，提供GUI相关的功能  
from tkinter import *  
# 导入滚动文本框模块，提供带滚动条的文本框功能  
from tkinter import scrolledtext  
  
# 从lab_and_dif模块中导入所有内容，提供与题目难度和标签相关的功能  
from lab_and_dif import *  
# 从qus_and_ans模块中导入所有内容，提供与题目和答案相关的功能  
from qus_and_ans import *  
  
# 定义一个名为invoke的函数  
def invoke():  
    
    # 获取用户选择的难度  
    difficulty = selectedDiff.get()  
    # 获取用户输入的标签，使用逗号进行分隔  
    tags = tagEntry.get().split(',')  
    # 创建一个空列表，用于存放清除无效标签后的标签列表  
    # 清除无效标签  
    clearTags = []  
    # 遍历用户输入的标签列表  
    for item in tags:  
        # 如果标签不为空，则将其添加到清除无效标签后的标签列表中  
        if item != '':  
            clearTags.append(item)  
    # 获取用户输入的关键词  
    keyword = keywordEntry.get()  
  
    # 根据用户输入的难度、清除无效标签后的标签列表和关键词，获取题目ID和总数  
    # 根据输入的条件爬取pid  
    result1, result2 = getPids(difficulty, clearTags, keyword)  
    # 如果获取的结果1为"invalid tag"，则打印错误信息并停止程序执行  
    if result1 == "invalid tag":  
        print("请输入正确的标签！！")  
        return 0  
  
    # 将获取的总数赋值给totalCount变量，将获取的题目列表赋值给problems变量  
    totalCount = result1  
    problems = result2  
  
    # 创建一个计数器cnt，用于记录已获取的题目数量  
    # 根据pid爬取题目  
    cnt = 0  
    # 遍历获取的题目列表  
    for item in problems:  
        # 获取每个题目的ID和标题  
        pid = item["pid"]  
        title = item["title"]  
          
        # 根据题目ID、标题、难度、标签和关键词获取题目信息，并将结果赋值给result变量  
        result = getProblem(pid, title, difficulty, clearTags, keyword)  
        # 如果result为"error"，则打印错误信息并停止程序执行  
        if result == "error":  
            print("P1050内所有符合要求的题目已经全部被爬取！！！ 或 P1050内无符合要求的题目！！！")  
            return 0  
        # 将计数器cnt加1  
        cnt += 1  
        # 如果计数器cnt达到50，则停止遍历题目列表并退出循环  
        if cnt == 50:  
            break  
  
# 定义一个集合，存放可选的难度选项  
difficultyOptions = {"无选择", "暂无评定", "入门", "普及-", "普及/提高-", "普及+/提高", "提高+/省选-", "省选/NOI-", "NOI/NOI+/CTSC"}  
# 创建一个主窗口对象，并设置窗口标题、大小和背景颜色  
# 创建主窗口  
window = Tk()  
window.title("mihoyo")  
window.geometry("1200x800")  
window.configure(bg="Pink")  
  
# 创建一个标签对象，设置文本、背景颜色和宽度，并将标签添加到主窗口上  
# 设置题库  
typeLabel = Label(window, text="爬虫",  bg="PaleTurquoise", width=30)  
typeLabel.grid(row=0, column=3, sticky="w", padx=10, pady=10)  
  
# 创建一个框架对象，设置背景颜色，并将框架添加到主窗口上  
# 设置难度下拉框  

# 设置难度下拉框
#创建一个名为difficultyFrame的框架对象，该框架对象是window的子窗口，背景颜色为银色
difficultyFrame = Frame(window, bg="Silver")
#将difficultyFrame放置在网格布局中，从第一行开始，从第一列开始，跨越4列，水平和垂直方向上的填充都为10，且当窗口大小改变时，该框架会保持在其原始位置
difficultyFrame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
#创建一个标签对象diffLabel，该标签对象是difficultyFrame的子窗口，显示的文本为“难度:”，背景颜色为银色，宽度为6个字符。
diffLabel = Label(difficultyFrame, text="难度:", bg="Silver",width=6)
#将diffLabel放置在difficultyFrame中，从左侧开始，水平和垂直方向上的填充分别为0和10
diffLabel.pack(side="left", padx=0, pady=10)
#创建一个字符串变量selectedDiff，该变量与window关联，初始值为“无选择”。
selectedDiff = StringVar(window, "无选择")
#创建一个选项菜单对象diffMenu，该菜单对象是difficultyFrame的子窗口，关联的变量为selectedDiff，选项列表为difficultyOptions中的所有元素。
diffMenu = OptionMenu(difficultyFrame, selectedDiff, *difficultyOptions)
#置diffMenu的宽度为18个字符，高度为1个字符
diffMenu.config(width=18, height=1)
#将diffMenu放置在difficultyFrame中，从左侧开始，水平和垂直方向上的填充分别为10
diffMenu.pack(side="left", padx=10, pady=10)

# 设置标签输入框
tagFrame = Frame(window, bg="Silver")
tagFrame.grid(row=1, column=3, columnspan=5, padx=10, pady=10, sticky="ew")
tagLabel = Label(tagFrame, text="标签:", bg="Silver", width=6)
tagLabel.pack(side="left", padx=0, pady=10)
tagEntry = Entry(tagFrame, width=23, borderwidth=3, relief="solid")
tagEntry.pack(side="left", padx=20, pady=10)

# 设置关键词输入框
# 创建一个名为keywordFrame的框架，该框架是window的子窗口，背景颜色为银色  
keywordFrame = Frame(window, bg="Silver")  
  
# 将keywordFrame放置在网格布局中，从第一行开始，从第5列开始，跨越5列，水平和垂直方向上的填充分别为10和11，且当窗口大小改变时，该框架会保持在其原始位置  
keywordFrame.grid(row=1, column=4, columnspan=5, padx=10, pady=10, sticky="ew")  
  
# 创建一个标签对象keywordLabel，该标签对象是keywordFrame的子窗口，显示的文本为“关键词:”，背景颜色为银色，宽度为5个字符  
keywordLabel = Label(keywordFrame, text="关键词:",  bg="Silver", width=5)
  
# 将keywordLabel放置在keywordFrame中，从左侧开始，水平和垂直方向上的填充分别为0和10  
keywordLabel.pack(side="left", padx=0, pady=10)  
  
# 创建一个输入框对象keywordEntry，该输入框对象是keywordFrame的子窗口，宽度为25个字符，边框宽度为6，边框样式为实线  
keywordEntry = Entry(keywordFrame, width=23, borderwidth=3, relief="solid")  
  
# 将keywordEntry放置在keywordFrame中，从左侧开始，水平和垂直方向上的填充分别为20和10  
keywordEntry.pack(side="left", padx=20, pady=10)

# 设置启动按钮
searchButton = Button(window, text="!!!!!启动!!!!!",  width=30, height=1, bg="red",command=invoke)
searchButton.grid(row=5, column=3, padx=10, pady=10)

# 设置日志
logFrame = Frame(window, bg="Tan")
logFrame.grid(row=6, column=0, columnspan=5, padx=10, pady=10,sticky="ew")

logText = scrolledtext.ScrolledText(logFrame,  width=100, height=30, bd=2)
logText.pack()


def redirect_output():
    # 输出日志
    def custom_write(msg):
        logText.insert("end", msg)
        logText.see("end")
        logText.update()

    # 将stdout和stderr重定向到自定义写函数
    sys.stdout.write = custom_write
    sys.stderr.write = custom_write


if __name__ == '__main__':
    redirect_output()
    window.mainloop()