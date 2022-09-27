# This is a sample Python script.
import xml
import re
from xml.dom.minidom import Document

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from pygoogletranslation import Translator

from StringsHandler import StringsHandler


def parseXml(xml_file):
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    handler = StringsHandler()
    parser.setContentHandler(handler)

    parser.parse(xml_file)
    return handler.stringList


def outputByMiniDom(content, xml_file):
    doc = Document()
    resources = doc.createElement("resources")
    doc.appendChild(resources)
    f = open(xml_file, "w", encoding='utf-8')
    for k, v in content.items():
        s = doc.createElement("string")
        value = doc.createTextNode(processText(v.text))
        resources.appendChild(s)
        s.setAttribute('name', k)
        s.appendChild(value)
    f.write(doc.toprettyxml(indent="  ", encoding='utf-8')
            .decode('utf-8'))
    f.close()


def outputBySax(content, xml_file):
    attr0 = xml.sax.xmlreader.AttributesImpl({})
    f = open(xml_file, "w", encoding='utf-8')
    x = xml.sax.saxutils.XMLGenerator(f, encoding='utf-8', short_empty_elements=True)
    x.startDocument()
    x.startElement("resources", attr0)
    for k, v in content.items():
        x.startElement("string", xml.sax.xmlreader.AttributesImpl({'name': k}))
        x.characters(processText(v.text))
        x.endElement("string")
    x.endElement("resources")
    x.endDocument()
    f.close()


def processText(src):
    result = re.sub(r'[％%]\s?([DdSs])', lambda matched: '%' + matched.group(1).lower(), src)
    result = re.sub(r'[^\\]\'', '\\\\\'', result)
    return result


def translateToXml(string_list, dst):
    translator = Translator(service_url='translate.google.cn')
    origin_list = list(string_list.values())
    print(origin_list)
    result_list = translator.translate(origin_list, src='en', dest=dst)
    for t in result_list:
        print(t.text)
    result_dic = {}
    i = 0
    for k, v in string_list.items():
        if i >= len(result_list):
            break
        result_dic[k] = result_list[i]
        i = i + 1
    outputByMiniDom(result_dic, "../res/strings-%s.xml" % dst)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    stringList = parseXml('../res/strings.xml')
    print(stringList)
    for d in ['it']:
        translateToXml(stringList, dst=d)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
