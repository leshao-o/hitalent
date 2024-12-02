import pytest
from unittest.mock import patch
from utils import get_input_task_data 


@pytest.mark.parametrize(
    "title, description, category, due_date, priority_choice",
    [
        ("Тестовая задача", "Это тестовое описание задачи", "Работа", "2023-12-31", "1"),
        ("Задача 1", "Описание задачи 1", "Личное", "2023-12-31", "3"),
        ("qwerty", "Описание без названия", "Работа", "2023-12-31", "4"),
    ]
)
def test_get_input_task_data(
    title,
    description,
    category,
    due_date,
    priority_choice
):
    inputs = [
        title,
        description,
        category,
        due_date,
        priority_choice 
    ]

    match priority_choice:
        case "1":
            priority = "Низкий"
        case "2":
            priority = "Средний"
        case "3":
            priority = "Высокий"
        case _:
            priority = "Низкий" 
    
    expected_task = {
        "title": title,
        "description": description,
        "category": category,
        "due_date": due_date,
        "priority": priority,
    }
    
    # Замена input() на mock, который будет возвращать значения из inputs
    with patch('builtins.input', side_effect=inputs):
        task = get_input_task_data()
    
    assert task == expected_task
