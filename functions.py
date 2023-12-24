file_path = 'ToDos.txt'


def load_file():
    with open(file_path, 'r') as file:
        todos_list = file.readlines()
    return todos_list


def write_todos(todo_list):
    with open(file_path, 'w') as file:
        file.writelines(todo_list)
    return


def print_todos(todo_list, print_msg):
    """ Return To Do list in its current state """
    print(print_msg)
    for index, i in enumerate(todo_list):
        display_todo = f"{index + 1}. {i}"
        print(display_todo.strip('\n'))
    return

