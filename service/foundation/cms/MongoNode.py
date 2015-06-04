class TxMongoNode(object):
    '''
    initValue = {
            'id':None,#'',
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
    '''

    def __init__(self):
        # self.__dict__ = self.__class__.initValue

        self.id = None
        self.curname = None
        self.originname = None
        self.nodetype = None
        self.ssid = None
        self.content = None
        self.contenttype = None
        self.link = None
        self.properties = None
        self.thumbnail = None
        self.parent = None
        self.children = None
        self.attachment = None
        self.state = None
        self.objectstate = None

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

