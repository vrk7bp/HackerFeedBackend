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
import sys
sys.path.append("C:\Users\Student\PycharmProjects\DBBackend\python_scripts")
import Recommender
import Structures
from protorpc import messages
from protorpc import remote
import json
import collections
from google.appengine.ext import ndb


class UsersList(ndb.Model):
    UserID = ndb.StringProperty(required=True)
    ArticlesRead = ndb.JsonProperty()
    ArticlesPush = ndb.JsonProperty()


class UserID(messages.Message):
    id = messages.StringField(1, required=True)


class Articles(messages.Message):
    id = messages.StringField(1, required=True)
    userLiked = messages.BooleanField(2, required=True)


class UserIDAndArticles(messages.Message):
    id = messages.StringField(1, required=True)
    items = messages.MessageField(Articles, 2, repeated=True)


class ArticleList(messages.Message):
    items = messages.MessageField(Articles, 1, repeated=True)

#Just a test method so that I could test the dataStore retrieval
def insertToDB2():
        list1 = [collections.OrderedDict({'id': '1', 'userLiked': True}), collections.OrderedDict({'id': '2', 'userLiked': True})]
        list2 = [collections.OrderedDict({'id': '3', 'userLiked': True}), collections.OrderedDict({'id': '4', 'userLiked': True})]
        list3 = [collections.OrderedDict({'id': '5', 'userLiked': True}), collections.OrderedDict({'id': '6', 'userLiked': True})]
        list4 = [collections.OrderedDict({'id': '7', 'userLiked': True}), collections.OrderedDict({'id': '8', 'userLiked': True})]
        UsersList(UserID='One', ArticlesRead=json.dumps(list1), ArticlesPush=json.dumps(list2)).put()
        UsersList(UserID='Two', ArticlesRead=json.dumps(list3), ArticlesPush=json.dumps(list4)).put()

#Have to create a method here that retrieves from the API the top 200 articles in default order
def defaultList():
    list1 = [collections.OrderedDict({'id': '11', 'userLiked': False}), collections.OrderedDict({'id': '12', 'userLiked': True})]
    return list1


@endpoints.api(name='hackerFeed', version='v1',
               description='API for Hacker Feed Application')
class HackerFeedApi(remote.Service):

    @endpoints.method(UserID, ArticleList,
                      name='user.articlePush',
                      path='articlesPush',
                      http_method='GET')
    def get_articles_push(self, request):
        uid = request.id
        userlist = UsersList.query(UsersList.UserID == uid).get()
        if userlist is None:
            raise endpoints.NotFoundException('List for user ID %s not found' % uid)

        return ArticleList(items = json.loads(userlist.ArticlesPush))

    @endpoints.method(UserID, ArticleList,
                      name='user.articleRead',
                      path='articlesRead',
                      http_method='GET')
    def get_articles_read(self, request):
        uid = request.id
        userlist = UsersList.query(UsersList.UserID == uid).get()
        if userlist is None:
            raise endpoints.NotFoundException('List for user ID %s not found' % uid)

        return ArticleList(items = json.loads(userlist.ArticlesRead))

    @endpoints.method(UserID, ArticleList,
                      name='user.newUser',
                      path='new_user',
                      http_method='POST')
    def new_user(self, request):
        articleList = defaultList()
        e = UsersList(UserID = request.id,
                      ArticlesRead= json.dumps([]),
                      ArticlesPush= json.dumps(articleList))
        e.put()

        return ArticleList(items = articleList)

    @endpoints.method(UserIDAndArticles, ArticleList,
                      name='user.update',
                      path='update',
                      http_method='POST')
    def get_update(self, request):
        # get UsersList entity and raise an exception if none found.
        uid = request.id
        userlist = UsersList.query(UsersList.UserID == uid).get()
        if userlist is None:
            raise endpoints.NotFoundException('List for user ID %s not found' % uid)

        list = json.loads(userlist.ArticlesRead)
        for item in request.items:
            dict = collections.OrderedDict({})
            dict['id'] = item.id
            dict['userLiked'] = item.userLiked
            list.append(dict)
        userlist.ArticlesRead = json.dumps(list)
        userlist.put()

        #put command to update push list here...

        #query2 = UsersList.query(UsersList.UserID == userID) [this is in case that the OG query doesn't update]

        return ArticleList(items= json.loads(userlist.ArticlesPush))

application = endpoints.api_server([HackerFeedApi])