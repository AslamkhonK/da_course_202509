import tkinter as tk
import random

# Настройки окна
WIDTH = 1200
HEIGHT = 800
FONT_SIZE = 15
UPDATE_DELAY = 50  # миллисекунды
TRAIL_LENGTH = 10  # длина следа

# Создание окна
root = tk.Tk()
root.title("Matrix")
root.configure(bg='black')
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='black', highlightthickness=0)
canvas.pack()

# Количество столбцов
columns = WIDTH // FONT_SIZE

# Позиции для каждого столбца
positions = [random.randint(-HEIGHT // FONT_SIZE, 0) for _ in range(columns)]

# Цвет кислотно-зелёный
COLOR = "#00FF00"

# Для хранения символов следа
trails = [[] for _ in range(columns)]

def draw_matrix():
    canvas.delete("all")
    for i, pos in enumerate(positions):
        # Создаем новый символ
        char = chr(random.randint(33, 126))  # ASCII символы

        # Добавляем символ в след столбца
        trails[i].append(pos)
        if len(trails[i]) > TRAIL_LENGTH:
            trails[i].pop(0)

        # Рисуем весь след
        for j, y_pos in enumerate(trails[i]):
            x = i * FONT_SIZE
            y = y_pos * FONT_SIZE
            brightness = int(255 * (j + 1) / TRAIL_LENGTH)
            color = f'#{0:02X}{brightness:02X}{0:02X}'  # зелёный с градиентом яркости
            canvas.create_text(x, y, text=char, fill=color, font=("Consolas", FONT_SIZE))

        # Обновляем позицию столбца
        positions[i] += 1
        if positions[i] * FONT_SIZE > HEIGHT:
            positions[i] = random.randin
