import random


class Queue:
    def __init__(self):
        self.__items = []

    def enqueue(self, item: any) -> None:
        self.__items.append(item)

    def dequeue(self) -> any:
        if self.length() > 0:
            return self.__items.pop(0)

        return None

    def remove_at(self, i:int) -> any:
        self.__items.pop(i)

    def shuffle(self) -> None:
        random.shuffle(self.__items)

    def length(self) -> int:
        return len(self.__items)

    def get(self, i) -> any:
        return self.__items[i]
