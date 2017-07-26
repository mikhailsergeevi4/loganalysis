# Python 2.7.3 (default, Oct 26 2016, 21:04:23)

import psycopg2

DB_NAME = "news"
# Views for single queries
# Article rank
view_ranking_articles = """create view ranking_articles as
                        select title, count(log.id) as number_of_views
                        from articles, log
                        where log.path = concat('/article/', articles.slug)
                        group by articles.title
                        order by number_of_views desc;
                        """
# Articles from one authon
view_articles_from_one_author = """
                                create view articles_from_one_author as
                                select title, name
                                from articles, authors
                                where articles.author = authors.id;
                                """
# Error status
view_status_error = """
                    create view status_error as
                    select date(time) as day,
                    cast(count(status) as float) as number_of_errors
                    from log
                    where not status='200 OK'
                    group by day
                    order by day;
                    """

# Al statuses
view_status_all = """
                 create view status_all as
                 select date(time) as day,
                 cast(count(status) as float) as status_all_sum
                 from log
                 group by day
                 order by day;
                 """
# queries for answer a question
query_for_question_one = view_ranking_articles + """
                          select * from ranking_articles limit 3;
                          """

query_for_question_two = view_ranking_articles + view_articles_from_one_author + """
                        select name, sum(ranking_articles.number_of_views)
                        as views
                        from articles_from_one_author, ranking_articles
                        where
                        articles_from_one_author.title = ranking_articles.title
                        group by name order by views desc;
                        """
query_for_question_three = view_status_error + view_status_all + """
                          select status_error.day,
                          round(
                          ((status_error.number_of_errors/status_all.status_all_sum)
                          * 100)::decimal, 2)
                          as percentage
                          from status_error, status_all
                          where status_all.day = status_error.day
                          and (((status_error.number_of_errors/
                          status_all.status_all_sum) * 100) > 1.0)
                          order by status_error.day;
                          """


def send_query(query):
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


def print_results_query_one(results):
    print "The most popular three articles of all time"
    for i in results:
        print '"' + i[0] + '" with ' + str(i[1]) + ' views'


def print_results_query_two(results):
    print " "
    print "The most popular article authors of all time"
    for i in results:
        print i[0] + ' - ' + str(i[1]) + ' views'


def print_results_query_three(results):
    print " "
    print "Days with more than 1% of requests lead to errors"
    for i in results:
        print str(i[0]) + ' - ' + str(i[1]) + " % errors"


print_results_query_one(send_query(query_for_question_one))
print_results_query_two(send_query(query_for_question_two))
print_results_query_three(send_query(query_for_question_three))
