import xml.sax.handler


class StringsHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        super().__init__()
        self.currentTag = ""
        self.currentName = ""
        self.currentContent = ""
        self.stringList = {}


    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.currentName = ""
        self.currentTag = tag
        if tag != "string":
            return
        if attributes.get("translatable", 'true') == 'false':
            return
        self.currentName = attributes["name"]
        self.stringList[self.currentName] = ""


    def endElement(self, name):
        if self.currentTag != 'string':
            return
        if self.currentName == '':
            return
        self.stringList[self.currentName] = self.currentContent
        self.currentTag = ""


    # 内容事件处理
    def characters(self, content):
        if(self.currentTag != 'string'):
            return
        self.currentContent = content