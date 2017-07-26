This is the **Log Analysis project** in **Udacity Full Stack Web Developer Nanodegree**.

You will need:

 1. Python (I wrote in 2.7 version)
 2. Vagrant
 3. VirtualBox

How to start:

 - Start the Virtual Machine (*vagrant up*)
 - Log into it (*vagrant ssh*)
 - Download file from (*[Udacity](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)*)
 - Unzip it. The file inside is called *newsdata.sql*. Put this file into the *vagrant* directory, which is shared with your virtual machine.
 - Load the data, use the command *psql -d news -f newsdata.sql*
 - Clone or dowload this repo inside the same directory
 - **Run the queries!!! (*python app.py*)**

----------
I have made some views and store it in app.py, you can take a look on they here:
# Article rank

> view_ranking_articles = """create view ranking_articles as
>                         select title, count(log.id) as number_of_views
>                         from articles, log
>                         where log.path = concat('/article/', articles.slug)
>                         group by articles.title
>                         order by number_of_views desc;
>                         """

# Articles from one authon

> view_articles_from_one_author = """
>                                 create view articles_from_one_author as
>                                 select title, name
>                                 from articles, authors
>                                 where articles.author = authors.id;
>                                 """

# Error status

> view_status_error = """
>                     create view status_error as
>                     select date(time) as day,
>                     cast(count(status) as float) as number_of_errors
>                     from log
>                     where not status='200 OK'
>                     group by day
>                     order by day;
>                     """

# All statuses

> view_status_all = """
>                  create view status_all as
>                  select date(time) as day,
>                  cast(count(status) as float) as status_all_sum
>                  from log
>                  group by day
>                  order by day;
>                  """
