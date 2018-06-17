# 报告


## 完成情况

1. 完成度很高！
2. 对未来的拓展有了明确的思路 

## 项目效果展示

### 实现效果
- 创建物体，删除物体
按下`S`、`D`和`Z`时分别在鼠标所指之处将自动产生球体、立方体和线段。
- 选择物体的时候会高光
- 可以对物体进行缩放，拉伸
- 可以物体进行旋转
- 可以对物体进行变色
- 对整个界面进行放大，进行平移，进行旋转 
- 保存场景
- 检测碰撞
- 自带阴影效果
2. 录屏


## 代码组织

### 关键类解释
#### Viewer类
Viewer类是整个项目的主类，负责各类初始化和整个模型的内容维护工作。
``` python
class Viewer(object):
    def __init__(self):
        self.init_interface()
        self.init_opengl()
        self.init_scene()
        self.init_interaction()
        init_primitives()
    def init_interface(self):
    def init_opengl(self):
    def init_scene(self):
    def init_interaction(self):
    def main_loop(self):
    def render(self):
    def delete(self):
    def init_view(self):
    def get_ray(self, x, y):
    def pick(self, x, y):
    def place(self, shape, x, y):
    def move(self, x, y):
    def rotate_color(self, forward):
    def scale(self, up):
    def scalex(self, up):
    def scaley(self, up):
    def scalez(self, up):
    def load_new_scene(self, file_name='t.save'):
    def save_cur_scene(self, file_name='t.save'):
```
| 函数名称    | 函数功能                 |
| ----------- | ------------------------ |
| \_\_init\_\_    | 初始化窗口、opengl设定，初始化场景（例如场景的网格和坐标轴）、初始化用户交互设置。    |
| init_interface | 利用glut产生窗口并初始化 |
|init_opengl|opengl初始化，例如产生光源和阴影，设置背景色等|
|init_scene|为场景绘制（水平面的）网格和坐标轴。在场景上放置若干个物体,作为初始化。|
|create_samle_scene|在场景上放若干个（默认的）小球|
|init_interaction|用于注册回调函数，处理诸如”添加物体“，”删除物体“，变换视角等|
|main_loop|opengl的阻塞死循环，将控制权完全交给Opengl|
|render  |主要指责是调用scene.render()，渲染出整个场景|
|init_view |摄像机初始化。设置摄像机位置、角度、透视效果等|
|get_ray| 光线追踪函数。当点击屏幕上某个点时，由于三维的图像被变换到二维的电脑屏幕上，鼠标点击的点可以对应三维世界中的一条直线。光线追踪函数用于确定该条直线。|
|pick| 鼠标左键单击可以选中物体。本函数用于确定（和修改）单击后被选中的物体。调用scene.pick()|
|place|按下某些按键后，向模型中放置物体时调用。调用scene.place()|
|move| 移动选中的物体。调用scene.rotate_selected()|
|rotate_color| 变换选中物体的颜色。调用scene.move_selected()|
|scale| 用于缩放选中物体的大小。调用scene.scale_selected()|
|mouse_drag| 鼠标拖拽时的回调函数。变换场景或旋转物体|
|scale*(*是x，y，z)|调用scene.scale*_selected(),用于在某个坐标轴一侧伸缩物体|
|load_new_scene|将当前场景的信息打包成文件|
|svae_cur_scene|将当前场景的信息从文件载入




#### Scene类

在3D建模中，一个及其重要的部分就是3D场景的建造。关于该场景的编写，我们编写了一个可扩展性极强的Scene类。该类的主要接口有

关于该类的功能，可以概括为以下几个部分

2. 对该场景内节点的管理
2. 对场景内某节点的选择及对节点的操作

Scene类与Viewer类之间的关系

```python
class Scene(object):
    def __init__(self)
    def add_node(self, node)
    def remove_node(self, node)
    
    def render(self)
    
    def pick(self, start, direction, mat)
    def move_selected(self, start, direction, inv_modelview)
    def place(self, shape, start, direction, inv_modelview)
    def rotate_selected_color(self, forwards)
    def scale_selected(self, up)
    def scalex_selected(self, up)
    def scaley_selected(self, up)
    def scalez_selected(self, up)
    def rotatex_selected(self, angle)
    def rotatey_selected(self, angle)
```



| 函数名称    | 函数功能                 |
| ----------- | ------------------------ |
| add_node    | 在场景中增加一个节点     |
| remove_node | 删除场景中指定的一个节点 |
|             |                          |
|             |                          |
|             |                          |
|             |                          |
|             |                          |
|             |                          |
|             |                          |


Scene



Interaction
Node
Primitive
User Define Object


### 类间关系解释

interaction类 与 scene 类 之间的关系





#### 函数注册机制
`Iteraction`类负责处理与用户交互有关的操作。例如键盘按下，鼠标左键、中键、右键的点击，鼠标的拖动等。由于用户交互无处不在，且用户的操作可能会涉及到整个程序绝大部分状态（例如变量等），如何解耦成为了极其关键的设计问题。

在`Interaction`类中，所有“需要被Interaction类访问“的函数，需要主动向其注册。在注册后，这些函数成为用户操作的回调函数。
``` python
class Interaction(object):
    ...
    def register(self):
        """ register callbacks with glut """
        glutMouseFunc(self.handle_mouse_button)
        glutMotionFunc(self.handle_mouse_move)
        glutKeyboardFunc(self.handle_keystroke)
        glutSpecialFunc(self.handle_keystroke)

    def register_callback(self, name, func):
        """ registers a callback for a certain event """
        self.callbacks[name].append(func)
```
`register`函数向glut注册了常用的回调函数，例如鼠标回调和键盘回调等。

`register_callback`函数供外部代码调用。外部代码在调用时，传递一个函数名（字符串）和函数引用。Interaction类会维护一个字典，将函数名（字符串）映射到函数的引用上。

``` python
...
    def trigger(self, name, *args, **kwargs):
        """ calls a callback, forwards the args """
        for func in self.callbacks[name]:
            func(*args, **kwargs)
```
回调是通过`trigger`函数做到的。trigger函数接收一个函数名，和`*args`, `**kwargs`这两个通用参数。通过在字典中搜索函数名，代码会得到系列函数的列表，对这个列表中的每个函数，传递通用参数。

如此即可做到，在事件发生时，每个注册了的函数都能得到响应，且参数能被正确地传递。
``` python
...
    def init_interaction(self):
        """ init user interaction and callbacks """
        self.interaction = Interaction()
        self.interaction.register_callback('pick', self.pick)
        self.interaction.register_callback('move', self.move)
        self.interaction.register_callback('place', self.place)
        self.interaction.register_callback('rotate_color', self.rotate_color)
        self.interaction.register_callback('scale', self.scale)
        self.interaction.register_callback('delete', self.delete)
        self.interaction.register_callback('scalex', self.scalex)
        self.interaction.register_callback('scaley', self.scaley)
        self.interaction.register_callback('scalez', self.scalez)
        self.interaction.register_callback('save_cur_scene', self.save_cur_scene)
        self.interaction.register_callback('load_new_scene', self.load_new_scene)
        self.interaction.register_callback('mouse_drag', self.mouse_drag)
```
以上是经过注册的函数。其中`move`负责在鼠标左键拖拽时，移动场景。`pick`负责在鼠标点击时，选中物体。`place`负责放置物体。`rotate_color`负责在方向左右键按下时，修改颜色。`scale`负责在方向上下键按下时修改大小。`delete`负责删除物体。`scale*`负责沿着x, y, z三个轴中的一个，伸缩物体。`save_cur_scene`和`load_new_scene`负责保存目前的场景和载入场景。

交互设计的代码极其繁杂，Iteraction需要能访问到绝大多数的变量。在平常（但低效）的实现中，我们可以把所有变量都设置为全局变量，Interaction类通过访问全局变量的方式修改整个程序的状态。但此处的注册、回调机制，允许大部分变量以局部变量的形式存在，只需要变量的作用域处于注册函数中即可。

#### 高度解耦
#### 

## 项目亮点
	代码组织就很好，可扩展性优良 
	用户交互 
## 项目难点
	用OpenGL很难，接触到底层的知识，对于线性代数的要求很高
	基于包围盒的算法实现比较复杂
杂乱的最后一面
	项目分工
	时间轴？ 
	
