from google.cloud import datastore

class Clothing():
    """An object to hold clothing"""
    def __init__(self, image, style):
        """Constructor"""
        self.image = image
        self.style = style

    def __str__(self):
        return '%s %s' % (self.image, self.style)

class User():
    """An object to hold users"""
    def __init__(self, name="admin", index=0):
        self.name = name
        self.likes = self.get_liked() #a list containing keys to datastore clothes the user has liked
        #self.preferences = preferences #todo
        self.index = index #index being the location in the list of clothing itmes
    
    def add_like(self, liked):
        """Add the liked clothing item to the list of likes"""
        self.likes.append(liked)
        client = datastore.Client()
        key = client.key('like')
        toUpload = datastore.Entity(key)
        toUpload['username'] = self.name
        toUpload['clothingi'] = liked.image
        toUpload['clothings'] = liked.style
        client.put(toUpload)

    def get_liked(self):
        #get all clothes from datastore where user has liked
        client = datastore.Client()
        result = []
        query = client.query(kind='like')
        query.add_filter("username", "=", self.name)
        for entity in query.fetch():
            result.append(Clothing(entity['clothingi'],entity['clothings']))
        return result

    def viewed_item(self):
        client = datastore.Client()
        self.index = self.index + 1
        key = client.key('user', self.name)
        toUpload = datastore.Entity(key)
        toUpload['index'] = self.index
        client.put(toUpload)


