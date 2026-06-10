from pypdf import PdfReader
path='/home/user/workspace/erdos872/buddhdev_872.pdf'
r=PdfReader(path)
terms=['4.3. The conditional T2 theorem','Definition 4.5','A.1. Conditional proof','Auxiliary slot game and potential','Proposition A.6','Proposition A.9']
for term in terms:
    print('\nTERM',term)
    for i,p in enumerate(r.pages, start=1):
        txt=p.extract_text() or ''
        if term in txt:
            print('page',i)
            j=txt.find(term)
            print(txt[max(0,j-200):j+500].replace('\n',' '))
