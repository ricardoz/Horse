def yuni(code):
    try: 
        #print "yccode", code
        return str(code).replace("'","*")
    except:
        print "yuni" + code
        raise "yuni", code
    

def dataFromRow(race):
    #what is race?
    print "Race", race.text
    print "Race type", type(race)
    print race.text_content()

    vals = {}
    
    data = race.findall(".//td")
    
    dt = [d.text_content().split() for d in data]
    
    
    iter = race.iterlinks()


    l = list(iter)
    iter = race.iterlinks()



    print "iter from race.iterlinks()", iter, "length", len(l)

    for item in iter:
        print item

    iter = race.iterlinks()

    href = iter.next()[2]  #.find(".//b[@class='black']//a")


    print "HREF DataFRomRow Race", href, "type", type(href)

    #11/9/14 Changed result to race_id
    while ("race_id" not in href):
        print "while loop checking for race_id", href
        href = iter.next()[2]

    #href = [r[2] for r in race.ite]
    
    
   
    start = href.index("?") + 1
    end = href.index("&r")
    
    vals['href'] = "http://www.racingpost.com" + href[:end]
    
    
    
    
   
    
    vals['date'] = dt [1][0]
    #print "1", dt[1], len(dt[1]), type(dt[1])
    
    vals['course'] = dt [2][0]
    vals['dist/going'] = dt [2][1]
    vals['class/rt'] = dt [2][2]

    print "prevalue", dt[2]

    vals['value'] = dt [2][-1]
    
    vals['weight'] = dt [3][0]
    
    posRunners = dt [4][0].split("/")
    
    ##print dt[4][1], type(dt[4][1])
    
    vals['pos'] = posRunners[0]
    vals['runners'] = posRunners[1]
    #vals['dist/next'] = getLength(dt[4][1]) + " ".join(dt [4][2:-1])
    vals['price'] = dt [4][-1]
    
    import unicodedata
    distance = 0
    
    if isinstance(dt[4][1], unicode):
        #print "unicode", dt[4][1]
        #print dt[4][1][1:-2]
        lengths = 0
        try:
            lengths = int( dt[4][1][1:-2] )
        except:
            pass
        distance = lengths + unicodedata.numeric(dt[4][1][-2])
        
    else:
        #print "reg", dt[4][1]
        print dt[4][1][1:-1]
        lengths = 1
        try:
            lengths = int( dt[4][1][1:-1] )
        except:
            pass
        distance = lengths
        
    vals['dist/next'] = str(distance) + "L " + " ".join([yuni(x) for x in dt [4][2:-1]])

    temp = " ".join(dt [5])
    vals['jockey'] = temp.replace("'","*")
    
    vals['or'] = dt [6][0]
    vals['ts'] = dt [7][0]
    vals['rpr'] = dt [8][0]


    print "FINISHED"
    
    return vals

class Race(object):
    def price(self, tag):
        if tag[0] == 'E':
            return 1.0
        
        else:
            num, den = tag.split('/')
        
            if len(num.split())>1:
                num = int(num.split()[1].strip())
            
            den = den.strip()
        
            if not den[-1].isdigit():
                
                den = den[:-1]
        
            return float(num)/int(den)
            

    def fg(self, fg):
            if (fg[1].isdigit()):
                
                return (int(fg[0:2]), fg[2:])
            else:
                return (int(fg[0:1]), fg[1:]) 
    
    def weight(self, w):
        stones, pounds = w.split('-')
        return 14 * int(stones) + int(pounds)
        
    def __init__(self, rx):
        self.date = rx['date']
        date = self.date
        day = int(date[0:2])
        month = date[2:5]
        year = int(date[5:])
        self.href = rx['href']

       # print day, month, year
    

        self.course = rx['course']
        f_g = rx['dist/going'].strip()
        self.furlongs, self.going = self.fg(f_g)

       # print self.furlongs, self.going
        
        key = 'class/rt/value'
        v = rx['value'].strip()
        #print "value",v, "--", v[:v.index('K')]
        self.raceClass = rx['class/rt']
        print "value:",v, v[:v.index('K')]
        self.value = int(v[:v.index('K')])
        
        #print self.raceClass, self.value
        
        self.weight = self.weight(rx['weight'])
        
        #print self.weight, "lbs"
        
        self.pos = -1
        try:
            self.pos = int(rx['pos'])
        except:
            print "position", rx['pos']
        self.runners = int(rx['runners'].strip())
        
        #print self.pos, "out of", self.runners
        
        self.price = self.price(rx['price'].strip())
        
        #print self.price
        
        self.jockey = rx['jockey']
        
        try:
            self.OR = int(rx['or'])
        except:
            self.OR = 0
            
        self.ts = rx['ts']
        self.rpr = rx['rpr']
        self.distNext = rx ['dist/next']
    
    def raceFromSoup(rx):
        return Race(dataFromRow(rx))
        
    def __str__(self):
        return self.date + " " + self.course + " " + str(self.furlongs) \
        + "" +self.going + " " + self.raceClass + " " + str(self.value)\
        + "\t" + str(self.pos) + "/" + str(self.runners) + " " + \
        yuni(self.distNext) + " " + str(self.price) + "\t" + self.jockey + \
        "\t" + str(self.OR) + "/" + str(self.ts) + "/" +  \
        str(self.rpr)
        
    def __repr__(self):
        return str(self.__dict__)
    
    raceFromSoup = staticmethod(raceFromSoup)
    
if __name__=="__main__":
    import lxml.etree
    import lxml.html
    import urllib2
    
    new = "http://www.racingpost.com/horses/horse_home.sd?race_id=578285&r_date=2013-05-25&horse_id=805266"
    url = urllib2.urlopen(new)
    content = url.read()
    
    soup = lxml.html.fromstring(content)
    #print "soup", soup.text_content()
        
    name = soup.find(".//title").text_content().split("|")[0].strip()
        
    tables = soup.findall(".//table")
    #print "tb len", len(tables), tables
    raceGrid = tables[1]
    raceRows = raceGrid.findall(".//tr")[1:]
        
    #print "rr len", len(raceRows), raceRows
        
    race = Race.raceFromSoup(raceRows[3])