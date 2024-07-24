from deta import Deta
from os import environ


deta_session=Deta(environ['DETA'])



class Database:
    def __init__(self,name):
        self.name = name
        self.db = deta_session.Base(name)
    def __setitem__(self,key,value):
        self.db.put(value,key)
    def __getitem__(self,key):
        v=self.db.get(key)
        return v['value'] if v != None else _raise(key)
    def __contains__(self,key):
        return self.db.get(key) != None
    def __delitem__(self,key):
        self.db.delete(key)
    def update(self,dict_u:dict):
        for k,v in dict_u.items():
            self[k]=v
    def query(self,dnl=False,query=None,):
        rt = {}
        response = self.db.fetch(query)
        last = None
        while response.last != None:
            if dnl:
                response = self.db.fetch(last=last,limit=dnl,desc=True)
            else:
                response = self.db.fetch(query,last=last)
            print(response.items,response.last)
            last = response.last
        for dict in response.items: rt.update(dict)
        return rt
    def top(self,n):
        return self.query(dnl=n)
    def get(self,key,*,default=None):
        try:
            return self[key]
        except KeyError:
            if default:
                return default
            else:
                _raise(key)
    @property
    def items(self):
        # VERY SLOW
        return {pair['key']:pair['value'] for pair in [dict for dict in self.query().items]}.items()
    
def _raise(key):
    raise KeyError(f'Key {key} not found.')
