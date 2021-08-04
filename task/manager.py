from task.error import OutputNotFoundError
from config import Configuration
from task.error import InputNotFoundError, OutputNotFoundError
from task.task import Task
from rich.console import Console
from jinja2 import Environment, BaseLoader
import copy


class Manager:
    
    _tasks = []
    

    def __init__(self, cfg: Configuration):
        self.cfg = cfg
        self._console = Console()
        self._tpl_env = Environment(loader=BaseLoader(), autoescape=True)

    def _extract_item(self, item, in_dict, out_dict):
        for k, v in in_dict.items():
            in_dict[k] = self._tpl_env.from_string(v).render(**item)
        for k, v in out_dict.items():
            out_dict[k] = self._tpl_env.from_string(v).render(**item)
        i = copy.deepcopy(self.cfg.inputs[in_dict['name']])
        o = copy.deepcopy(self.cfg.outputs[out_dict['name']])
        i.__dict__.update(in_dict)
        o.__dict__.update(out_dict)
        return  (i, o)
             

    def _generate_tasks(self):
        for t in self.cfg.tasks:
            in_dict = t['input']
            if in_dict['name']  not in self.cfg.inputs:
                raise InputNotFoundError(in_dict)
            out_dict = t['output']
            if out_dict['name'] not in self.cfg.outputs:
                raise OutputNotFoundError(out_dict)
            items = [{}]
            if 'with_items' in t:
                items = t['with_items']
            for idx  in range(len(items)):
                item = items[idx]
                i, o = self._extract_item(item, copy.deepcopy(in_dict), copy.deepcopy(out_dict))
                t_name = '{}[{}]'.format(t['name'], idx)
                self._tasks.append(Task(t_name, i, o))

    def run(self):
        self._generate_tasks()
        if (self._tasks) == 0:
            self._console.print("No tasks!", style="bold red")

    