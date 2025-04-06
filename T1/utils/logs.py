class Logs:
    def __init__(self, log_message_func, object_list ):
        self.__log_message = log_message_func
        self.__object_list = object_list

    def logDeleteMessage(self):
        index_selected_obj = self.__object_list.currentRow()      
        if index_selected_obj != -1:
            selected_item = self.__object_list.item(index_selected_obj)
            selected_item_text = selected_item.text()
            object_name = selected_item_text.split(' (')[0]
            self.__log_message(f"Objeto {object_name} deletado.")
        
    def logAddObject(self):
              
        item_count = self.__object_list.count()
        if item_count > 0:
            last_item = self.__object_list.item(item_count - 1)
            
            self.__log_message(f"O objeto {last_item.text()} foi criado.") 
    
    def logObjectEdited(self, object_name):
        self.__log_message(f"Objeto {object_name} editado.")

    def logObjNotFound(self):
        self.__log_message("Object not found.")

    def logNoSelectedItem(self):
        self.__log_message("No selected item.")

    def logNoObjSelected(self):
        self.__log_message("No object selected.")
    
    def logWindowMovidaPara(self, side, scale):

        if side == "left":
            self.__log_message(f"Window foi movida pra esquerda em {scale}%.")

        elif side == "rigth":
            self.__log_message(f"Window foi movida pra direita em {scale}%.")

        elif side == "up":
            self.__log_message(f"Window foi movida pra cima em {scale}%.")

        elif side == "down":
            self.__log_message(f"Window foi movida pra baixo em {scale}%.")

    def logZoomIn(self, scale):
        self.__log_message(f"Zoom In de {scale}% aplicado.")

    def logZoomOut(self, scale):
        self.__log_message(f"Zoom Out de {scale}% aplicado.")

    def logWindowRotation(self, scale):
        self.__log_message(f"Rotação de {scale}% aplicada na window.")