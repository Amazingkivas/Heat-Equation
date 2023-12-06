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


class FirstScreen(Screen):
    param1: int
    param2: int
    param3: float
    param4: float
    #plot_type: str

    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)

        super().__init__()
        self.param1 = 0
        self.param2 = 0
        self.param3 = 0
        self.param4 = 0
        #self.plot_type = "plus"

        with self.canvas:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        # The main layout of the application
        layout = BoxLayout(orientation='horizontal', padding=10, spacing=5)
        vertical_box = BoxLayout(orientation='vertical', spacing=5)

        # Fields for entering parameters
        parameter1 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='n')
        parameter2 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='m')
        parameter3 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='T')
        parameter4 = TextInput(multiline=False, size_hint=(None, None), size=(150, 30), hint_text='t')

        # Table for displaying data
        self.table_layout = GridLayout(cols=3, spacing=5, size_hint_y=None, row_default_height=40)
        self.table_layout.bind(minimum_height=self.table_layout.setter('height'))
        self.scroll_view = ScrollView(size_hint=(0.4, 1), do_scroll_y=True, do_scroll_x=False,
                                      scroll_type=['bars'], bar_width='15dp')
        self.scroll_view.add_widget(self.table_layout)

        # Adding a field for a graph
        self.fir, self.ax = plt.subplots()

        # Handler for the parameter input event
        def on_text(instance):
            try:
                self.param1 = int(parameter1.text)
                self.param2 = int(parameter2.text)
                self.param3 = float(parameter3.text)
                self.param4 = float(parameter4.text)
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

                x_values = []
                y_values = []
                dx = 1.0 / self.param1
                x = 0.0
                for n in range(0, self.param1 + 1):
                    x_values.append(x)
                    x += dx
                with open('OutputData.csv', 'r') as file:
                    reader = list(csv.reader(file, delimiter=';'))
                    for row in reader:
                        y_values.append(list(map(float, row)))

                dt = self.param3 / self.param2
                t = int(self.param4 / dt)
                print(t)
                print(len(y_values))
                self.ax.clear()
                # Build a graph
                self.ax.plot(x_values, y_values[t])
                self.ax.set_title("График распределения тепла вдоль стержня в момент времени t = " + str(self.param4))
                self.ax.set_xlabel('x')
                self.ax.set_ylabel('V')
                self.ax.grid(True)
                self.ax.figure.canvas.draw()

                # Build a table
                self.table_layout.clear_widgets()
                self.add_table_data(x_values, y_values[t])
            except ValueError:
                print("ERR")

        self.label1 = Label(text='Число разбиений по x: ', size_hint_y=None, height='30dp', halign='right')
        layout1 = BoxLayout(orientation='horizontal', size_hint=(0.4, None))
        self.label2 = Label(text='Число разбиений по t: ', size_hint_y=None, height='30dp', halign='right')
        layout2 = BoxLayout(orientation='horizontal', size_hint=(0.4, None))
        self.label3 = Label(text='Максимальное время: ', size_hint_y=None, height='30dp', halign='right')
        layout3 = BoxLayout(orientation='horizontal', size_hint=(0.4, None))
        self.label4 = Label(text='Построить график по слою: ', size_hint_y=None, height='30dp', halign='right')
        layout4 = BoxLayout(orientation='horizontal', size_hint=(0.4, None))

        # Process the press of the Enter key
        parameter1.bind(on_text_validate=on_text)
        parameter2.bind(on_text_validate=on_text)
        parameter3.bind(on_text_validate=on_text)
        parameter4.bind(on_text_validate=on_text)

        # Add widgets to the layout
        grid = GridLayout(cols=3)

        layout1.add_widget(self.label1)
        layout1.add_widget(parameter1)
        layout2.add_widget(self.label2)
        layout2.add_widget(parameter2)
        layout3.add_widget(self.label3)
        layout3.add_widget(parameter3)
        layout4.add_widget(self.label4)
        layout4.add_widget(parameter4)

        vertical_box.add_widget(layout1)
        vertical_box.add_widget(layout2)
        vertical_box.add_widget(layout3)
        vertical_box.add_widget(layout4)

        #vertical_box.add_widget(switch_button)
        vertical_box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        layout.add_widget(vertical_box)
        grid.add_widget(self.scroll_view)
        layout.add_widget(grid)
        self.add_widget(layout)

    def add_table_data(self, x_values, y_values):
        # Add data to the table
        for value in ['№ узла (i)', 'xi', 'Vi']:
            cell = Label(text=str(value), size_hint_x=None, width=150, color=[0, 0, 0, 1])
            cell.bind(size=self.draw_border)
            self.table_layout.add_widget(cell)
        num = -1
        for x, y in zip(x_values, y_values):
            num += 1
            for value in [num, round(x, len(str(self.param1))), y]:
                cell = Label(text=str(value), size_hint_x=None, width=150, color=[0, 0, 0, 1])
                cell.bind(size=self.draw_border)
                self.table_layout.add_widget(cell)

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
