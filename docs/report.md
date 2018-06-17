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
        """ Initialize the viewer. """
        self.init_interface()
        self.init_opengl()
        self.init_scene()
        self.init_interaction()
        init_primitives()

    def init_interface(self):
        """ initialize the window and register the render function """

    def init_opengl(self):
        """ initialize the opengl settings to render the scene """
    def init_scene(self):
        """ initialize the scene object and initial scene """

    def init_interaction(self):
        """ init user interaction and callbacks """

    def main_loop(self):
        glutMainLoop()

    def render(self):
        """ The render pass for the scene """
    def delete(self):
    def init_view(self):
        """ initialize the projection matrix """
    def get_ray(self, x, y):
        """ Generate a ray beginning at the near plane, in the direction that the x, y coordinates are facing
            Consumes: x, y coordinates of mouse on screen
            Return: start, direction of the ray """
    def pick(self, x, y):
        """ Execute pick of an object. Selects an object in the scene. """

    def place(self, shape, x, y):
        """ Execute a placement of a new primitive into the scene. """

    def move(self, x, y):
        """ Execute a move command on the scene. """

    def rotate_color(self, forward):
        """ Rotate the color of the selected Node. Boolean 'forward' indicates direction of rotation. """

    def scale(self, up):
        """ Scale the selected Node. Boolean up indicates scaling larger."""
        """ right click. """
    def scalex(self, up):
        """ Scale the selected Node. Boolean up indicates scaling larger."""

    def scaley(self, up):
        """ Scale the selected Node. Boolean up indicates scaling larger."""

    def scalez(self, up):
        """ Scale the selected Node. Boolean up indicates scaling larger."""
    def load_new_scene(self, file_name='t.save'):
        """ Load a file and make a Scene object, then display it """
    def save_cur_scene(self, file_name='t.save'):
        """ Save current scene object to a file using pickle """
```



#### Scene类

在3D建模中，一个及其重要的部分就是3D场景的建造。关于该场景的编写，我们编写了一个可扩展性极强的Scene类。

##### 维护的数据结构

在场景类中,主要维护两个成员

| 成员变量名称  | 作用                                                   |
| ------------- | ------------------------------------------------------ |
| node_list     | 存放存储在该场景中的各个节点。                         |
| selected_node | 为该场景中被选中的节点，若没有被选中的节点，则为None。 |

##### 该类的功能

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


##### 一些说明

注意到viewer中，`Scene`为场景的一个成员对象。Viewer通过调用`Scene`中提供的各个接口，对场景中的节点进行管理与操作。需要特别说明的是，该场景的职责重点在于节点`Node`对象的管理，以及将从`Viewer`类中得到的节点变换信息传达给指定的节点。对于节点本身的操作，并没有做过的干预，仅仅是调用节点`Node`的接口来实现节点的变换。

#### Node类及其派生子类

Node类作为场景中一个个3D对象的基类，定义了在场景中的一个节点必须具有的操作，如平移，旋转，以及最终渲染节点内容的实现。

TODO:

#### Interaction类

TODO:


### 类间关系解释

interaction类 与 scene 类 之间的关系

Scene类与Viewer类之间的关系



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
	
