from task_manager import TaskManager
from utils import get_input_task_data


if __name__ == "__main__":
    task = TaskManager("tasks.json")

    while True:
        print("""
            Выберите действие:
            1. Просмотр всех задач
            2. Просмотр задач по категориям
            3. Добавление задачи 
            4. Изменение задачи
            5. Отметка задачи как выполненной
            6. Удаление задачи по айди или категории
            7. Поиск по ключевым словам, категории или статусу выполнения
        """)
        action = int(input("Введите номер действия: "))
        print()
        match action:
            case 1:
                task.show_all_tasks()
            case 2:
                category = input("Введите категорию: ")
                task.show_tasks_by_category(category)
            case 3:
                data = get_input_task_data()
                task.add_task(**data)
            case 4:
                id = int(input("Введите id задачи: "))
                print("Введите только те данные, которые надо изменить")
                data = get_input_task_data()
                task.edit_task(id=id, **data)
            case 5:
                id = int(input("Введите id задачи: "))
                task.mark_task_as_completed(id=id)
            case 6:
                print("Удалить по id или по категории:")
                print("1. По id")
                print("2. По категории")
                delete_by = input("Введите номер: ")
                if delete_by == "1":
                    id = int(input("Введите id задачи: "))
                    task.delete_task(id=id)
                elif delete_by == "2":
                    category = input("Введите категорию: ")
                    task.delete_task(category=category)
            case 7:
                print("Поиск по ключевым словам, категории или статусу выполнения:")
                print("1. По ключевым словам")
                print("2. По категории")
                print("3. По статусу выполнения")
                search_by = input("Введите номер: ")
                if search_by == "1":
                    keyword = input("Введите ключевые слова: ")
                    task.show_tasks_by_filters(keyword=keyword)
                elif search_by == "2":
                    category = input("Введите категорию: ")
                    task.show_tasks_by_filters(category=category)
                elif search_by == "3":
                    status = input("Введите статус выполнения: ")
                    task.show_tasks_by_filters(status=status)
                else:
                    print("Неправильный номер")
            case _:
                print("Такого действия нет, выберите другое") 
        