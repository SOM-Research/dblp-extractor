
class ErrorLogger:
    def __init__(self):
        self.filePath = './itemErrorLog.xml'

    def addItemErrorLogger(self, textItem):
        file = open(self.filePath, 'ab')
        file.write(textItem)
        file.write(bytes('\n', 'ascii'))
        file.close()

    def startObjectList(self, objectName):
        file = open(self.filePath, 'ab')
        file.write(bytes(('<%s>' % objectName), 'utf-8'))
        file.write(bytes('\n', 'ascii'))
        file.close()

    def endObjectList(self, objectName):
        file = open(self.filePath, 'ab')
        file.write(bytes(('</%s>' % objectName), 'utf-8'))
        file.write(bytes('\n', 'ascii'))
        file.close()
