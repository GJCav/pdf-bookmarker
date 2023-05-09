from PyPDF2 import PdfFileReader as PReader, PdfFileWriter as PWriter

import argparse

parser = argparse.ArgumentParser(description='Add bookmarks to pdf')
parser.add_argument('-i', type=str, help='input pdf file', required=True)
parser.add_argument('-o', type=str, help='output pdf file', default='out.pdf')
parser.add_argument('-m', type=str, help='menu file')
parser.add_argument('-f', type=int, help='page offset', required=True)

args = parser.parse_args()

menu_file = args.m
with open(menu_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

class Node:
    def __init__(self, title, page, parent) -> None:
        self.title = title
        self.page = page
        self.parent = parent
        self.children = []

        if parent:
            parent.children.append(self)
        
root = Node('/docroot',  -1, None)
hierachy = [[], [], [], []]

def tabCount(s):
    cnt = 0
    for i in range(len(s)):
        if s[i] == '\t': cnt+=1
        else: break
    return cnt

def isInt(s):
    try:
        int(s)
        return True
    except:
        return False

def getTitlePage(s: str):
    s = s.strip()
    arr = s.split(' ')
    if isInt(arr[-1]):
        return (' '.join(arr[:-1]), int(arr[-1]))
    else:
        print(s)
        return (' '.join(arr), None)

for l in lines:
    if l == None or not l.strip():
        continue
    lvl = tabCount(l)
    while len(hierachy) <= lvl:
        hierachy.append([])
    
    if lvl == 0:
        title, page = getTitlePage(l)
        hierachy[0].append(Node(title, page, root))
    else:
        parent = hierachy[lvl-1][-1]
        title, page = getTitlePage(l)
        hierachy[lvl].append(Node(title, page, parent))



inPDF = PReader(args.i)
pdf = PWriter()
pdf.cloneDocumentFromReader(inPDF)

print(f'{len(pdf.getObject(pdf._pages)["/Kids"])}')

offset = args.f
_lvl = 0
_parent = None
def dfsAddBookMark(h: Node):
    global _lvl, _parent
    if h == root:
        _parent = None
        for c in h.children:
            dfsAddBookMark(c)
        _parent = None

    else:

        _lvl+=1
        _oldPnt = _parent

        if h.page is not None:
            print(f'{h.title} --> {h.page+offset}')
            _parent = pdf.addBookmark(h.title, h.page+offset, _parent)
            
        else:
            # _parent = pdf.addBookmark(h.title, h.children[0].page//2-1, _parent)
            print(h.page)
            raise 'Fuck'

        for c in h.children:
            dfsAddBookMark(c)

        _parent = _oldPnt
        _lvl -= 1

dfsAddBookMark(root)

with open(args.o, 'wb') as f:
    pdf.write(f)
