from datetime import datetime

def get_input_task_data() -> dict:
    """
    Функция для ввода данных о задаче
    """
    while True:
        title = input("Введите название задачи: ")
        if not title.strip():
            print("Название задачи не может быть пустым. Пожалуйста, введите название.")
            continue
        break

    while True:
        description = input("Введите описание задачи: ")
        if not description.strip():
            print("Описание задачи не может быть пустым. Пожалуйста, введите описание.")
            continue
        break

    while True:
        category = input("Введите категорию задачи: ")
        if not category.strip():
            print("Категория задачи не может быть пустой. Пожалуйста, введите категорию.")
            continue
        break

    while True:
        due_date = input("Введите срок выполнения задачи (YYYY-MM-DD): ")
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Некорректный формат даты. Пожалуйста, введите дату в формате YYYY-MM-DD.")
    
    priority_choice = input("Выберите приоритет задачи:\n  1. Низкий\n  2. Средний\n  3. Высокий\n")
    match priority_choice:
        case "1":
            priority = "Низкий"
        case "2":
            priority = "Средний"
        case "3":
            priority = "Высокий"
        case _:
            print("Некорректный выбор. Установлен приоритет по умолчанию: низкий.")
            priority = "Низкий" 

    task = {
        "title": title,
        "description": description,
        "category": category,
        "due_date": due_date,
        "priority": priority,
    }
    return task