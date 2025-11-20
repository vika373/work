import numpy as np
import matplotlib.pyplot as plt

# Генерация данных
def generate_data(n_samples=100):
    np.random.seed(42)
    X = np.random.randn(n_samples, 2)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)  # Класс 1 если x+y > 0, иначе 0
    return X, y

# Функция активации (ступенчатая функция)
def step(x):
    return np.where(x >= 0, 1, 0)

# Перцептрон
class Perceptron:
    def __init__(self, input_size, learning_rate=0.1):
        self.weights = np.zeros(input_size + 1)  # +1 для смещения (bias)
        self.lr = learning_rate

    def predict(self, x):
        x = np.insert(x, 0, 1)  # Добавляем bias
        activation = np.dot(self.weights, x)
        return step(activation)

    def train(self, X, y, epochs=10):
        for epoch in range(epochs):
            for xi, target in zip(X, y):
                xi_aug = np.insert(xi, 0, 1)  # Добавляем bias
                prediction = self.predict(xi)
                error = target - prediction
                self.weights += self.lr * error * xi_aug

# Обучение и тест
X, y = generate_data(200)
model = Perceptron(input_size=2)
model.train(X, y, epochs=20)

# Предсказания для обучающих данных
preds = np.array([model.predict(x) for x in X])

# Ввод нескольких точек пользователем
print("Введите несколько точек C через пробел, каждую в формате x,y (например: 1.0,2.0 0.5,-1.2)")
print("Или оставьте пустую строку для случайных точек.")
user_input = input("Введите точки: ").strip()

if user_input:
    points_str = user_input.split()
    points = []
    for p_str in points_str:
        try:
            x_str, y_str = p_str.split(',')
            x_val = float(x_str)
            y_val = float(y_str)
            points.append([x_val, y_val])
        except Exception as e:
            print(f"Ошибка при разборе точки '{p_str}': {e}")
    if not points:
        print("Ни одна точка не была корректно введена. Создадим одну случайную точку.")
        points = [np.random.uniform(low=X.min(), high=X.max(), size=2)]
else:
    # Если пустой ввод — создаём 3 случайных точки
    points = [np.random.uniform(low=X.min(), high=X.max(), size=2) for _ in range(3)]
    print("Созданы 3 случайные точки:", points)

points = np.array(points)

# Классификация введённых точек
points_preds = np.array([model.predict(p) for p in points])

# Цвета для классов
class_colors = ['blue', 'red']

for i, (pt, pred) in enumerate(zip(points, points_preds)):
    color_name = 'синий' if pred == 0 else 'красный'
    print(f"Точка {i+1}: {pt}, класс: {pred} ({color_name})")

# Визуализация
plt.scatter(X[:, 0], X[:, 1], c=preds, cmap='bwr', edgecolors='k', label='Обучающие точки')

# Рисуем точки C с цветом в соответствии с классом
for pt, pred in zip(points, points_preds):
    plt.scatter(pt[0], pt[1], color=class_colors[pred], edgecolors='black', s=150, label=f'Точка C класс {pred}')

plt.title("Классификация перцептроном с цветными точками C")
plt.xlabel("X1")
plt.ylabel("X2")

# Чтобы легенда не дублировалась для нескольких точек одного класса,
# добавим легенду только для первых появлений
handles, labels = plt.gca().get_legend_handles_labels()
from collections import OrderedDict
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

plt.grid(True)
plt.show()