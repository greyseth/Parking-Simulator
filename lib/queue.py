class Queue:
    contents = []

    def __init__(self, size, defaultContent=None):
        self.contents = [defaultContent] * size

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
        firstNoneIndex = 0
        for i, c in enumerate(self.contents):
            if c is None:
                firstNoneIndex = i
                break

        self.contents[firstNoneIndex] = new

    def dequeue(self):
        ret = self.contents[0]
        self.contents[0] = None

        newContents = self.contents
        for i in range(len(self.contents)):
            if i < len(self.contents) - 1:
                newContents[i] = self.contents[i + 1]
            else:
                newContents[i] = None

        self.contents = newContents
        return ret

    def peek(self):
        return self.contents[0]
