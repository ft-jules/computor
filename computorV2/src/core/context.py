from src.utils.errors import MathError
class Context:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def set_variable(self, name, value):
        if name == 'i':
            raise MathError("Cannot reassign imaginary unit 'i'")
        self.variables[name] = value

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        raise MathError(f"Unknown variable '{name}'")