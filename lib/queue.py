class Queue:
    contents = []

    def __init__(self, size):
        self.contents = [None] * size

    def isFull(self):
        ret = True
        for c in self.contents:
            if c is None:
                ret = False

        return ret

    def changeContent(self, index, content):
        self.contents[index] = content
        return self.contents

    def dequeue(self):
        ret = self.contents[0]
        self.contents[0] = None

        return ret

    def isEmpty(self):
        ret = True
        for c in self.contents:
            if c is not None:
                ret = False

        return ret

    def peek(self):
        return self.contents[0]
