import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox
from matplotlib.patches import FancyBboxPatch
from scipy.integrate import solve_ivp
from matplotlib.patches import Rectangle

# Константы
g = 9.81  # ускорение свободного падения (м/с^2)
k_max = 1000  # Максимальная жесткость пружины до разрыва (примерное значение)
x_max = 1  # Максимальное удлинение пружины до разрыва (м)

# Начальные условия: позиция=0, скорость=0
x0 = 0
x_dot0 = 0

# Время симуляции и количество кадров в секунду
t_final = 10
fps = 30

# Флаг разрыва пружины
spring_broken = False

# Настройка графика
fig, ax = plt.subplots()
ax.set_facecolor('black')
ax.set_aspect('equal')
ax.set_xlim(-1, 1)
ax.set_ylim(-2, 2)
ax.set_xticks([])  # Убираем метки с оси X
ax.set_yticks(np.linspace(-2, 2, 5))

# Создание виджетов для ввода значений
def create_text_box(ax, label, initial):
    box = TextBox(ax, label, initial=initial)
    rect = Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor='white', edgecolor='black', linewidth=1.5)
    rect.set_clip_on(False)
    ax.add_patch(rect)
    return box

axbox_k = plt.axes([0.15, 0.05, 0.1, 0.075])
axbox_m = plt.axes([0.65, 0.05, 0.1, 0.075])
axbox_b = plt.axes([0.15, 0.15, 0.1, 0.075])
axbox_x_max = plt.axes([0.65, 0.15, 0.1, 0.075])

text_box_k = create_text_box(axbox_k, 'Stiffnes(N/m):', initial="100")
text_box_m = create_text_box(axbox_m, 'kg:', initial="1")
text_box_b = create_text_box(axbox_b, 'Damping coefficient(kg/s):', initial="0.25")
text_box_x_max = create_text_box(axbox_x_max, 'max length:', initial="1")

# Начальные значения
k = float(text_box_k.text)
m = float(text_box_m.text)
b = float(text_box_b.text)
x_max = float(text_box_x_max.text)

# Дифференциальные уравнения для системы пружина-масса
def spring_mass_ODE(t, y):
    x, x_dot = y
    return [x_dot, g - k * x / m - b * x_dot / m]

# Решение ОДУ
sol = solve_ivp(spring_mass_ODE, [0, t_final], [x0, x_dot0], t_eval=np.linspace(0, t_final, t_final * fps + 1))

# Вывод решения
x, x_dot = sol.y
t = sol.t

# Генерация координат пружины
def generate_spring(n, length, stretch_factor=2):
    data = np.zeros((2, n + 2))
    data[1, :] = np.linspace(0, -length * stretch_factor, n + 2)  # Увеличиваем расстояние между витками
    data[0, 1:-1:2] = 0.2
    data[0, 2:-1:2] = -0.2
    return data

# Начальная позиция пружины
n_points = 10  # Уменьшение количества витков для увеличения расстояния между витками
spring_length = 0.2  # Длина пружины в начальном состоянии, укороченная
data = generate_spring(n_points, spring_length, stretch_factor=4)  # Увеличение растяжения
spring = Line2D(data[0], data[1], color='white', linewidth=3)  # Сделать пружину тоньше

# Координаты линии фиксации (верхняя часть графика)
y_fixation = 1.8  # Определяем y_fixation
fixation_line = Line2D([-0.5, 0.5], [y_fixation, y_fixation], color='white', linewidth=4)  # Горизонтальная линия фиксации

# Начальное положение пружины (линии фиксации)
new_data = data.copy()
new_data[1, :] += y_fixation
spring.set_data(new_data[0], new_data[1])

# Квадрат в качестве груза (пружина и груз снизу)
square_width = 0.5
square_height = 0.5
initial_square_y = y_fixation - spring_length - square_height - 0.13
square = FancyBboxPatch(
    (-square_width / 2, initial_square_y - square_height),
    square_width, square_height,
    boxstyle="round,pad=0.04,rounding_size=0.1",  # Закругленные углы
    fc='blue', ec='black', linewidth=1
)

# Добавление пружины, квадрата и линии фиксации на график
ax.add_line(spring)
ax.add_patch(square)
ax.add_line(fixation_line)


# Анимация
def animate(i):
    global k, m, x_max, b, spring_broken
    if spring_broken:
        # Анимация падения груза при разрыве пружины
        y_square = square.get_y() - 0.1  # Падение груза
        if y_square <= -2:
            y_square = -2  # Ограничение падения
        square.set_y(y_square)
        return spring, square
    
    # Обновление положения груза
    y_square = initial_square_y - x[i] - square_height
    if y_square < -2:
        y_square = -2  # Ограничение падения
    square.set_y(y_square)
    
    # Обновление координат пружины
    new_data[1, :] = data[1, :] * (y_fixation - (y_square + square_height)) / (y_fixation - initial_square_y)
    new_data[1, :] += y_fixation
    spring.set_data(new_data[0], new_data[1])
    
    # Проверка на разрыв пружины
    if k * abs(x[i]) > k_max * x_max or abs(x[i]) > x_max:
        spring.set_color('red')
        spring_broken = True
        return spring, square
    
    spring.set_color('white')
    return spring, square

# Обновление параметров при изменении значений в текстовых полях
def submit_k(text):
    global k, spring_broken
    k = float(text)
    spring_broken = False
    update_solution()

def submit_m(text):
    global m, spring_broken
    m = float(text)
    spring_broken = False
    update_solution()

def submit_b(text):
    global b, spring_broken
    b = float(text)
    spring_broken = False
    update_solution()

def submit_x_max(text):
    global x_max, spring_broken
    x_max = float(text)
    spring_broken = False
    update_solution()

# Пересчет решения при изменении параметров
def update_solution():
    global sol, x, x_dot, t
    sol = solve_ivp(spring_mass_ODE, [0, t_final], [x0, x_dot0], t_eval=np.linspace(0, t_final, t_final * fps + 1))
    x, x_dot = sol.y
    t = sol.t

# Привязка функций к текстовым полям
text_box_k.on_submit(submit_k)
text_box_m.on_submit(submit_m)
text_box_b.on_submit(submit_b)
text_box_x_max.on_submit(submit_x_max)

# Создание анимации
ani = FuncAnimation(fig, animate, frames=len(t), interval=1000/fps, blit=True)

# Отображение графика
plt.show()
