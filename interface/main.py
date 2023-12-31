from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

import csv
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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

        with self.canvas:
            Color(0.15, 0.15, 0.15, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # The main layout of the application
        self.layout = BoxLayout(orientation='horizontal', padding=20, spacing=1)
        self.vertical_box = BoxLayout(orientation='vertical', padding=10, spacing=25)

        # Fields for entering parameters
        self.parameter1 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='n')
        self.parameter2 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='m')
        self.parameter3 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='T')
        self.parameter4 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='t')
        self.parameter5 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='x')

        # Table for displaying data
        self.tab = BoxLayout(orientation='vertical')

        # Build 3D plot
        self.fig = plt.gcf()
        self.bx = self.fig.add_subplot(111, projection='3d')
        self.plt_box = BoxLayout(orientation='vertical', padding=10, spacing=5, size_hint=(None, None),
                            size=(800, 610))
        widget_plt = FigureCanvasKivyAgg(self.fig)
        self.plt_box.add_widget(widget_plt)

        # Add a field for a graph
        self.fir, self.ax = plt.subplots()
        self.plt_box_1 = BoxLayout(orientation='vertical', padding=10, spacing=5, size_hint=(None, None),
                            size=(800, 610))
        self.plt_1 = FigureCanvasKivyAgg(plt.gcf())
        self.plt_box_1.add_widget(self.plt_1)

        # Buttons for a graphs
        grid2 = GridLayout(cols=1)
        self.button0 = Button(text='Ввести параметры', size_hint=(None, None), size=(500, 40))
        self.button0.bind(on_press=self.set_params)
        grid2.add_widget(self.button0)

        self.button2 = Button(text='График изменения распределения температуры на всём стержне', size_hint=(None, None),
                              size=(500, 40))
        self.button2.bind(on_press=self.plot_3d_graph)
        grid2.add_widget(self.button2)

        self.button1 = Button(text='График распределения температуры при фиксированном t', size_hint=(None, None),
                              size=(500, 40))
        self.button1.bind(on_press=self.plot_graph_x)
        grid2.add_widget(self.button1)

        self.button3 = Button(text='График изменения температуры при фиксированном x', size_hint=(None, None),
                              size=(500, 40))
        self.button3.bind(on_press=self.plot_graph_t)
        grid2.add_widget(self.button3)

        self.label1 = Label(text='Число разбиений по x: ', size_hint_y=None, height='30dp', halign='right')
        layout1 = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1))
        self.label2 = Label(text='Число разбиений по t: ', size_hint_y=None, height='30dp', halign='right')
        layout2 = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1))
        self.label3 = Label(text='Максимальное время: ', size_hint_y=None, height='30dp', halign='right')
        layout3 = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1))
        self.label4 = Label(text='Фиксированное время: ', size_hint_y=None, height='30dp', halign='right')
        layout4 = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1))
        self.label5 = Label(text='Фиксированная координата (0, 1): ', size_hint_y=None, height='30dp', halign='right')
        layout5 = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1))

        self.popup = Popup(
            title='Ошибка: некорректные параметры',
            size_hint=(None, None),
            size=(400, 200),
            background='atlas://data/images/defaulttheme/button',
            separator_color=(0, 0, 1, 1)
        )
        button_box = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(375, 100))

        # Creating an OK button to close the window
        ok_button = Button(text="Поменять параметры")
        ok_button.bind(on_press=self.popup.dismiss)
        button_box.add_widget(ok_button)

        # Positioning the container with buttons
        self.popup.bind(size=lambda instance, value: setattr(button_box, 'pos', (0.5, self.popup.y)))
        self.popup.add_widget(button_box)

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
        self.vertical_box.add_widget(self.plt_box)
        self.layout.add_widget(self.vertical_box)
        self.layout.add_widget(self.tab)
        self.add_widget(self.layout)

    def set_params(self, instance):
        try:
            self.param1 = int(self.parameter1.text)
            self.param2 = int(self.parameter2.text)
            self.param3 = float(self.parameter3.text)
            self.param4 = float(self.parameter4.text)
            self.param5 = float(self.parameter5.text)
        except ValueError:
            self.popup.open()

        if (self.param1 <= 0 or self.param2 <= 0 or self.param4 < 0 or self.param3 <= 0 or self.param5 < 0 or
            self.param4 > self.param3 or self.param5 > 1.0 or
            not isinstance(self.param1, int) or not isinstance(self.param2, (int, float)) or
            not isinstance(self.param3, (int, float)) or not isinstance(self.param4, (int, float)) or
            not isinstance(self.param5, (int, float))):
            self.popup.open()
            return

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
                if row == reader[0]:
                    continue
                self.y_values.append(list(map(float, row)))

        dt = self.param3 / self.param2
        self.t = int(self.param4 / dt)

        self.tab.clear_widgets()
        label = MDLabel(
            text='''Таблица изменения распределения температуры вдоль стержня:\n
            i - индексы узлов сетки, x(i) - соответствующая координата узла
            j - номера слоёв, t(j) - соответствующий момент времени
            ''',
            # Text alignment in the center
            size_hint=(1, 0.2),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.45, 'center_y': 0.5},
        )
        self.tab.add_widget(label)

        df = pd.read_csv('OutputData.csv', sep=';', dtype=str)

        for i, column in enumerate(df.columns):
            df.rename(columns={str(i): str(round(1.0 / float(self.param1) * float(i), len(str(self.param1)))) +
                      '\n--‐----------------------\n ' + str(i)}, inplace=True)

        column_label_1 = [str(col) for col in range(0, len(df))]

        column_label_2 = [str(col * self.param3/self.param2) for col in range(0, len(df))]
        for index in range(0, len(df)):
            if float(column_label_2[index]) % 1 == 0:
                column_label_2[index] = str(int(float(column_label_2[index])))

        df.insert(0, '     x(i)\n-------------------------\n  j \ i', column_label_1)
        df.insert(0, ' \n------------------------\n t(j)', column_label_2)

        # Create table
        table = MDDataTable(
            use_pagination=True,
            size_hint=(1, 1),
            rows_num=10,
            pos_hint={'center_x': 0.45, 'center_y': 0.5},
            column_data=[(column, dp(30)) for column in df.columns],
            row_data=df.values.tolist()  # Table data
        )
        self.tab.add_widget(table)

    def plot_graph_x(self, instance):
        if self.plt_box in self.vertical_box.children:
            self.vertical_box.remove_widget(self.plt_box)

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


    def plot_graph_t(self, instance):
        if self.plt_box in self.vertical_box.children:
            self.vertical_box.remove_widget(self.plt_box)

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


    def plot_3d_graph(self, instance):
        self.vertical_box.remove_widget(self.plt_box_1)
        self.bx.clear()

        x = np.array(self.x_values)
        y = np.array(self.t_values)
        z = np.array(self.y_values)

        X, T = np.meshgrid(x, y)

        self.bx.set_xlabel('x')
        self.bx.set_ylabel('t')
        self.bx.set_zlabel('V')
        self.bx.set_title('График изменения температуры на стержне')

        # Build plot
        self.bx.plot_surface(X, T, z, cmap='viridis')
        if self.plt_box not in self.vertical_box.children:
            self.vertical_box.add_widget(self.plt_box)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


class ParameterInputApp(MDApp):
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def build(self):
        screen_manager = ScreenManager()
        self.title = "Уравнение теплопроводности Борисов С.А. 3821Б1ПМоп3 команда 2"
        first_screen = FirstScreen(name='first')
        screen_manager.add_widget(first_screen)
        return screen_manager


if __name__ == '__main__':
    ParameterInputApp().run()
