from PySide6 import QtWidgets

from screens.editObject import EditObject

class ObjectEditor:
    def __init__(self, object_list, display_file, log_message_func, update_view_func):
        self.__object_list = object_list
        self.__display_file = display_file
        self.__log_message = log_message_func
        self.__updateViewframe = update_view_func

    def edit_object(self):
        """Handles the process of selecting and editing an object."""
        
        index_selected_obj = self.__object_list.currentRow()      
        if index_selected_obj != -1:
            selected_item = self.__object_list.item(index_selected_obj)
            if selected_item:
                selected_item_text = selected_item.text()
                object_name = selected_item_text.split(' (')[0]
                selected_object = self.__display_file.get_object(object_name)
                
                if selected_object:
                    edit_window = EditObject(selected_object, self.__display_file, self.__object_list)
                    
                    if edit_window.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                        updated_object = edit_window.object_to_edit

                        self.__display_file.updateObject(index_selected_obj, updated_object)
                        self.__object_list.takeItem(index_selected_obj)
                        self.__object_list.insertItem(index_selected_obj, updated_object.name + edit_window.object_type)
                    
                        self.__updateViewframe()
                        self.__log_message.logObjectEdited(object_name)
                else:
                    self.__log_message.logObjNotFound()
            else:
                self.__log_message.logNoSelectedItem()
        else:
            self.__log_message.logNoObjSelected()
