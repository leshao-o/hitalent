import json
import pytest
import io
from contextlib import redirect_stdout
import pprint

from task_manager import TaskManager, Task


@pytest.fixture(scope="function")
def clear_json_file():
    with open("test_tasks.json", "w") as file:
        json.dump([], file)  

@pytest.fixture()
def task_manager(clear_json_file):
    yield TaskManager("test_tasks.json")

@pytest.fixture(scope="function")
def populate_json_file(task_manager):
    sample_tasks = [
        {
            "id": 1,
            "title": "Сделать домашнее задание",
            "description": "Необходимо выполнить все задания по математике.",
            "category": "Учеба",
            "due_date": "2023-10-15",
            "priority": "Высокий",
            "status": "Не выполнена"
        },
        {
            "id": 2,
            "title": "Купить продукты",
            "description": "Купить молоко, хлеб и яйца.",
            "category": "Покупки",
            "due_date": "2023-10-10",
            "priority": "Средний",
            "status": "Не выполнена"
        },
        {
            "id": 3,
            "title": "Провести встречу с клиентом",
            "description": "Встреча состоится в офисе в 14:00.",
            "category": "Работа",
            "due_date": "2023-10-12",
            "priority": "Высокий",
            "status": "Выполнена"
        }
    ]
    
    with open("test_tasks.json", "w") as file:
        json.dump(sample_tasks, file, indent=4, ensure_ascii=False)
    
    task_manager._refresh_tasks()

def test_show_all_tasks(task_manager, populate_json_file):
    f = io.StringIO()
    with redirect_stdout(f): 
        task_manager.show_all_tasks()
    
    output = f.getvalue()  

    # Форматируем ожидаемый вывод с помощью pprint
    expected_output = io.StringIO()
    with redirect_stdout(expected_output):
        pprint.pprint([
            {
                "id": 1,
                "title": "Сделать домашнее задание",
                "description": "Необходимо выполнить все задания по математике.",
                "category": "Учеба",
                "due_date": "2023-10-15",
                "priority": "Высокий",
                "status": "Не выполнена"
            },
            {
                "id": 2,
                "title": "Купить продукты",
                "description": "Купить молоко, хлеб и яйца.",
                "category": "Покупки",
                "due_date": "2023-10-10",
                "priority": "Средний",
                "status": "Не выполнена"
            },
            {
                "id": 3,
                "title": "Провести встречу с клиентом",
                "description": "Встреча состоится в офисе в 14:00.",
                "category": "Работа",
                "due_date": "2023-10-12",
                "priority": "Высокий",
                "status": "Выполнена"
            }
        ])

    expected_output_str = expected_output.getvalue()
    assert output.strip() == expected_output_str.strip()

def test_show_tasks_by_category(task_manager, populate_json_file):
    f = io.StringIO()
    with redirect_stdout(f): 
        task_manager.show_tasks_by_category("Покупки")
    
    output = f.getvalue()  

    expected_output = io.StringIO()
    with redirect_stdout(expected_output):
        pprint.pprint([
            {
                "id": 2,
                "title": "Купить продукты",
                "description": "Купить молоко, хлеб и яйца.",
                "category": "Покупки",
                "due_date": "2023-10-10",
                "priority": "Средний",
                "status": "Не выполнена"
            }
        ])

    expected_output_str = expected_output.getvalue()
    assert output.strip() == expected_output_str.strip()

def test_add_task(task_manager, clear_json_file):
    task_manager.add_task(
        title="New Task", 
        description="New Desc", 
        category="New Category", 
        due_date="2022-01-03", 
        priority="Средний"
    )
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "New Task"
    task_manager.add_task(
        title="New Task 2", 
        description="New Desc 2", 
        category="New Category 2", 
        due_date="2022-01-04", 
        priority="Высокий"
    )
    assert len(task_manager.tasks) == 2
    assert task_manager.tasks[1].priority == "Высокий"

def test_edit_task(task_manager, populate_json_file):
    task_manager.edit_task(id=1, title="Updated Task", description="Updated Desc")
    assert task_manager.tasks[-1].title == "Updated Task"
    assert task_manager.tasks[-1].description == "Updated Desc"

def test_mark_task_as_completed(task_manager, populate_json_file):
    task_manager.mark_task_as_completed(id=1)
    assert task_manager.tasks[-1].status == "Выполнена"

def test_delete_task(task_manager, populate_json_file):
    assert len(task_manager.tasks) == 3
    task_manager.delete_task(id=1)
    assert len(task_manager.tasks) == 2
    task_manager.delete_task(category="Покупки")
    assert len(task_manager.tasks) == 1

def test_show_tasks_by_filters(task_manager, populate_json_file):
    f = io.StringIO()
    with redirect_stdout(f): 
        task_manager.show_tasks_by_filters(keyword="задание")
        task_manager.show_tasks_by_filters(category="Покупки")
        task_manager.show_tasks_by_filters(status="Выполнена")

    expected_tasks = []
    expected_tasks.append([
        {
            "id": 1,
            "title": "Сделать домашнее задание",
            "description": "Необходимо выполнить все задания по математике.",
            "category": "Учеба",
            "due_date": "2023-10-15",
            "priority": "Высокий",
            "status": "Не выполнена"
        }
    ])
    expected_tasks.append([
        {
            "id": 2,
            "title": "Купить продукты",
            "description": "Купить молоко, хлеб и яйца.",
            "category": "Покупки",
            "due_date": "2023-10-10",
            "priority": "Средний",
            "status": "Не выполнена"
        }
    ])
    expected_tasks.append([
        {
            "id": 3,
            "title": "Провести встречу с клиентом",
            "description": "Встреча состоится в офисе в 14:00.",
            "category": "Работа",
            "due_date": "2023-10-12",
            "priority": "Высокий",
            "status": "Выполнена"
        }
    ])

    output = f.getvalue()  
    expected_output = io.StringIO()
    with redirect_stdout(expected_output):
        for task in expected_tasks:
            pprint.pprint(task)

    expected_output_str = expected_output.getvalue()
    assert output.strip() == expected_output_str.strip()

def test_get_all_task_ids(task_manager, populate_json_file):
    assert task_manager._get_all_task_ids() == [1, 2, 3]

def test_save_tasks_to_JSON(task_manager, populate_json_file):
    assert len(task_manager.tasks) == 3
    task = Task(
        id=1,
        title="Сделать домашнее задание",
        description="Необходимо выполнить все задания по математике.",
        category="Учеба",
        due_date="2023-10-15",
        priority="Высокий",
        status="Не выполнена"
    )
    task_manager._save_tasks_to_JSON(task)
    task_manager._refresh_tasks()
    assert len(task_manager.tasks) == 4

def test_refresh_tasks(task_manager, populate_json_file):
    task_manager._refresh_tasks()
    assert len(task_manager.tasks) == 3
