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

在3D建模中，一个及其重要的部分就是3D场景的建造。关于该场景的编写，我们编写了一个可扩展性极强的Scene类。该类的主要接口有

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
    def scale_selected(self, up):##################v
    def scalex_selected(self, up):
    def scaley_selected(self, up):
    def scalez_selected(self, up):
    def rotatex_selected(self, angle):
    def rotatey_selected(self, angle):
```




Scene



Interaction
Node
Primitive
User Define Object


### 类间关系解释

interaction类 与 scene 类 之间的关系





#### 函数注册机制
高度解耦的用户交互模块。

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
	
