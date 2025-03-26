class DisplayFile:
    def __init__(self):
        self.__objects_list = []

    def addObject(self, g_object):
        self.__objects_list.append(g_object)
    
    def removeObject(self, i):
        self.__objects_list.pop(i)
    
    def get_names(self):
        return [obj.name for obj in self.__objects_list]

    def get_object(self, name):
        return next((obj for obj in self.__objects_list if obj.name == name), None)

    def updateObject(self, index, updated_object):
        self.__objects_list[index] = updated_object

    @property
    def objects_list(self):
        return self.__objects_list