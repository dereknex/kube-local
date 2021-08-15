from task.error import OutputNotFoundError
from config import Configuration
from task.error import InputNotFoundError, OutputNotFoundError
from task.task import Task
from rich.console import Console
from rich.progress import Progress

from jinja2 import Environment, BaseLoader
import copy
import concurrent.futures


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

        i = copy.deepcopy(self.cfg.inputs[in_dict["name"]])
        o = copy.deepcopy(self.cfg.outputs[out_dict["name"]])
        i.__dict__.update(in_dict)
        o.__dict__.update(out_dict)
        i._observers = []
        o._observers = []
        return (i, o)

    def _generate_tasks(self):
        for t in self.cfg.tasks:
            in_dict = t["input"]
            if in_dict["name"] not in self.cfg.inputs:
                raise InputNotFoundError(in_dict)
            out_dict = t["output"]
            if out_dict["name"] not in self.cfg.outputs:
                raise OutputNotFoundError(out_dict)
            items = [{}]
            if "with_items" in t:
                items = t["with_items"]
            for item in items:
                i, o = self._extract_item(item, copy.deepcopy(in_dict), copy.deepcopy(out_dict))
                o.set_local_path(i.get_save_path())
                t_name = "{}({})".format(t["name"], item["title"])
                task = Task(t_name, i, o)
                self._tasks.append(task)

    def run(self):
        self._console.print("Generating tasks...")
        self._generate_tasks()
        self._console.print("Running tasks...")
        if (self._tasks) == 0:
            self._console.print("No tasks!", style="bold red")
        futures = []
        with Progress(console=self._console) as progress:

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                for task in self._tasks:
                    task.progress_bar = progress
                    task.progress_id = progress.add_task(task.name + " wating", total=100)
                    # task.run()
                    futures.append(executor.submit(task.run))
        for future in futures:
            if future.exception() is not None:
                self._console.log(future.result())
        self._console.print("All Done!")
