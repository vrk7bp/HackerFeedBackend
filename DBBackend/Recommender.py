from __future__ import division  # makes integer division not round
# to do 'normal' integer division, do int1//int2
from Structures import User_Article
import copy


def same_sign(a, b):
    """ This checks if numbers a and b have the same sign """
    # TODO: What to do in the zero case?
    flag = (a <= 0 and b <= 0) or (a >= 0 and b >= 0) #or (a == 0 and b == 0)
    return flag


def compare_articles(art1, art2):
    """ This computes if 2 articles have similar ratings """
    difference = abs(abs(art1.rating) - abs(art2.rating))
    if same_sign(art1.rating, art2.rating):
        return 1-difference
    else:
        return -1+difference


def compare_two_users(user1, user2):
    """ This function compares two users, returning their compatibility as a float """
    running_sum = 0
    articles_in_common = 0
    for art1 in user1.read_articles:
        for art2 in user2.read_articles:
            if art1.id == art2.id:  # if the articles are the same, modeled by User_Article objects
                articles_in_common += 1
                diff = compare_articles(art1, art2)
                if diff > abs(.5):
                    diff *= 2  # may need to rethink this - max value is now +/- 2 - just divide by 2
                running_sum += diff
                break
    return running_sum/articles_in_common  # average all ratings


def compare_all_users(target_user, user_list, user_dict):
    """
    This function compares one user to all other users
    Target User is the user you want to get comparisons for
    user_list is a list of all users
    user dict holds all comparison values between every user.
    """
    user_dict[target_user] = []  # flush old values
    for user in user_list:
        if user != target_user:
            closeness = compare_two_users(target_user, user)
            user_dict[target_user].append((user, closeness))


def create_matrix(user_list):
    """
    Generate closeness values for all users in the user list
    """
    user_dict = {}
    for user in user_list:
        compare_all_users(user, user_list, user_dict)
    return user_dict


def get_new_articles(target_user, user_dict):
    """
    Generates new articles for the target user given a dictionary full of closness values
    returns nothing, but target_user's unread article set is replenished
    """
    # This could probably be optimized tonnes TODO
    user_list = user_dict[target_user]
    article_set = set()
    for user_tup in user_list:
        closeness = user_tup[1]
        articles = copy.deepcopy(user_tup[0].read_articles)
        if closeness > 0:  # if their tastes are similar enough
            for art in articles:
                art.rating = closeness
            article_set.union(articles)
    # Get new, unread articles into the target_user's queue
    target_user.unread_articles = target_user.unread_articles | article_set
    target_user.unread_articles = target_user.unread_articles - target_user.read_articles
    # best matches are at the front of the list
    return sorted(target_user.unread_articles, reverse=True, key= lambda article : article.rating)


def append_new_user(new_user, user_dict):
    user_dict[new_user] = []
    user_list = user_dict.keys()
    compare_all_users(new_user, user_list, user_dict)


def run_user_update(target_user, user_dict, article_list):
    """
    article_list is a list like [ {'id': int, 'rating':int}, {}, {}, {} ]
    """
    for article in article_list:
        target_user.read_articles(article['id'], article['rating'])
    compare_all_users(target_user, user_dict.keys(), user_dict)
    return get_new_articles(target_user, user_dict)




def test():  # my shitty testing function
    art_list = [
        User_Article('101', -.7),
        User_Article('1', .5),
        User_Article('99', 1),
        User_Article('55', -1),
        User_Article('61', -.3)
    ]
    print art_list
    print sorted(art_list)
    print sorted(art_list, reverse=True)
    print sorted(art_list, key=lambda article : article.rating)
    print sorted(art_list, reverse=True, key=lambda article : article.rating)


if __name__ == '__main__':
    test()