from config import Configuration
from task.task import Task
from rich.console import Console
from rich.progress import Progress
from informer import Status

from jinja2 import Environment, BaseLoader

import copy
import concurrent.futures

from input import Factory as InputFactory
from output import Factory as OutputFactory


class Manager:

    _tasks = []
    _task_status = {}
    _progress_bar = None

    def __init__(self, cfg: Configuration):
        self.cfg = cfg
        self._console = Console()
        self._progress_bar = Progress(console=self._console)
        self._tpl_env = Environment(loader=BaseLoader(), autoescape=True)

    def _extract_item(self, item, in_dict, out_dict):
        for k, v in in_dict.items():
            if not isinstance(v, str):
                continue
            in_dict[k] = self._tpl_env.from_string(v).render(**item)
        for k, v in out_dict.items():
            if not isinstance(v, str):
                continue
            out_dict[k] = self._tpl_env.from_string(v).render(**item)

        i = InputFactory.create(type=in_dict["kind"], config=in_dict)
        o = OutputFactory.create(type=out_dict["kind"], config=out_dict)

        return (i, o)

    def _generate_tasks(self):
        for t in self.cfg.tasks:

            in_data = t["input"]
            in_dict = {**self.cfg.inputs[in_data["name"]], **in_data}
            # if in_dict["name"] not in self.cfg.inputs:
            #     raise InputNotFoundError(in_dict)
            out_data = t["output"]
            out_dict = {**self.cfg.outputs[out_data["name"]], **out_data}
            # if out_dict["name"] not in self.cfg.outputs:
            #     raise OutputNotFoundError(out_dict)
            items = [{}]
            if "with_items" in t:
                items = t["with_items"]
            for item in items:
                i, o = self._extract_item(item, copy.copy(in_dict), copy.copy(out_dict))
                # o.set_local_path(i.get_save_path())
                t_name = "{}({})".format(t["name"], item["title"])
                task = Task(t_name, i, o)
                i.watch(self, {"name": t_name, "type": "in"})
                o.watch(self, {"name": t_name, "type": "out"})
                self._tasks.append(task)

    def update_progress(self, info, meta=None):
        if meta is None:
            return
        name = meta["name"]
        if name not in self._task_status.keys():
            return
        progress_id = self._task_status[name]
        if meta["type"] == "in":
            desc = "{} {}".format(name, "Downloaded" if info.status == Status.DONE else "Downloading")
        elif meta["type"] == "out":
            desc = "{} {}".format(name, "Done" if info.status == Status.DONE else "Uploading")
        self._progress_bar.update(progress_id, completed=info.progress, description=desc)

    def run(self):
        self._console.print("Generating tasks...")
        self._generate_tasks()
        self._console.print("Running tasks...")
        if (self._tasks) == 0:
            self._console.print("No tasks!", style="bold red")

        futures = []
        with self._progress_bar as progress:
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                for task in self._tasks:
                    progress_id = progress.add_task(task.name + " wating", total=100)
                    self._task_status[task.name] = progress_id
                    futures.append(executor.submit(task.run))
        for future in futures:
            if future.exception() is not None:
                self._console.log(future.result())
        self._console.print("All Done!")
