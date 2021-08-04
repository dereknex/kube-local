class Task(object):
    name = ''
    in_obj = None
    out_obj = None

    def __init__(self, name, input, output):
        self.name = name
        self.in_obj = input
        self.out_obj = output

    def run(self):
       self.in_obj.download()
       self.out_obj.upload() 
