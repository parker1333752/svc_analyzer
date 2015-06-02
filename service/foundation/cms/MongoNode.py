class TxMongoNode(object):
    __initValue = {
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

    __slots__ = tuple(__initValue.iterkeys())

    def __init__(self):
        self.__dict__ = __initValue

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

