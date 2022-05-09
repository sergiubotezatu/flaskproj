class Services:
    container = {}
    dependencies = {}
    
    @classmethod
    def get(cls, constructor):
        def wrapper(*services):
            service_list = list(services)
            for i in range (0, len(service_list)):
                injected = cls.container.get(service_list[i])
                dependency = cls.dependencies.get(service_list[i])
                if injected != None:
                    service_list[i] = injected() if dependency == None else injected(*dependency)
            constructor(*service_list)
        return wrapper
  
