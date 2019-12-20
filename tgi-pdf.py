import urllib.request
import urllib.parse
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader, PdfFileWriter
import ntpath

def getlinks(debug = False):
    url = "https://i11www.iti.kit.edu/teaching/winter2019/tgi/index"
    req = urllib.request.Request(url) 
    resp = urllib.request.urlopen(req)
    respData = resp.read() 
    soup = BeautifulSoup(respData, features="html.parser")
    soup = soup.find_all('a', attrs={'class':'media mediafile mf_pdf'})
    #print(soup)
    pdfs = []
    for s in soup:
        if ("vorlesung" in s['href'] or "uebung" in s['href']) and not "uebungsblatt" in s['href']:
            pdfs.append("https://i11www.iti.kit.edu" + s['href'])
            #print("https://i11www.iti.kit.edu" + s['href'])
    return pdfs

def download(paths):
    for link in paths:
        filename = ntpath.basename(link)
        urllib.request.urlretrieve(link, "pdfs/" + filename)

def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        path = "pdfs/" + ntpath.basename(path)
        pdf_reader = PdfFileReader(path, strict=False)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)


if __name__ == "__main__":
    #print(sys.version)
    paths = getlinks(False)
    download(paths)
    merge_pdfs(paths, output='tgi.pdf')
    #main(sys.argv[1:])