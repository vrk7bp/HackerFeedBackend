class User():
    """ Models a user"""
    def __init__(self, id):
        self.id = id
        self.read_articles = set()  # Both of these sets are composed of User_Articles
        self.unread_articles = set()
        self.interests = []  # list of interests, subset of article keywords, NOT IN USE YET
        self.sites = []  # list of sites user is most interested in , NOT IN USE YET

    def add_article(self, user_article):
        """
         Adds an item of class User_article to the Article list
        """
        self.unread_articles.add(user_article)



    def read_article(self, id, rating):
        art = User_Article(id, rating)
        self.unread_articles.remove(art)
        self.read_articles.add(art)

    def add_interest(self, keyword):
        self.interests.append(keyword)

    def add_sites(self, site):
        self.sites.append(site)  # site is just a base url
        # ie www.wired.com/subdir/article -> www.wired.com 

    def __str__(self):
        return str(self.id) + " " + str(self.unread_articles)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class User_Article():
    """Models a user's view of an Article - light structure """

    def __init__(self, id, rating):
        """
        id = article
        Url = path to the article
        Keywords = list of keywords in the article
        """
        self.id = id
        self.rating = rating

    def update_rating(self, rating):
        self.rating = rating

    def __eq__(self, other):
        """
         Equality is based soley on ID and class type
        """
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __str__(self):
        return str((self.id, self.rating))

    def __repr__(self):
        return str(self)


class Article():
    """Models an Article - is a more complete structure """

    def __init__(self, id, url, keywords, title):
        """
        id = article
        Url = path to the article
        Keywords = list of keywords in the article
        """
        self.id = id
        self.url = url
        self. keywords = keywords
        self.title = title
        # Add stuff here, like score, comments, ect ..

    def __eq__(self, other):
        """
         Equality is based soley on ID and class type
        """
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False



if __name__ == '__main__' : 
    User1 = User(1)
    user2 = User(2)
    print User1 == user2