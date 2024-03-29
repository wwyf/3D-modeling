# 报告

[TOC]

## 完成情况
本次项目进展顺利，完成情况良好，覆盖了我们一开始提出的五个预期目标。由于OpenGL属于比较底层的第三方库，开发难度较大，我们克服了线性代数知识的繁杂，以及API的稀少和局限。利用纯粹OpenGL，我们完成了键盘鼠标交互、三维空间里的视角转换、快捷键生成常用模型、三维模型的重合与碰撞检测，以及模型的格式化保存与加载。并且，在设计模式上，我们学习了一些专业的设计模式，借鉴许多优秀项目中的代码框架，使得优化后的代码框架结构清晰、解耦良好，易于未来扩展与多开发者合作。

未来我们考虑在此项目基础上，开发通过网络建模、多人协作的功能(如果暑假有时间)，期望实现如“石墨文档”的多人协作效果。对于这个功能的实现我们目前已有较为明确的思路：设置一个中心服务器用于处理来自多客户端的请求，程序运行于服务器节点，服务器节点内使用多线程(需要使用`thread`库)对多个客户端的请求进行监听，额外设置请求队列将所有到达的操作请求都挂入其中。所有的客户每进行一次操作就将操作发送到服务器，服务器对模型参数进行修改之后广播返回给所有客户端，实现同步更新。客户端与服务器之间使用`Socket`套接字进行通信，我们已具备套接字编程的基本能力，对实现多人协作具有信心。

## 项目效果展示
全局效果
![image 1](assets/1.png)
鼠标中键按下拖动可以平移整个坐标轴，鼠标右键按下拖动旋转整个视图
![image2](assets/2.png)
鼠标移动到视图的任意一个地方，键盘`S` `C` `F` `Z`分别可用于产生球体、立方体、球串儿和线段
![image3](assets/3.png)
选中物体，键盘按下`D`可以删除此物体
![image9](assets/9.png)
鼠标左键选中物体的时候，物体会高亮，且显示正方体边框，比如我们选中红色小球
![image4](assets/4.png)
鼠标左键按下可以拖动物体
![image5](assets/5.png)
键盘`↑`和`↓`可以放缩物体大小，`←`和`→`可用于变换物体颜色
![image6](assets/6.png)
键盘`1` `2` `3`用于将物体沿xyz轴进行压缩
键盘`4` `5` `6`用于将物体沿xyz轴进行拉伸
![image7](assets/7.png)
鼠标左线选中物体，接下来按下鼠标右键，可以对物体进行旋转
![image8](assets/8.png)
其次，按下`o`可以保存当前页面为我们定义的一种格式文件，按`L`可用于加载文件中的页面。
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

![](figure/2018-06-27-18-00-59.png)

在代码组织上，本次项目做到了较好的抽象和解耦。在下面的介绍中，我们会详细地讲解项目中的所有主要类，阐述主要类的接口和主要工作。最后我们会给出类与类之间的关系。

解耦的思想遍布整个项目。例如建模工具中的每个物体，它的基类都是Node类。Node类完成的是场景变换工作。Primitive类继承Node类，完成渲染工作。Scene类是场景类，包含了若干Primitive；Scene类的存在，使得程序可以同时维护多个场景，每个场景有自己独立的坐标系和物体，这给分屏带来了可能。Viewer类负责窗口的初始化和键鼠交互。每个类各司其职，又在一定程度上相互交互。

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

在3D建模中，一个及其重要的部分就是3D场景的建造。关于该场景的编写，我们编写了一个可扩展性极强的Scene类。

在场景类中,主要维护两个数据成员

| 成员变量名称  | 作用                                                   |
| ------------- | ------------------------------------------------------ |
| node_list     | 存放存储在该场景中的各个节点。                         |
| selected_node | 为该场景中被选中的节点，若没有被选中的节点，则为None。 |


该类的功能，可以分为以下几个大类，并且每一类都有一些具体的函数。

1. 渲染场景

    | 函数名称 | 函数功能         |
    | -------- | ---------------- |
    | render   | 遍历渲染所有节点 |

2. 对该场景内节点的管理

    | 函数名称    | 函数功能                 |
    | ----------- | ------------------------ |
    | place       | 在场景中增加预置模型     |
    | add_node    | 在场景中增加一个节点     |
    | remove_node | 删除场景中指定的一个节点 |

3. 对“选中节点”功能的支持

    | 函数名称 | 函数功能                                                   |
    | -------- | ---------------------------------------------------------- |
    | pick     | 在鼠标点击后，会调用这个函数，找到对应节点，从而”选中“节点 |

4. 对该场景选中节点的操作

    | 函数名称                                           | 函数功能           |
    | -------------------------------------------------- | ------------------ |
    | move_selected                                      | 移动所选节点       |
    | scalex_selected /scaley_selected / scalez_selected | 对节点进行缩放操作 |
    | rotatex_selected / rotatey_selected                | 对节点进行旋转操作 |
    | rotate_selected_color                              | 改变所选节点的颜色 |


注意到viewer中，`Scene`为场景的一个成员对象。Viewer通过调用`Scene`中提供的各个接口，对场景中的节点进行管理与操作。需要特别说明的是，该场景的职责重点在于节点`Node`对象的管理，以及将从`Viewer`类中得到的节点变换信息传达给指定的节点。对于节点本身的操作，并没有做过的干预，仅仅是调用节点`Node`的接口来实现节点的变换。

#### Node类及其派生子类

Node类作为场景中一个个3D对象的基类，定义了在场景中的一个节点必须具有的操作，如平移，旋转，以及最终渲染节点内容的实现。


![](figure/2018-06-27-18-59-14.png)

``` python
class Node(object):
    def __init__(self):
    def drawWireCuboid(self):
    def render(self):
    def render_self(self):
    def translate(self, x, y, z):
    def rotate_color(self, forwards):
    def scale(self, up):
    def scalex(self, up):
    def scaley(self, up):
    def scalez(self, up):
    def rotatex(self, angle):
    def rotatey(self, angle):
    def pick(self, start, direction, mat):
    def select(self, select=None):
```
Node类是场景中所有对象的基类。其私有变量中带存储着所有变换矩阵。包括与平移、旋转、缩放相关的矩阵。该类暴露了修改和设置这些矩阵的API。例如scale函数等。对一个元素的所有变换操作，都可以抽象成调用Node类实现的变换API。在Node类的render_self函数中，会自动把所有的变换矩阵相乘，对类的定点做坐标变换，然后再绘制图像。

| 函数名称                                           | 函数功能           |
| -------------------------------------------------- | ------------------ |
|\_\_init\_\_|类的构造函数，将所有变换矩阵初始化为单位阵|
|render|将所有变换矩阵相乘，得到复合变换，调用render_self做真正的渲染|
| render_self| 该基类中，不实现本函数。会抛出NotImplementedError异常 |
| translate| 平移API，平移到坐标x, y, z处 |
| rotate_color| 改变物体颜色。这是通过修改color_index实现的|
| scale / scalex / scaley / scalez| 等比例地、沿着x轴地、沿着y轴地、沿着z轴地缩放物体|
| rotatex / rotatey | 绕着x轴、绕着y轴旋转|
| pick | 返回鼠标的点击（射出的光线）是否击中（射穿）该物体|
| select| 每次调用时，翻转物体的“被选中”状态|

Node类提供了足够的抽象。更细致的物体类继承于Node类。
下面介绍的Primitive类通过call-list机制，真正实现了Node类中没有实现的render_self操作。
``` python
class Primitive(Node):
    def __init__(self):
        super(Primitive, self).__init__()
        self.call_list = None

    def render_self(self):
        glCallList(self.call_list)
```
首先在一个全局的init函数中，初始化所有的call-list，其中最重要的是基本集合图形的call-list，例如立方体和球体的call-list。在真正的渲染中，我们利用openGL提供的call-list机制，传入一个id，即可完成渲染操作。

例如在下述代码中，将self.call_list初始化为G_OBJ_CUBE.

``` python
class Cube(Primitive):
    """ Cube primitive """
    def __init__(self):
        super(Cube, self).__init__()
        self.call_list = G_OBJ_CUBE
```

为了定义组合图形，我们还定义了类HierarchicalNode,其具体定义见下
``` python
class HierarchicalNode(Node):
    def __init__(self):
        super(HierarchicalNode, self).__init__()
        self.child_nodes = []

    def render_self(self):
        for child in self.child_nodes:
            child.render()
    def rotate_color(self, forwards):
        for child in self.child_nodes:
            child.rotate_color(forwards)
```
self.child_nodes成员函数存储着一个列表。列表的每个元素都是一个Node的派生类。在render_self的实现中，该元素会递归地调用其所有部分的render_self.

#### Interaction类

Interaction类的最重要职责是：对用户交互产生的原始数据进行适当的处理，并调用Scene的接口，从而与后端进行联动。


``` python
class Interaction(object)
    def __init__(self):
    def register(self):
    def register_callback(self, name, func):
    def trigger(self, name, *args, **kwargs):
    def translate(self, x, y, z):
    def handle_mouse_button(self, button, mode, x, y):
    def handle_mouse_move(self, x, screen_y):
    def handle_keystroke(self, key, x, screen_y):
```

对于该类的接口功能说明，可以见下面的表格。


|接口名称|功能|
|-|-|
|register|将处理用户交互的函数注册到glut窗口管理程序上|
|register_callback|注册回调函数|
|trigger| 调用指定的回调函数|
|translate|移动相机|
|handle_mouse_button|处理鼠标按键动作|
|handle_mouse_move| 处理鼠标移动|
|handle_keystroke| 处理键盘事件|



### 类间关系解释

不同类之间的依赖关系一直是软件设计中一个需要重点关注的内容。在我们的设计中，不同类之间相互依赖的信息很少，耦合度低。同时，我们在低耦合的前提下还做到了高可扩展性，能够做到在不修改原有代码的情况下通过注册机制增加新的功能与效果。下面是对此特性的具体说明。

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

#### 实例说明


以调用放大功能为例子，在这一个情境下说明各个类之间关系。并以修改该放大功能，增加交互操作，来说明此种代码组织方式的可扩展性。

![](docs/figure/triggle-call-graph.png)

当我鼠标点击模块后，模块进入被选择状态。此时我按住鼠标并拖动鼠标，触发了我们已经在glut窗口管理程序注册好的回调函数`Interaction.hadle_mouse_move`,该函数截取一部分代码进行说明：

```python

def handle_mouse_move(self, x, screen_y):
    """ Called when the mouse is moved """
    xSize, ySize = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
    y = ySize - screen_y  # invert the y coordinate because OpenGL is inverted
    if self.pressed is not None:
        dx = x - self.mouse_loc[0]
        dy = y - self.mouse_loc[1]
        # ....省略一部分代码
        elif self.pressed == GLUT_LEFT_BUTTON:
            self.trigger('move', x, y)
        # ....省略一部分代码
        glutPostRedisplay()
    self.mouse_loc = (x, y)

```

通过这一段代码，可以看到`Interaction.handle_mouse_move`在发现鼠标左键被按下并移动的时候，会通过`trigger`函数调用已经在`Interaction`注册好的`move`函数，该函数通过字符串进行匹配，并找到对应的函数对象执行实际的操作。在这里，将回调函数与实际处理move操作的函数完全地解耦合，只要保持接口不变，该回调函数就不需要进行改动。

我们回到`viewer.py`，发现实际注册了`move`这个名字的函数为`Viewer.move`函数，因此此后该回调函数就会调用该函数。

```python
def move(self, x, y):
    """ Execute a move command on the scene. """
    start, direction = self.get_ray(x, y)
    self.scene.move_selected(start, direction, self.inverseModelView)
```

通过`Viewer`类中的转发，将这一个实际的操作转交给`Scene`类完成。由此，这个操作就可以完成了。

> 关于可扩展性的更进一步说明
> 
>注意到这里我们的回调函数是通过注册机制来确定调用关系的。在注册机制中，我们实现了一个名字可以注册多个函数，这也就意味着，如果我希望在函数`move`中再增加例如移动特效之类的效果，我们可以不用修改原有注册的函数，而是编写一个新的显示特效的函数，并且再注册到`move`这个名字中，这样子，我们的程序就可以通过增加代码而不是修改已有代码的方式实现功能的扩展，大大提高了程序的扩展性。

## 项目亮点

TODO:可能写得还不够

1. 可扩展性优良
    1. 我们借鉴了其他大型项目中的优秀设计模式，在初版完成后花了一些心思和时间重构了框架，重构后的代码框架结构清晰，类与类之间解耦良好，分工明确。
    1. 基于此框架的代码如添加模块，不需大幅调整原有代码，只需将新增模块与对应注册类接口进行衔接。尽量做到“只增不改”，使项目协作开发者能如同搭积木一样组装新功能。详情请阅回调函数与注册机制部分。
2. 用户交互友好
    1. 我们克服了原生OpenGL在交互上的短板，完成了一些复杂的交互逻辑代码(包括如何将二维的操作映射到三维空间里对应的变化)。我们设计的画板采用键盘和鼠标结合的交互方式，考虑到大多数用户在实际工作中使用鼠标的频率大于键盘的频率，开发时我们努力做到降低对键盘的依赖，与此同时优化鼠标的操作手势，用户易于上手，操控方便。


## 项目难点


1. OpenGL比较难用，接触到底层的知识，底层接口不好用
    1. OpenGL接口规范在计算机图形学中属于一个较为底层的接口，有接近硬件的部分(涉及到对显存的操作)。在此接口上，我们需要深刻理解OpenGL的工作原理，并使用OpenGL实现这样的一个简洁的3D建模工具并不容易。我们需要对计算机操作显存具有一些了解。
    1. 三维空间和二位空间的转化是另一个难点。我们复习了一个星期的线性代数才重新搞懂了怎么将三维平面正确投影到二位平面展示出来。二位平面上的鼠标操作映射到三维空间里对物体的实际操作，从远到近，设计是一个需要时间的过程。
在本项目中，需要大量用到线性代数的内容。首先每个物体最初处在模型坐标系中。我们利用矩阵变换的方式，在四维坐标系下，对物体作平移、拉伸、旋转等操作，将其变换到世界坐标系。在这一步中，我们需要注意矩阵相乘的顺序，矩阵的行列顺序。在世界坐标系中，我们需要调整摄像机的角度，增加透视效果等。这些也通过矩阵变换完成。需要对线性代数有一定深度的认识，对四维坐标有一定程度的了解，才能胜任这个代码工作。
3. 基于包围盒的与光线追踪的方法
    1. 当我们的鼠标点击屏幕上的一点时，我们该如何判断是否有模型是否被选中？这里的难点在于我们需要通过只有二维信息的鼠标屏幕坐标，去定位位于三维空间中的实际模型。我们的解决方法是包围盒算法与光线追踪。
    1. 光线追踪，顾名思义即是利用鼠标的位置，加上当时我们的视角信息，得到一个三维空间的向量，该向量就如同我们鼠标沿着我们的视角发出的一条光线。此后场景中的其他模型判断自己与该光线的距离，并判断自己是否被选中,并返回自身的距离，场景类再进行判断，选择唯一的最近的物体，设置为选中状态。
    1. 包围盒方法即是将一个物体抽象成一个盒子。因为如果需要对任意形状都需要精确地判断光线与物体边缘的距离，必须要十分复杂的实现才可以做到。在这里我们采取了将物体简化成一个包围盒的做法，由此避免了复杂模型与光线之间计算距离的问题。


## 附录一：小组信息

TODO:具体分工信息？

|队员名字|学号|具体工作|
|-|-|-|
|王永锋|16337237||
|颜彬|16337269|
|王锦鹏||
|王浩翔||



## 附录二：用到的库的相关说明

在本项目的开发中，我们使用了以下第三方库。

|库名称|库作用|
|-|-|
|pyopengl|python中的opengl接口函数库|
|numpy|线性代数数学库|
|OpenGL.GLUT| 窗口管理库|
|collections| python中额外的数据结构 |
|pyglm| 矩阵变换库，与OpenGL协同使用|
|pickle | 用来存放python对象到文件中|
