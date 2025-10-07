from core.clickableimage import ClickableImage


class Window:
    """
    Класс, содержащий в себе набор изображений для управления и взаимодействия с ними
    """

    def __init__(self, image_list: list["ClickableImage"] = None):
        self.image_list = list()
        if image_list is not None:
            self.image_list = image_list

    def append_image(self, img: "ClickableImage"):
        """
        Добавление новго изображения в окно

        :param img: новое изображение
        """
        self.image_list.append(img)
