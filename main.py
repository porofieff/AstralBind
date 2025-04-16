import numpy as np

# Шкала Саати
SAATY_SCALE = {
    1: "Равная важность",
    3: "Умеренное превосходство",
    5: "Сильное превосходство",
    7: "Очень сильное превосходство",
    9: "Абсолютное превосходство",
    2: "Промежуточное значение между 1 и 3",
    4: "Промежуточное значение между 3 и 5",
    6: "Промежуточное значение между 5 и 7",
    8: "Промежуточное значение между 7 и 9"
}

# Случайные индексы согласованности RI
RI_TABLE = {
    1: 0.00,
    2: 0.00,
    3: 0.58,
    4: 0.90,
    5: 1.12,
    6: 1.24,
    7: 1.32,
    8: 1.41,
    9: 1.45,
    10: 1.49
}

def input_comparison_matrix(criteria):
    n = len(criteria)
    matrix = np.ones((n, n))
    print("\nВведите оценки по шкале Саати:")
    for i in range(n):
        for j in range(i+1, n):
            while True:
                print(f"\nНасколько '{criteria[i]}' важнее чем '{criteria[j]}'?")
                for k, v in SAATY_SCALE.items():
                    print(f"{k}: {v}")
                try:
                    value = int(input("Оценка: "))
                    if value in SAATY_SCALE:
                        matrix[i][j] = value
                        matrix[j][i] = 1 / value
                        break
                    else:
                        print("Неверное значение. Повторите ввод.")
                except ValueError:
                    print("Введите число.")
    return matrix

def calculate_weights(matrix):
    eigvals, eigvecs = np.linalg.eig(matrix)
    max_index = np.argmax(eigvals.real)
    principal_eigvec = eigvecs[:, max_index].real
    weights = principal_eigvec / principal_eigvec.sum()
    return weights, eigvals[max_index].real

def calculate_consistency_ratio(matrix, lambda_max):
    n = matrix.shape[0]
    CI = (lambda_max - n) / (n - 1)
    RI = RI_TABLE.get(n, 1.49)  # Если больше 10 критериев
    CR = CI / RI if RI != 0 else 0
    return CI, CR

def run_ahp():
    print("=== Метод анализа иерархий (МАИ) ===")
    criteria = input("Введите критерии (через запятую): ").strip().split(",")
    criteria = [c.strip() for c in criteria if c.strip()]
    if len(criteria) < 2:
        print("Необходимо минимум два критерия.")
        return

    while True:
        matrix = input_comparison_matrix(criteria)
        weights, lambda_max = calculate_weights(matrix)
        CI, CR = calculate_consistency_ratio(matrix, lambda_max)

        print("\n--- Результаты ---")
        print("Весы критериев:")
        for crit, w in zip(criteria, weights):
            print(f"{crit}: {w:.4f}")
        print(f"\nИндекс согласованности (CI): {CI:.4f}")
        print(f"Отношение согласованности (CR): {CR:.4f}")

        if CR < 0.1:
            print("\nСогласованность удовлетворительная.")
            break
        else:
            print("\nСогласованность неудовлетворительная (CR > 0.1).")
            retry = input("Хотите повторить ввод сравнений? (y/n): ").lower()
            if retry != 'y':
                break

if __name__ == "__main__":
    run_ahp()
