class settings:
    class __settings:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg=0):
        if not settings.instance:
            settings.instance = settings.__settings(arg)
        else:
            settings.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __getitem__(self, name):
        return getattr(self.instance, name)
    def __setitem__(self, vaue,name):
        return setattr(self.instance,vaue, name)
