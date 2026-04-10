class Command():
    def __init__(self, command_type, arg1=None, arg2=None):
        self.command_type = command_type
        self.arg1 = arg1
        self.arg2 = arg2
    
    def ToString(self):
        return f"{self.command_type} {self.arg1} {self.arg2}"


