from hn import HN   # Maybe use th


def get_top_articles(n):
    """
    Retrieves top n articles using hacker news API
    returns a list of dictionaries, dicts represent article
    """
    hn = HN()
    type = ''
    stories = hn.get_stories(story_type=type, limit=n)
    article_list = []
    for article in stories:
        article_dict = {'id': str(article.story_id), 'title': article.title, 'points': article.points,
                        'comments': article.comments_link, 'submitter': article.submitter, 'url': article.link,
                        'self': article.is_self, 'domain': article.domain, 'profile': article.submitter_profile,
                        'time': article.published_time, 'num_comments': article.num_comments, 'rank': article.rank}
        article_list.append(article_dict)
    return article_list  # this is a list of story objects


def get_new_articles(n):
    """
    Retrieves n newest articles
    returns a list of dictionaries, dicts represent article
    """
    hn = HN()
    type = 'newest'
    stories = hn.get_stories(story_type=type, limit=n)
    article_list = []
    for article in stories:
        article_dict = {'id': article.story_id, 'title': article.title, 'points': article.points,
                        'comments': article.comments_link, 'submitter': article.submitter, 'url': article.link,
                        'self': article.is_self, 'domain': article.domain, 'profile': article.submitter_profile,
                        'time': article.published_time, 'num_comments': article.num_comments, 'rank': article.rank}
        article_list.append(article_dict)
    return article_list


def get_best_articles(n):
    """
    Retrieves n best articles
    returns a list of dictionaries, dicts represent article
    """
    hn = HN()
    type = 'best'
    stories = hn.get_stories(story_type=type, limit=n)
    article_list = []
    for article in stories:
        article_dict = {'id': article.story_id, 'title': article.title, 'points': article.points,
                        'comments': article.comments_link, 'submitter': article.submitter, 'url': article.link,
                        'self': article.is_self, 'domain': article.domain, 'profile': article.submitter_profile,
                        'time': article.published_time, 'num_comments': article.num_comments, 'rank': article.rank}
        article_list.append(article_dict)
    return article_list


def main():
    while(True):
        mode = raw_input('Enter input mode (t,n,b,l) (q to quit): ')
        if mode == 'q':
            break
        else:
            n = raw_input('Number of articles?: ')
            try:
                n = int(n)
            except ValueError:
                print 'Please enter an integer for number of articles.'
                continue
            if mode == 't':
                list = get_top_articles(n)
                for story in list:
                    print story
            if mode == 'b':
                list = get_best_articles(n)
                for story in list:
                    print story
            if mode == 'n':
                list = get_new_articles(n)
                for story in list:
                    print story


if __name__ == "__main__":
    main()