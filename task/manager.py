from task.error import OutputNotFoundError
from config import Configuration
from task import InputNotFoundError, OutputNotFoundError, Task
from rich.console import Console
from jinja2 import Environment, BaseLoader

class Manager:
    
    _tasks = []
    

    def __init__(self, cfg: Configuration):
        self.cfg = cfg
        self._generate_tasks()
        self._console = Console()

    def _extract_task(self, task) -> list:
        i = task['input']
        o = task['output']
        if i['name'] not in self.cfg.inputs:
            raise InputNotFoundError(i)
        if o['name'] not in self.cfg.outputs:
            raise OutputNotFoundError(o)
        if 'with_items' not in task:
            i_obj = self.cfg.inputs[i['name']]
            o_obj = self.cfg.outputs[o['name']]
            i_obj.__dict__.update(i)
            o_obj.__dict__.update(o)
            return [Task(task['name'], i_obj, o_obj)]

        for item in task['with_items']:
            for k, v in i:
                i[k] = Environment(loader=BaseLoader()).from_string(v).render(**item)
            for k, v in o:
                o[k] = Environment(loader=BaseLoader()).from_string(v).render(**item)
            i_obj = self.cfg.inputs[i['name']]
            o_obj = self.cfg.outputs[o['name']]
            i_obj.__dict__.update(i)
            o_obj.__dict__.update(o)
             

    def _generate_tasks(self):
        for t in self.cfg.tasks:
            self._extract_task(t)

    def run(self):
        if (self._tasks) == 0:
            self._console.print("No tasks!", style="bold red")

    