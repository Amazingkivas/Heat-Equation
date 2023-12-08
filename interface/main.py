from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import csv
import subprocess
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class FirstScreen(Screen):
    param1: int
    param2: int
    param3: float
    param4: float
    param5: float
    x_values: list
    y_values: list
    t_values: list
    t: int
    plot_type: str

    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)

        super().__init__()
        self.param1 = 0
        self.param2 = 0
        self.param3 = 0
        self.param4 = 0
        self.param5 = 0
        self.x_values = []
        self.y_values = []
        self.t_values = []
        self.t = 0
        self.plot_type = "_"

        with self.canvas:
            Color(0.15, 0.15, 0.15, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # The main layout of the application
        layout = BoxLayout(orientation='horizontal', padding=10, spacing=5)
        self.vertical_box = BoxLayout(orientation='vertical', padding=10, spacing=20)

        # Fields for entering parameters
        self.parameter1 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='n')
        self.parameter2 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='m')
        self.parameter3 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='T')
        self.parameter4 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='t')
        self.parameter5 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='x')

        # Table for displaying data
        self.table_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, row_default_height=40)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))
        self.scroll_view = ScrollView(size_hint=(0.4, 1), do_scroll_y=True, do_scroll_x=False,
                                      scroll_type=['bars'], bar_width='15dp')
        self.scroll_view.add_widget(self.table_layout)


        # Строим трехмерный график
        self.fig = plt.gcf()
        self.bx = self.fig.add_subplot(111, projection='3d')

        self.plt_box = BoxLayout(orientation='vertical', padding=10, spacing=5, size_hint=(None, None),
                            size=(800, 650))

        widg_plt = FigureCanvasKivyAgg(self.fig)
        self.plt_box.add_widget(widg_plt)


        # Adding a field for a graph
        self.fir, self.ax = plt.subplots()

        self.plt_box_1 = BoxLayout(orientation='vertical', padding=10, spacing=5, size_hint=(None, None),
                            size=(800, 650))

        self.plt_1 = FigureCanvasKivyAgg(plt.gcf())

        self.plt_box_1.add_widget(self.plt_1)

        # Buttons for a graphs
        grid2 = GridLayout(cols=1)

        self.button0 = Button(text='Ввести параметры', size_hint=(None, None), size=(550, 40))
        self.button0.bind(on_press=self.set_params)
        grid2.add_widget(self.button0)

        self.button2 = Button(text='График изменения распределения температуры на всём стержне', size_hint=(None, None),
                              size=(550, 40))
        self.button2.bind(on_press=self.plot_3d_graph)
        grid2.add_widget(self.button2)

        self.button1 = Button(text='График и таблица распределения температуры при фиксированном t', size_hint=(None, None),
                              size=(550, 40))
        self.button1.bind(on_press=self.plot_graph_x)
        grid2.add_widget(self.button1)

        self.button3 = Button(text='График и таблица изменения температуры при фиксированном x', size_hint=(None, None),
                              size=(550, 40))
        self.button3.bind(on_press=self.plot_graph_t)
        grid2.add_widget(self.button3)

        self.label1 = Label(text='Число разбиений по x: ', size_hint_y=None, height='30dp', halign='right')
        layout1 = BoxLayout(orientation='horizontal', size_hint=(0.4, 0.1))
        self.label2 = Label(text='Число разбиений по t: ', size_hint_y=None, height='30dp', halign='right')
        layout2 = BoxLayout(orientation='horizontal', size_hint=(0.4, 0.1))
        self.label3 = Label(text='Максимальное время: ', size_hint_y=None, height='30dp', halign='right')
        layout3 = BoxLayout(orientation='horizontal', size_hint=(0.4, 0.1))
        self.label4 = Label(text='Фиксированное время: ', size_hint_y=None, height='30dp', halign='right')
        layout4 = BoxLayout(orientation='horizontal', size_hint=(0.4, 0.1))
        self.label5 = Label(text='Фиксированная координата: ', size_hint_y=None, height='30dp', halign='right')
        layout5 = BoxLayout(orientation='horizontal', size_hint=(0.4, 0.1))

        # Add widgets to the layout
        grid = GridLayout(cols=3)

        layout1.add_widget(self.label1)
        layout1.add_widget(self.parameter1)
        layout2.add_widget(self.label2)
        layout2.add_widget(self.parameter2)
        layout3.add_widget(self.label3)
        layout3.add_widget(self.parameter3)
        layout4.add_widget(self.label4)
        layout4.add_widget(self.parameter4)
        layout5.add_widget(self.label5)
        layout5.add_widget(self.parameter5)

        self.vertical_box.add_widget(layout1)
        self.vertical_box.add_widget(layout2)
        self.vertical_box.add_widget(layout3)
        self.vertical_box.add_widget(layout4)
        self.vertical_box.add_widget(layout5)
        self.vertical_box.add_widget(grid2)
        #vertical_box.add_widget(plt_box_1)
        self.vertical_box.add_widget(self.plt_box)
        #
        #plt_box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        #grid2.add_widget(plt_box)

        #vertical_box.add_widget(switch_button)

        layout.add_widget(self.vertical_box)
        grid.add_widget(self.scroll_view)
        layout.add_widget(grid)
        self.add_widget(layout)

    def set_params(self, instance):
        self.param1 = int(self.parameter1.text)
        self.param2 = int(self.parameter2.text)
        self.param3 = float(self.parameter3.text)
        self.param4 = float(self.parameter4.text)
        self.param5 = float(self.parameter5.text)
        with open("Source.txt", "w") as file:
            file.write(str(self.param1) + '\n')
            file.write(str(self.param2) + '\n')
            file.write(str(self.param3))

        cpp_executable = "Release/sample.exe"
        args = [cpp_executable]
        try:
            subprocess.run(args, check=True)
        except subprocess.CalledProcessError:
            print("Error when starting a C++ project")
        except FileNotFoundError:
            print("sample.exe not found")

        self.x_values.clear()
        self.y_values.clear()
        self.t_values.clear()
        dx = 1.0 / self.param1
        x = 0.0
        mdt = self.param3 / self.param2
        mt = 0.0
        for n in range(0, self.param1 + 1):
            self.x_values.append(x)
            x += dx
        for m in range(0, self.param2 + 1):
            self.t_values.append(mt)
            mt += mdt
        with open('OutputData.csv', 'r') as file:
            reader = list(csv.reader(file, delimiter=';'))
            for row in reader:
                self.y_values.append(list(map(float, row)))

        self.dt = self.param3 / self.param2
        self.t = int(self.param4 / self.dt)

        # Build a table
        # self.table_layout.clear_widgets()
        # self.add_table_data(self.x_values, self.y_values[self.t])

    def plot_graph_x(self, instance):
        flag = True
        if self.plt_box in self.vertical_box.children:
            self.vertical_box.remove_widget(self.plt_box)
            if self.plot_type == "x":
                flag = False

        self.ax.clear()
        # Build a graph
        self.ax.plot(self.x_values, self.y_values[self.t])
        self.ax.set_title("График распределения тепла вдоль стержня в момент времени t = " + str(self.param4))
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('V')
        self.ax.grid(True)
        self.ax.figure.canvas.draw()

        if self.plt_box_1 not in self.vertical_box.children:
            self.vertical_box.add_widget(self.plt_box_1)

        if flag:
            self.table_layout.clear_widgets()
            for value in ['№ узла (i)', 'xi', 'Vi']:
                cell = Label(text=str(value), size_hint_x=None, width=150, color=[0, 0, 0, 1])
                cell.bind(size=self.draw_border)
                self.table_layout.add_widget(cell)
            num = -1
            for x, y in zip(self.x_values, self.y_values[self.t]):
                num += 1
                for value in [num, round(x, len(str(self.param1))), y]:
                    cell = Label(text=str(value), size_hint_x=None, width=150, color=[0, 0, 0, 1])
                    cell.bind(size=self.draw_border)
                    self.table_layout.add_widget(cell)

        self.plot_type = "x"

    def plot_graph_t(self, instance):
        flag = True
        if self.plt_box in self.vertical_box.children:
            self.vertical_box.remove_widget(self.plt_box)
            if self.plot_type == "t":
                flag = False

        self.ax.clear()
        # Build a graph
        v_values = []
        dx = 1.0 / self.param1
        x = int(self.param5 / dx)
        print(x)
        for lst in self.y_values:
            v_values.append(lst[x])
        self.ax.plot(self.t_values, v_values)
        self.ax.set_title("График изменения температуры в узле x = " + str(self.param5))
        self.ax.set_xlabel('t')
        self.ax.set_ylabel('V')
        self.ax.grid(True)
        self.ax.figure.canvas.draw()

        if self.plt_box_1 not in self.vertical_box.children:
            self.vertical_box.add_widget(self.plt_box_1)

        if flag:
            self.table_layout.clear_widgets()
            for value in ['№ узла (j)', 'tj', 'Vj']:
                cell = Label(text=str(value), size_hint_x=None, width=150, color=[0, 0, 0, 1])
                cell.bind(size=self.draw_border)
                self.table_layout.add_widget(cell)
            num = -1
            for x, y in zip(self.t_values, v_values):
                num += 1
                for value in [num, round(x, len(str(self.param1))), y]:
                    cell = Label(text=str(value), size_hint_x=None, width=150, color=[0, 0, 0, 1])
                    cell.bind(size=self.draw_border)
                    self.table_layout.add_widget(cell)

        self.plot_type = "t"

    def plot_3d_graph(self, instance):
        self.vertical_box.remove_widget(self.plt_box_1)
        self.bx.clear()

        #x_vals = self.x_values[::-1]

        x = np.array(self.x_values)
        y = np.array(self.t_values)
        z = np.array(self.y_values)

        X, T = np.meshgrid(x, y)

        self.bx.set_xlabel('x')
        self.bx.set_ylabel('t')
        self.bx.set_zlabel('V')
        self.bx.set_title('График изменения температуры на стержне')

        # Строим поверхность
        self.bx.plot_surface(X, T, z, cmap='viridis')
        if self.plt_box not in self.vertical_box.children:
            self.vertical_box.add_widget(self.plt_box)




    # def add_table_data(self, x_values, y_values):
    #     # Add data to the table
    #     for value in ['№ узла (i)', 'xi', 'Vi']:
    #         cell = Label(text=str(value), size_hint_x=None, width=150, color=[0, 0, 0, 1])
    #         cell.bind(size=self.draw_border)
    #         self.table_layout.add_widget(cell)
    #     num = -1
    #     for x, y in zip(x_values, y_values):
    #         num += 1
    #         for value in [num, round(x, len(str(self.param1))), y]:
    #             cell = Label(text=str(value), size_hint_x=None, width=150, color=[0, 0, 0, 1])
    #             cell.bind(size=self.draw_border)
    #             self.table_layout.add_widget(cell)

    def draw_border(self, instance, size):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(1, 1, 1, 1)
            instance.rect = Rectangle(size=instance.size, pos=instance.pos)
        instance.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class ParameterInputApp(App):
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def build(self):
        screen_manager = ScreenManager()
        first_screen = FirstScreen(name='first')
        screen_manager.add_widget(first_screen)
        return screen_manager


if __name__ == '__main__':
    ParameterInputApp().run()
