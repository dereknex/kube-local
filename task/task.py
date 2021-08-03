class Task(object):
    name = ''
    in_obj = None
    out_obj = None

    def __init__(self, name, input, output):
        self.name = name
        self.in_obj = input
        self.out_obj = output

    def run(self):
        raise NotImplementedError()


# class TaskTemplate(object):
#     input_tpl = None
#     output_tpl = None
#     items = []
#     name = None

#     def _render_item(self, item):
#         pass

#     def render(self):
#         if self.items.count() == 0 :
#             return [Task(self.name, self.input_tpl, self.output_tpl)]
#         tasks = []
#         for i in self.items:
#             tasks.append(self._render_item(i))
#         return tasks

