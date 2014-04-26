#!/usr/bin/env python

# What to tell Monty... 1) That he sends me a true or false (boolean) based on whether the person liked the article (based on how much time they spend reading it)
                    #   2) That he has to use a collections.OrderedDict in order to pass JSON values correctly to me.

#What I have to do... make sure the defaultList method does what it is supposed to
# Add the algorithm change for the update method so that ArticlesPush gets updated...
# Add authentication from the Android/iOS client
# Create a data structure for the ArticlesRead List so that it stops at 100 or 200 articles (and coordinate that with the API)
# Add a transaction around that update API call back.
# Change JSONProperty to Structured Property

import endpoints
import API_comm
import Recommender
import Structures
from protorpc import messages
from protorpc import remote
from protorpc import message_types
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from bs4 import BeautifulSoup


class ArticleRead(ndb.Model):
    id = ndb.StringProperty(required=True)
    userLiked = ndb.FloatProperty(required=True)


class ArticleList(ndb.Model):
    id = ndb.StringProperty(required=True) #Just the Article ID


class UsersList(ndb.Model):
    UserID = ndb.StringProperty(required=True)
    ArticlesToRead = ndb.StructuredProperty(ArticleRead, repeated=True)
    ArticlesToPush = ndb.StructuredProperty(ArticleList, repeated=True)


class ArticleDatabase(ndb.Model):
    id = ndb.StringProperty(required=True) #Article ID
    title = ndb.StringProperty(required=True) #Title
    points = ndb.IntegerProperty(required=True) #Points of the story
    comments = ndb.StringProperty(required=True) #Link to the comments
    submitter = ndb.StringProperty(required=True) #UserName of the person who submitted
    url = ndb.StringProperty(required=True) #URL
    self_post = ndb.BooleanProperty(required=True) #Is this AskHN or not
    domain = ndb.StringProperty(required=True) #Domain of the article
    profile = ndb.StringProperty(required=True) #link to user profile
    time = ndb.StringProperty(required=True) #As in like 10 hours
    num_comments = ndb.IntegerProperty(required=True) #Number of comments
    rank = ndb.IntegerProperty(required=True) #Ranking


class UserID(messages.Message):
    id = messages.StringField(1, required=True)


class ArticlesPush(messages.Message):
    id = messages.StringField(1, required=True) #Article ID
    title = messages.StringField(2, required=True) #Title
    points = messages.IntegerField(3, required=True) #Points of the story
    comments = messages.StringField(4, required=True) #Link to the comments
    submitter = messages.StringField(5, required=True) #UserName of the person who submitted
    url = messages.StringField(6, required=True) #URL
    self_post = messages.BooleanField(7, required=True) #Is this AskHN or not
    domain = messages.StringField(8, required=True) #Domain of the article
    profile = messages.StringField(9, required=True) #link to user profile
    time = messages.StringField(10, required=True) #As in like 10 hours
    num_comments = messages.IntegerField(11, required=True) #Number of comments
    rank = messages.IntegerField(12, required=True) #Ranking


class TestReturn(messages.Message):
    field = messages.StringField(1, required=True)


class Articles(messages.Message):
    id = messages.StringField(1, required=True)
    userLiked = messages.FloatField(2, required=True)


class UserIDAndArticles(messages.Message):
    id = messages.StringField(1, required=True)
    items = messages.MessageField(Articles, 2, repeated=True)


class ArticleListOut(messages.Message):
    items = messages.MessageField(ArticlesPush, 1, repeated=True)

def populateArticleDB(value):
    ArticleList = API_comm.get_top_articles(value)
    for elements in ArticleList:
        articleQuery = ArticleDatabase.query(ArticleDatabase.id == elements['id']).get()
        if articleQuery is None:
            e = ArticleDatabase(id = elements['id'],
                                title= elements['title'],
                                points= elements['points'],
                                comments = elements['comments'],
                                submitter = elements['submitter'],
                                url = elements['url'],
                                self_post = elements['self'],
                                domain = elements['domain'],
                                profile = elements['profile'],
                                time = elements['time'],
                                num_comments = elements['num_comments'],
                                rank = elements['rank'])
            e.put()
        else:
            articleQuery.time = elements['time'];
            articleQuery.points = elements['points'];
            articleQuery.num_comments = elements['num_comments'];
            articleQuery.rank = elements['rank'];
            articleQuery.put()


def getArticleInformation(articleIDList):
    returnList = []
    for element in articleIDList:
        articleInfo = ArticleDatabase.query(ArticleDatabase.id == element.id).get()
        tempArticle = ArticlesPush()
        tempArticle.id = articleInfo.id
        tempArticle.title = articleInfo.title
        tempArticle.points = articleInfo.points
        tempArticle.comments = articleInfo.comments
        tempArticle.submitter = articleInfo.submitter
        tempArticle.url = articleInfo.url
        tempArticle.self_post = articleInfo.self_post
        tempArticle.domain = articleInfo.domain
        tempArticle.profile = articleInfo.profile
        tempArticle.time = articleInfo.time
        tempArticle.num_comments = articleInfo.num_comments
        tempArticle.rank = articleInfo.rank
        returnList.append(tempArticle)
    return returnList


#Just a test method so that I could test the dataStore retrieval
def insertToDB2():
        list1 = [ArticleRead(id = '1', userLiked = .1), ArticleRead(id = '2', userLiked = .1)]
        list2 = [ArticleList(id= '3'), ArticleList(id= '4')]
        list3 = [ArticleRead(id = '1', userLiked = .1), ArticleRead(id= '2', userLiked= .1)]
        list4 = [ArticleList(id= '5'), ArticleList(id= '6')]
        UsersList(UserID='Three', ArticlesToRead=list1, ArticlesToPush=list2).put()
        UsersList(UserID='Five', ArticlesToRead=list3, ArticlesToPush=list4).put()
        ArticleDatabase(id= '3', title= "hi3", points= 3, comments= "comm3", submitter= "sub3", url= "url3", self_post= False, domain= "domain3", profile= "prof3", time= "time3", num_comments= 3, rank= 3).put()
        ArticleDatabase(id= '4', title= "hi4", points= 4, comments= "comm4", submitter= "sub4", url= "url4", self_post= True, domain= "domain4", profile= "prof4", time= "time4", num_comments= 4, rank= 4).put()
        ArticleDatabase(id= '5', title= "hi5", points= 5, comments= "comm5", submitter= "sub5", url= "url5", self_post= False, domain= "domain5", profile= "prof5", time= "time5", num_comments= 5, rank= 5).put()
        ArticleDatabase(id= '6', title= "hi6", points= 6, comments= "comm6", submitter= "sub6", url= "url6", self_post= True, domain= "domain6", profile= "prof6", time= "time6", num_comments= 6, rank= 6).put()
        ArticleDatabase(id= '1', title= "hi1", points= 1, comments= "comm1", submitter= "sub1", url= "url1", self_post= True, domain= "domain1", profile= "prof1", time= "time1", num_comments= 1, rank= 1).put()
        ArticleDatabase(id= '2', title= "hi2", points= 2, comments= "comm2", submitter= "sub2", url= "url2", self_post= False, domain= "domain2", profile= "prof2", time= "time2", num_comments= 2, rank= 2).put()

#Have to create a method here that retrieves from the API the top 200 articles in default order
def defaultList():
    list1 = [ArticleList(id= '1'), ArticleList(id= '2')]
    return list1


@endpoints.api(name='hackerFeed', version='v1',
               description='API for Hacker Feed Application')
class HackerFeedApi(remote.Service):

    @endpoints.method(UserID, ArticleListOut,
                      name='user.articlePush',
                      path='articlesPush',
                      http_method='GET')
    def get_articles_push(self, request):
        uid = request.id
        userlist = UsersList.query(UsersList.UserID == uid).get()
        if userlist is None:
            raise endpoints.NotFoundException('List for user ID %s not found' % uid)

        articlesToPush = userlist.ArticlesToPush

        returnList = getArticleInformation(articlesToPush)

        return ArticleListOut(items = returnList)

    @endpoints.method(UserID, ArticleListOut,
                      name='user.articleRead',
                      path='articlesRead',
                      http_method='GET')
    def get_articles_read(self, request):
        uid = request.id
        userlist = UsersList.query(UsersList.UserID == uid).get()
        if userlist is None:
            raise endpoints.NotFoundException('List for user ID %s not found' % uid)

        articlesToRead = userlist.ArticlesToRead

        returnList = getArticleInformation(articlesToRead)

        return ArticleListOut(items = returnList)

    @endpoints.method(UserID, ArticleListOut,
                      name='user.newUser',
                      path='new_user',
                      http_method='POST')
    def new_user(self, request):
        articleList = defaultList()
        e = UsersList(UserID = request.id,
                      ArticlesToRead= [],
                      ArticlesToPush= articleList)
        e.put()

        returnList = getArticleInformation(articleList)

        return ArticleListOut(items = returnList)

    @endpoints.method(UserIDAndArticles, ArticleListOut,
                      name='user.update',
                      path='update',
                      http_method='POST')
    def get_update(self, request):
        # get UsersList entity and raise an exception if none found.
        uid = request.id
        userlist = UsersList.query(UsersList.UserID == uid).get()
        if userlist is None:
            raise endpoints.NotFoundException('List for user ID %s not found' % uid)

        list = userlist.ArticlesToRead
        for item in request.items:
            tempArticle = ArticleRead()
            tempArticle.id = item.id
            tempArticle.userLiked = item.userLiked
            list.append(tempArticle)
        userlist.ArticlesToRead = list
        userlist.put()

        #put command to update push list here...

        #query2 = UsersList.query(UsersList.UserID == userID) [this is in case that the OG query doesn't update]

        articlesToPush = userlist.ArticlesToPush

        returnList = getArticleInformation(articlesToPush)

        return ArticleListOut(items= returnList)
    @endpoints.method(message_types.VoidMessage, TestReturn,
                      name='user.test',
                      path='test',
                      http_method='GET')
    def test(self, request):
        BASE_URL = 'https://news.ycombinator.com'
        url = '%s/%s' % (BASE_URL, '')
        result = urlfetch.fetch(url, deadline=45, method=urlfetch.HEAD)
        #content = BeautifulSoup(result.content)
        return TestReturn(field=result.content)

application = endpoints.api_server([HackerFeedApi])
populateArticleDB(100)