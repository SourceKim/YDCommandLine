
'''
前景色         背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              洋红
36                46              青色
37                47              白色
显示方式             　 意义
----------------------------------
0                    终端默认设置
1                    高亮显示
22　　　　　　　　　　　非高亮显示
4                    使用下划线
24　　　　　　　　　　　去下划线
5                    闪烁
25　　　　　　　　　　　去闪烁
7                    反白显示
27　　　　　　　　　　　非反显
8                    不可见
28　　　　　　　　　　　可见
'''

from enum import Enum, unique
@unique
class LogLevel(Enum):
    HIGH_LIGHT = 0
    NORMAL = 1
    ERROR = 2
    TIPS = 3
    COMMON = 4
    INPUT = 5
    MARK = 6

def getStr(content, foreColor, backColor, showWay, withTail=True):

    cStr = "\033[" + str(showWay) + ";" + str(foreColor) + ";" + str(backColor) + "m"  + content
    if withTail:
        cStr += "\033[0m"
    return cStr

def getStrByLevel(content, level, withTail=True):

    foreColor = 37 # white 
    backColor = 40 # black
    showWay = 0

    if level == LogLevel.HIGH_LIGHT:
        foreColor = 35
        showWay = 1
    
    if level == LogLevel.ERROR:
        foreColor = 31

    if level == LogLevel.TIPS:
        foreColor = 36
        showWay = 1

    if level == LogLevel.INPUT:
        foreColor = 31
        showWay = 4

    if level == LogLevel.MARK:
        backColor = 47

    return getStr(content, foreColor, backColor, showWay, withTail)

def cPrint(content, level, withTail=True):

    print(getStrByLevel(content, level, withTail))
        