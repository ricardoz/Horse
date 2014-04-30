import lxml.etree
import lxml.html
import urllib2
import Race
    
import unicodedata
def strip_accents(s):
    print "before",s
    nkfd_form = unicodedata.normalize('NFKD', unicode(s))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    
    print "after",  only_ascii
    return only_ascii
    

class Horse(object):
    # Create based on class name:
    #self.races = []
    
    def __init__(self, name, races, new = None):
        #print "name", name
        self.href = new
        
        if isinstance(name, unicode):
            self.name = strip_accents(name)
        else:
            self.name = str(name)
            
        print self.name, "is my name"
        self.races = [] + races
        
    def filt(self, func, disp= False):
        #print type(func), "func"
        races = [x for x in self.races if func(x)]
        if disp: 
            return self.display(races)
        if races:
            return races
        else:
            return []
        
    def display(self, races):
        return self.name + ": \n" + "\n".join(str((x)) for x in races)
        
    def __repr__(self):
        #for x in self.races:
            #print str(x)
        return self.display(self.races)
    
    def factory(href):
        #return eval(type + "()")
        start = href.index('?')+1
        end = href.index('&h')+1
        new = href[:start] + href [end:]
        
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
        
        races = [Race.Race.raceFromSoup(r) for r in raceRows]
        return Horse(name, races, new)
        
    factory = staticmethod(factory)
    
    def horseLinks(self,list=None):
        print "hlinks", str(list)
        if list is None:
            list = self.races
        l = [self.href] + [r.href for r in list]
        return "var horseLinks = " + str(l)

 