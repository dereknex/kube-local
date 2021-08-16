from informer import Informer
from rich.progress import Progress


class Task(object):
    name = ""
    in_obj = None
    out_obj = None
    progress_bar = None
    progress_id = 0

    def __init__(self, name, input, output):
        self.name = name
        self.in_obj = input
        self.out_obj = output
        self.in_obj.watch(self)
        self.out_obj.watch(self)

    def run(self):
        self.in_obj.download()
        self.out_obj.__dict__.update(self.in_obj.data)
        self.out_obj.upload()

    def update_progress(self, info):
        if self.progress_bar is None:
            return
        desc = ""
        if info == self.in_obj:
            desc = "{} {}".format(self.name, "Downloaded" if info.progress == 100 else "Downloading")
        if info == self.out_obj:
            desc = "{} {}".format(self.name, "Done" if info.progress == 100 else "Uploading")
        # print(desc)
        self.progress_bar.update(self.progress_id, completed=info.progress, description=desc)
