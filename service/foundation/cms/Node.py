class TxNode(object):
    __initValue = {
            'id_':None,#'',
            'curname':None,#'',
            'originname':None,#'',
            'nodetype':None,#0,
            'ssid':None,#'',
            'content':None,#'',
            'contenttype':None,#'',
            'link':None,#'',
            'properties':None,#{},
            'thumbnail':None,#'',
            'parent':None,#[],
            'children':None,#[],
            'attachment':None,#[],
            'state':None,#1,
            'objectstate':None#0,
            }

    def __init__(self):
        for k,v in self.__class__.__initValue.iteritems():
            self.__dict__[k] = v

    def addChildren(self, childid):
        if not self.children:
            self.children = []

        if childid not in self.children:
            self.children.append(childid)

    def removeChildren(self,childid):
        if self.children and childid in self.children:
            self.children.remove(childid)

    def addParent(self, parentid):
        if not self.parent:
            self.parent = []

        if parentid not in self.parent:
            self.parent.append(parentid)

    def removeParent(self, parentid):
        if self.parent and parentid in self.parent:
            self.parent.remove(parentid)

    def setProperty(self, name, value):
        if not self.properties:
            self.properties = {}

        self.properties[name] = value

    def getProperty(self,name):
        if self.properties:
            return self.properties.get(name)

    def __setattr__(self,name,value):
        if name not in self.__class__.__initValue.iterkeys():
            pass

        else:
            super.__setattr__(self,name,value)
