# ui界面设计介绍

首先呢，ui界面一共分为三个部分，共有三个界面来实现这三个部分的功能： 欢迎页面， 信息采集页面， 数据处理界面

主要运用 QT-designer 对界面进行便捷的设计，设计完成后使用 layout对界面进行一个整体的布局，使界面能够自由调节大小，内容可以自适应界面

QT-designer的具体使用教程大家可以去看B站上的：https://www.bilibili.com/video/BV1cJ411R7bP/?share_source=copy_web&vd_source=63e1419d56ed8f448e047063033d5f7a

QT-designer中控件的使用可以参考：https://blog.csdn.net/weixin_42964413/article/details/114387591?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522169795965216800213024656%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fall.%2522%257D&request_id=169795965216800213024656&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~first_rank_ecpm_v1~rank_v31_ecpm-4-114387591-null-null.142^v96^pc_search_result_base7&utm_term=qtdesigner%E4%B8%ADText%20Edit%E4%BB%8B%E7%BB%8D&spm=1018.2226.3001.4187

## 欢迎界面

这个界面有主要由一个文本编辑框和三个按钮构成，下面三个按钮点击之后可以通过槽函数进入不同的界面

三个按钮为左侧菜单栏中buttons 里的Push Button

最上面的标题可以用两个文本编辑的工具： Input Widgets 里的Line Edit 或 Text Edit；

Line Edit：单行文本(即：无论输入多少的文字，均放在同一行)，其中设置文本为只读可以在QLineEdit属性中找到readOnly进行设定，文本居中等属性也可以在这里面设置

Text Edit：多行文本框(可用在输入)，在文字显示不完全时，框的最右侧会有一个滚动条，这个滚动条可以通过属性栏中QAbstractScrollArea中的verticalScrollBarPolicy和horizontalScrollBarPolicy选择打开或关闭

最后三个部分设置好之后，首先设置一下空间的最小大小，然后选中全部，鼠标右击之后进行布局，最后再进行全局布局，使窗口可以自适应大小

设置背景透明度：https://blog.csdn.net/wu9797/article/details/78722396

## 信息采集页面

这个画面主要由左右两部分组成，左边为一个单行文本框和一个表格控件，右边由两个功能按钮和一个显示摄像头的画面(OpenGL weights)组成

左边：文本框与列表为垂直布局，列表中可以显示保存下来的图片的信息，双击即可查看图片，

中间为一条竖线，可以在Display Wights中的Vertical Line寻找到使用

右边： 下方的两个按钮分别负责打开摄像头和采集图片，摄像头开启之后可以在上面显示实时的画面，图片采集后会在左边列表中显示对应的信息，

**两个按钮为水平布局，按钮与上面的画面是垂直布局，这个画面中的三个部分要使用分裂器水平布局(使得三个部分可以在显示框内随时调整大小)**

## 数据处理界面

这个画面与信息采集界面相似，只需要对右边画面调整一下

左边：文本框与列表为垂直布局，列表中可以显示保存下来的图片的信息，双击即可查看图片，

中间为一条竖线，可以在Display Wights中的Vertical Line寻找到使用

右边： 下方一个按钮点击后调用模型对图片进行处理，上方是label控件，可以对目标图片和处理后的图片显示，

## 图片编辑界面

这个界面可以分为三个区域：左侧图片信息展示区，右侧上方labels图片展示区域，右侧下方功能区域

左侧： 使用控件 List Weight展示文件夹下图片的信息，双击之后可以把图片展示到右侧上方的labels中；

右侧上方： 展示所选择的图片

右侧下方： 设置了可以对图片进行编辑的七个功能，画笔和橡皮(Check Box控件)，画笔粗细设定(Spin Box控件), 画笔颜色(Combo Box控件)，三个按钮(分别实现了清空画板，裁剪图片，保存图片三个功能)

**在对界面整体设计完成后，要想界面可以自适应大小，需要对界面中所有的控件进行布局，在这里有一个技巧：就是首先把窗口设置为最小的大小，然后调整里面的控件。**  
**调整结束之后，设定每一个控件的最小大小，而后再去设置垂直或者水平布局，设置控件的比例，这样会省很多事情**

## QT-designer的安装

QT-designer的安装参考：https://zhuanlan.zhihu.com/p/469526603