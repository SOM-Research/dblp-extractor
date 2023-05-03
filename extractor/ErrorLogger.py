from datetime import datetime

class ErrorLogger:
    def __init__(self):
        self.filePath = './itemErrorLog_'+str(datetime.now())+'.xml'

    def addItemErrorLogger(self, textItem):
        """
        Add a xml item in the error logger file
        :param textItem: xml item as a binary text
        """
        file = open(self.filePath, 'ab')
        file.write(textItem)
        file.write(bytes('\n', 'ascii'))
        file.close()

    def startObjectList(self, objectName):
        """
        The beginning of a xml item list
        :param objectName: the object list name
        """
        file = open(self.filePath, 'ab')
        file.write(bytes(('<%s>' % objectName), 'utf-8'))
        file.write(bytes('\n', 'ascii'))
        file.close()

    def endObjectList(self, objectName):
        """
        The end of a xml item list
        :param objectName: the object list name
        """
        file = open(self.filePath, 'ab')
        file.write(bytes(('</%s>' % objectName), 'utf-8'))
        file.write(bytes('\n', 'ascii'))
        file.close()

    def exceptionObject(self, exc_type, exc_value, exc_traceback):
        """
        Insert to the logger file an exception
        :param exc_type: exception type
        :param exc_value: exception value
        :param exc_traceback: exception traceback
        """
        file = open(self.filePath, 'ab')
        file.write(bytes(('<exception>'), 'ascii'))
        file.write(bytes('\n', 'ascii'))
        file.write(bytes(('<type>%s</type>' % exc_type), 'utf-8'))
        file.write(bytes('\n', 'ascii'))
        file.write(bytes(('<value>%s</value>' % exc_value), 'utf-8'))
        file.write(bytes('\n', 'ascii'))
        file.write(bytes(('<traceback>%s</traceback>' % exc_traceback), 'utf-8'))
        file.write(bytes('\n', 'ascii'))
        file.write(bytes(('</exception>'), 'ascii'))
        file.write(bytes('\n', 'ascii'))
        file.close()
