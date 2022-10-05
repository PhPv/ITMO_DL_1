

class Frame:
    """
    Основной объект кадра. Плагины, в которые обернуты модели работают именно с этим объектом
    """
    def __init__(self, img):
        """
        :param img: изображение кадра
        """
        self.img = img
        # координаты bound-box автомобиля на текущем кадре
        self.car = []
        # координаты bound-box номера автомобился на кадре
        self.number = []
        # итоговый распознанный номер автомобился
        self.recognition_number = ''
        #  тип атвомобился: auto – легковой, special – спецтехника
        self.status = 'auto'


class Model:
    def __init__(self):
        pass

    def process(self, frame: Frame):
        pass
