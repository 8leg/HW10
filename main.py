class Rectangle:

    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def area(self):
        return self.__width * self.__height

    def perimeter(self):
        return 2 * self.__width + 2 * self.__height


if __name__ == '__main__':
    rec=Rectangle(5,6)
    print(rec.area())
    print(rec.perimeter())