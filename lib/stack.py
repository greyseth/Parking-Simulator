class Stack:
    contents = []

    def __init__(self, size):
        self.contents = [None] * size

    def isFull(self, noneCheck=None):
        ret = True
        for c in self.contents:
            if noneCheck is None:
                if c is None:
                    ret = False
            else:
                if noneCheck(c) == True:
                    ret = False

        return ret

    def size(self):
        return len(self.contents)

    def isEmpty(self, fillCheck=None):
        ret = True
        for c in self.contents:
            if fillCheck is None:
                if c is not None:
                    ret = False
            else:
                if fillCheck(c) == True:
                    ret = False

        return ret

    def changeContent(self, index, content):
        self.contents[index] = content
        return self.contents

    def enqueue(self, new):
        firstNoneIndex = -1
        for i, c in enumerate(self.contents):
            if c is None:
                firstNoneIndex = i
                break

        if firstNoneIndex != -1:
            self.contents[firstNoneIndex] = new

    def dequeue(self):
        lastContentIndex = len(self.contents) - 1
        for i, c in enumerate(self.contents):
            if c is None:
                lastContentIndex = i - 1
                break

        ret = self.contents[lastContentIndex]
        self.contents[lastContentIndex] = None

        return ret

    def checkCanDequeue(self, content=None, index: int = -1):
        ret = False

        for i, c in enumerate(self.contents):
            if content is not None:
                if c == content:
                    if i == len(self.contents) - 1:
                        ret = True
                        break
                    ret = self.contents[i + 1] is None
            else:
                if i == index:
                    if i == len(self.contents) - 1:
                        ret = True
                        break
                    ret = self.contents[i + 1] is None

        return ret

    def peek(self):
        return self.contents[len(self.contents) - 1]
