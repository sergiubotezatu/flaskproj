

class Services:
    container = {}
    dependencies = {}
    
    @classmethod
    def get(cls, constructor):
        def wrapper(instance, *services):
            next_inject = ()
            injected = ()
            for service in services:
                if cls.dependencies[service] == None:
                    injected += (cls.container[service](),)
                else:
                    next_inject = Services.pack_if_needed(cls.dependencies[service])
                    injected += (cls.container[service](*next_inject),)
            return constructor(instance, *injected)
                
        return wrapper
  
    @staticmethod
    def pack_if_needed(dependency):
        if type(dependency) != tuple:
            return (dependency,)
        return dependency