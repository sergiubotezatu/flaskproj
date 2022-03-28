
class Services:
    container = {}
    DEPENDENCIES = {}
    
    @classmethod
    def get(cls, constructor):
        def wrapper(instance, *services):
            if len(services) == 1 and services[0] == None:
                return constructor(instance)
            else:
                next_inject = ()
                injected = ()
                for service in services:
                    next_inject = Services.unpack_if_needed(cls.DEPENDENCIES[service])
                    injected += (cls.container[service](*next_inject),)
                constructor(instance, *injected)
                
        return wrapper
  
    @staticmethod
    def unpack_if_needed(dependency):
        if type(dependency) != tuple:
            return (dependency,)
        return dependency