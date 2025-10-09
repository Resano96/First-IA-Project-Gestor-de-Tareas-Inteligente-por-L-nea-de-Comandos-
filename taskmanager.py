import json

#clase tarea
class Task:
    #cada tarea tiene atributos: id, descripcion y completada
    def __init__(self, id, description, completed=False):
        self.id = id
        self.description = description
        self.completed  = completed

    def __str__(self):
        status = "✔️" if self.completed else "❌"
        return f"[{status}] #{self.id}: {self.description}"
    
#clase manager    
class TaskManager:

    FILENAME = "task.json"
    #tiene los atributos tasks(lista) y nextID(int)
    def __init__(self):
        self._tasks=[]
        self._next_id=1
        self.load_tasks()

    #add task recibe una descripcion, la añade a la lista de tasks, sube el contador y guarda en el json
    def add_task(self, description):
        task = Task(self._next_id, description)
        self._tasks.append(task)
        self._next_id +=1
        print(f"Tarea añadida: {description}")
        self.save_tasks()

    #list task comprueba que la lista no este vacia y si no lo esta muestra las tareas
    def list_task(self):
        if not self._tasks:
            print("No hay tareas pendientes")
        else:
            for task in self._tasks:
                print(task)

    #complete task recibe un id de tarea, comprueba si esta en la lista y si lo esta,
    #cambia su valor de completed a true y guarda en el json
    def complete_task(self, id):
        for task in self._tasks:
            if task.id == id:
                task.completed = True
                print(f"Tarea completada: {task}")
                self.save_tasks()
                return
        print(f"Tarea no encontrada: #{id}")

    #delete task recibe un id de tarea, comprueba si esta en la lista y si lo esta,
    #elimina esa tarea de la lista y guarda en el json
    def delete_task(self, id):
        for task in self._tasks:
            if task.id == id:
                self._tasks.remove(task)
                print(f"Tarea eliminada: {id}")
                self.save_tasks()
                return
        print(f"Tarea no encontrada: #{id}")

    #load task sirve para cargar el json
    def load_tasks(self):
        try:
            with open(self.FILENAME, "r") as file:
                data = json.load(file)
                self._tasks= [Task(item["id"], item["description"], item["completed"])for item in data]
                if self._tasks:
                    self._next_id = self._tasks[-1].id + 1
                else:
                    self._next_id = 1
        except FileNotFoundError:
            self._tasks = []

    #save task sirve para guardar el json
    def save_tasks(self):
        with open(self.FILENAME, "w") as file:
            json.dump([{"id": task.id, "description": task.description, "completed": task.completed} for task in self._tasks], file, indent=4)