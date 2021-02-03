class Save(object):
    def working(self, item):
        try:
            save_state, save_result = self.item_save(item)
        except Exception as excep:
            save_state, save_result = -1, [self.__class__.__name__, excep]

        return save_state, save_result

    def item_save(self,item) -> (int,str):

        raise NotImplementedError
