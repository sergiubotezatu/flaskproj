class Services:
    container = {}
    
    @classmethod
    def get(cls, constructor):
        def wrapper(instance, service):
            constructor(instance, cls.container[service]())
        return wrapper