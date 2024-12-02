import json
import pprint

from task import Task


class TaskManager:
    """
    Менеджер по управлению задачами
    """
    def __init__(self, filename: str):
        """
        Инициализация менеджера задач
        """
        self.filename = filename
        self._tasks: list[Task] = []
        self._refresh_tasks()
    
    @property
    def tasks(self) -> list[Task]:
        """
        Геттер для получения списка задач.
        """
        return self._tasks
    
    def show_all_tasks(self, tasks: list[Task] = None) -> None:
        """
        Отображает все задачи или переданные задачи
        """
        self._refresh_tasks()
        pprint.pprint(list(map(Task.to_dict, tasks or self._tasks)))

    def show_tasks_by_category(self, category: str) -> None:
        """
        Отображает задачи по указанной категории
        """
        tasks_by_category = []
        for task in self._tasks:
            if task.category == category:
                tasks_by_category.append(task)
        if not tasks_by_category:
            print("\nЗадач с такой категорией нет")
            return
        self.show_all_tasks(tasks_by_category)

    def add_task(
        self, 
        title: str, 
        description: str, 
        category: str, 
        due_date: str, 
        priority: str, 
        id: int = None,
        status: str = "Не выполнена"
    ) -> None:
        """
        Добавление новой задачи
        """
        tasks_ids = self._get_all_task_ids()
        if not id:
            id = max(tasks_ids) + 1 if tasks_ids else 1
        task = {
            "id": id,
            "title": title,
            "description": description,
            "category": category,
            "due_date": due_date,
            "priority": priority,
            "status": status
        }
        new_task = Task(**task)
        self._save_tasks_to_JSON(new_task)
        self._refresh_tasks()
        print("\nНовая задача добавлена")
        
    def edit_task(self, id: int, **data: dict) -> None:
        """
        Редактирование задачи
        """
        self._refresh_tasks()
        task_to_edit = None
        for task in self._tasks:
            if task.id == id:
                task_to_edit = task
                break
        if task_to_edit is None:
            print(f"\nЗадача с ID {id} не найдена.")
            return
        
        for key, value in data.items():
            if hasattr(task_to_edit, key) and value:
                setattr(task_to_edit, key, value)
        
        self.delete_task(id=id)
        self._save_tasks_to_JSON(task_to_edit)
        self._refresh_tasks()
        print(f"\nЗадача с ID {id} успешно обновлена.")


    def mark_task_as_completed(self, id: int) -> None:
        """
        Маркирование задачи как выполненной
        """
        self.edit_task(id=id, status="Выполнена")

    def delete_task(self, id: int = None, category: str = None) -> None:
        """
        Удаление задачи
        """
        for task in self._tasks:
            if (id and task.id == id) or (category and task.category == category):
                self._tasks.remove(task)
                self._save_tasks_to_JSON()  
                break  
        else:
            print("\nЗадача для удаления не найдена.")
        
    def show_tasks_by_filters(self, keyword: str = None, category: str = None, status: str = None) -> None:
        """
        Поиск задач по ключевым словам, категории или статусу выполнения.
        """
        results = []
        self._refresh_tasks()
        for task in self._tasks:
            if (keyword and (keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower())) or \
            (category and task.category.lower() == category.lower()) or \
            (status and task.status.lower() == status.lower()):
                results.append(task)

        if results:
            self.show_all_tasks(results)
        else:
            print("\nЗадачи не найдены.")

    def _get_all_task_ids(self) -> list[int]:
        """
        Функция для получения всех id задач
        """
        self._refresh_tasks()
        return [task.id for task in self._tasks]

    def _save_tasks_to_JSON(self, task: Task = None) -> None:
        """
        Сохраняет задачи в JSON файл. Если передан task, добавляет его к существующим задачам,
        иначе перезаписывает файл со всеми задачами.
        """
        tasks_data = []
        
        try:
            with open(self.filename, "r") as file:
                tasks_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при чтении файла {self.filename}: {e}")
        
        if task:
            tasks_data.append(task.to_dict())
        else:
            tasks_data = list(map(Task.to_dict, self._tasks))

        try:
            with open(self.filename, "w") as file:
                json.dump(tasks_data, file, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Ошибка записи в файл: {e}")
        except (ValueError, TypeError) as e:
            print(f"Ошибка с данными для записи в JSON: {e}")

    def _refresh_tasks(self) -> None:
        """
        Обновляет данные о задачах внутри программы, загружая их из JSON файла.
        """
        try:
            with open(self.filename, "r") as file:
                tasks_data = json.load(file) 
                self._tasks = [Task(**task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка при чтении файла {self.filename}: {e}")
            self._tasks = []
