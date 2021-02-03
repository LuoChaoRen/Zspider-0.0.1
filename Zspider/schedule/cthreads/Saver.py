import logging
import multiprocessing
from .base import TypeEnum, BaseThread
from .utilities import *

class SaverThread(BaseThread):
    def working(self):
        """
        功能：
        a.获取save-item数据
        b.根据配置保存数据
        """
        item, keys,property = self._pool.get_a_task(TypeEnum.ITEM_SAVE)
        save_state, save_result = self._worker.working(item)
        if save_state > 0:
            self._pool.update_number_dict(TypeEnum.ITEM_SAVE_SUCC, +1)
        else:
            self._pool.update_number_dict(TypeEnum.ITEM_SAVE_FAIL, +1)
            logging.error("save error: %s", save_result)
        self._pool.finish_a_task(TypeEnum.ITEM_SAVE)

        return True
