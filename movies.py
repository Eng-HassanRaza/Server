import requests,bs4,re
import MySQLdb,sys
from bs4 import BeautifulSoup
gtypes = []
games = []
db = MySQLdb.connect(host="localhost",user="scrapy",passwd="scrapybook",db="bookcomparer")
mycursor = db.cursor()
def grb(link):
        with requests.session() as a:
                xx = a.get(link)
                soup = BeautifulSoup(xx.text,"html.parser")
                cl = soup.findAll("div",{"class":"breadcrumbs"})
                lis = cl[0].findAll("li")
                tmp1 = "NA"
                tmp2 = "NA"
                tmp3 = "NA"
                tmp4 = "NA"
                tmp5 = "NA"
                tmp6 = "NA"
                tmp7="Startseite"
                tmp8="NA"
                tmpx=[]
                for i in range(1,5):
			try:
                        	tmp7=tmp7+"/%s"%lis[i].text.replace(" ","")
			except IndexError:
				continue                
		clm = soup.findAll("div",{"class":"details-text"})
                gr = clm[0].findAll("h1")
                gra = clm[0].findAll("p")
                if len(gra) == 2:
                        tmp2=gr[0].text
                        tmp1= gra[0].text
                        tmp8= gra[1].text.replace(" ","").replace("FSK:\n","")
                else:
                        tmp2=gr[0].text
                        tmp1= gra[0].text
                clma = soup.findAll("ul",{"class":"tabs-nav"})
                three = clma[0].findAll("div",{"class":"tab-container"})
                for i in range(0,3):
                        if i == 0:
                                try:
                                        xx = three[0].find("strong").text
                                        tmp3 = xx.encode("utf-8")
                                        tmp3 = re.sub('[^0-9,]', '', tmp3)
                                except AttributeError:
                                        continue
                        elif i == 1:
                                try:
                                        xx = three[1].find("strong").text
                                        tmp4 = xx.encode("utf-8")
                                        tmp4 = re.sub('[^0-9,]', '', tmp4)
                                except AttributeError:
                                        continue
                        elif i == 2:
                                try:
                                        xx = three[2].find("strong").text
                                        tmp5 = xx.encode("utf-8")
                                        tmp5 = re.sub('[^0-9,]', '', tmp5)
                                except AttributeError:
                                        continue
                it = soup.findAll("span",{"class":"price"})
                tmp6 = re.sub('[^0-9,]', '', str(it[0].text.encode("utf-8")))
                try:
                        sql = "INSERT INTO BZ_Films VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(tmp1.encode("utf-8","ignore"),tmp2.encode("utf-8","ignore"),tmp3.encode("utf-8","ignore"),tmp6.encode("utf-8","ignore"),tmp4.encode("utf-8","ignore"),tmp5.encode("utf-8","ignore"),tmp7.encode("utf-8","ignore"),tmp8.encode("utf-8","ignore"))
                        mycursor.execute(sql)
                        db.commit()
                except:
                        pass
def game_links(wa):
        ur = wa.findAll("div",{"class":"item-text"})
        for ll in ur:
                gm=ll.findChild("a",href=True)
                games.append("https://www.buyzoxs.de/%s"%gm["href"])
def the_real(jeta,nn,wa):
        last = nn*20-20
        pa = 0
        while pa != last+20:
                with requests.session() as lo:
                        linkm="%s/from/%s.html?all=1"%(jeta.replace(".html?all=1",""),pa)
                        ah = lo.get(linkm)
                        soup = BeautifulSoup(ah.text,"html.parser")
                        game_links(soup)
                        pa = pa+20
			sys.stdout.write("Acquired links: %s\r"%len(games))
			sys.stdout.flush()
	print "Links sorted !"
def get_gtypes():
        with requests.session() as s:
                x = s.get("https://www.buyzoxs.de/kaufen/dvd-blu-ray.html")
                soup = BeautifulSoup(x.text,"html.parser")
                ss = soup.findAll("section", {"class": "categories-all row"})
                li = ss[0].findChildren("a",href=True)
                for x in li:
                        gtypes.append("https://www.buyzoxs.de/%s?all=1"%x["href"])
get_gtypes()
for gtl in gtypes:
        with requests.session() as e:
                try:
                        ff = e.get(gtl)
                        soup= BeautifulSoup(ff.text,"html.parser")
                        cl = soup.findAll("div",{"class":"pager"})
                        num = cl[0].findChildren("li",class_=False)
                        if len(num) == 5:
                                pg= num[4].text
                                the_real(gtl,int(pg),soup)
                        elif len(num) == 4:
                                the_real(gtl,4,soup)
                        elif len(num) == 3:
                                the_real(gtl,3,soup)
                        elif len(num) == 2:
                                the_real(gtl,2,soup)
                        elif len(num) == 1:
                                the_real(gtl,1,soup)
                except IndexError:
                        continue
mycursor.execute("DELETE FROM BZ_Films")
db.commit()
print "Appending to database !"
for lin in games:
        grb(lin)
print "Scraping Completed ."

