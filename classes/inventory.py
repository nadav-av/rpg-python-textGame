class Item:
    def __init__(self, name, var, description, prop):
        self.name = name
        self.var = var
        self.description = description
        self.prop = prop

    def get_name(self):
        return self.name

    def get_descrioption(self):
        return self.description
