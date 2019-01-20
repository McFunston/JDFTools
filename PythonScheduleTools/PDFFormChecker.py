import sys
import os.path
import time
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1


def PDFFormChecker(path, fieldName, trueValue):
    #filename = sys.argv[1]
    print('Checking '+path)
    if 'digital' in path.lower() or 'changes' in path.lower():
        return False
    if 'approv' in path.lower() or 'ok' in path.lower() or 'final' in path.lower():
        return True
    try:
        fp = open(path, 'rb')
    except FileNotFoundError:
        return False
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    try:
        fields = resolve1(doc.catalog['AcroForm'])['Fields']
    except KeyError:
        return False
    for i in fields:
        field = resolve1(i)
        name, value = field.get('T'), field.get('V')
        if fieldName in str(name) and trueValue in str(value):
            return True
    return False

#print(PDFFormChecker('G:/OneDrive/P001R10-Ott3_01.pdf', 'PROOF OK AS SUBMITTED', 'Yes'))
