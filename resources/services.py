
class Services:
    container = {}
    DEPENDENCIES = {}
    
    @classmethod
    def get(cls, constructor):
        def wrapper(instance, service = None):
            if service == None:
                return constructor(instance)
            else:
                next_inject = cls.DEPENDENCIES[service]
                injected = cls.container[service]
                constructor(instance, injected(next_inject))
                
        return wrapper