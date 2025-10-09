from taskmanager import TaskManager
from ai_service import create_simple_task_Hugging

def print_menu():
    print("\n---------Gestor de tareas Inteligente------")
    print("1. Añadir tarea")
    print("2. Añadir tarea compleja (con IA)")
    print("3. Listar tareas")
    print("4. Completar tarea")
    print("5. Eliminar tarea")
    print("6. Salir")


def main():

    manager = TaskManager()

    while True:

        print_menu()
    
        try: 

            choice = int(input("Elige una opcion: "))

            match choice:

                case 1:
                    description = input("Descripcion de la tarea: ")
                    manager.add_task(description)

                case 2:
                    description = input("Descripcion de la tarea compleja: ")
                    subtasks= create_simple_task_Hugging(description)
                    for subtask in subtasks:
                        if not subtask.startswith("Error:"):
                            manager.add_task(subtask)
                        else:
                            print(subtask)
                            break


                case 3:
                    manager.list_task()

                case 4:
                    id= int(input("Id de tarea a completar: "))
                    manager.complete_task(id)

                case 5:
                    id= int(input("Id de tarea a eliminar"))
                    manager.delete_task(id)

                case 6:
                    print("Saliendo...")
                    break

                case _:
                    print("Opcion no valida. Selecciona otra.")
        except ValueError:
            print("Opcion no valida. Selecciona otra.")


if __name__ == "__main__":
    main()