#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from sqlalchemy_utils import database_exists, create_database


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.18.7/w4111
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.18.7/w4111"
#
DATABASEURI = "postgresql://jad2267:jj2883@34.73.21.127/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI, isolation_level="AUTOCOMMIT")
if not database_exists(engine.url):
    create_database(engine.url)
    engine.execute(open("tables.sql", "r").read())
    engine.execute(open("data.sql", "r").read())
#    print True
#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  #print request.args


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
  names = []
  for result in cursor:
    names.append(result[0])  # can also be accessed using result[0]

    entities = [i for i in names_ if '_' not in i]
    # relations = [i for i in names_ if '_' in i]
    entities = sorted(entities)
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(entities = entities)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)



class List_Search(MethodView):

    # methods = ['GET', 'POST']

    # def dispatch_request(self, name):
    #     return 'Hello %s!' % name

    def get(self, name):
        if request.method != 'POST':
            '''
            # Get table fields
            field_query = "SELECT column_name FROM information_schema.columns WHERE table_name = %s;"
            cursor_field = g.conn.execute(field_query, (name,))
            fields = []
            for field in cursor_field:
                fields.append(field)
            cursor_field.close()
            '''
            # http://stackoverflow.com/questions/13793399/passing-table-name-as-a-parameter-in-psycopg2
            # Get table entries
            query = "SELECT * FROM %(table)s;"
            cursor = g.conn.execute(query, {"table": AsIs(name)})
            table = []
            for cells in cursor:
                table.append(cells)
            # Get table fields, http://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.ResultProxy
            fields = cursor.keys()
            # Format fields correctly
            fields = [(f,) for f in fields]
            cursor.close()
            table = sorted(table)
            context = dict(t_name=str(name), table=table, fields=fields)
            if '_' not in name:
                return render_template("entities.html", **context)
            else:
                return render_template("relations.html", **context)

    def post(self, name):
        # print name
        search = request.form['search']
        search_ph = search + '%%'
        name = name.lower()
        # print search
        if name == 'team':
            # Need %% to escape %
            query = "SELECT * FROM team t LIKE %s;"
            #query = "SELECT * FROM artist a, album al, (select a_id, al_id from contributes_to) c WHERE a.a_id = c.a_id AND al.al_id = c.al_id AND al.al_name LIKE %s;"
            # print query
            cursor = g.conn.execute(query, (search_ph,))
        elif name == 'player':
            query = "SELECT * FROM playerr p  LIKE %s;"
            #query = "SELECT * FROM artist a, album al, (select a_id, al_id from contributes_to) c WHERE a.a_id = c.a_id AND al.al_id = c.al_id AND a.a_name LIKE %s;"
            # print query
            cursor = g.conn.execute(query, (search_ph,))
        # elif name == 'song':
        #     query = "SELECT * FROM artist a, song s, (select a_id, s_id from contributes_to) c WHERE a.a_id = c.a_id AND s.s_id = c.s_id AND s.s_name LIKE %s;"
        #     # print query
        #     cursor = g.conn.execute(query, (search_ph,))
        # elif name == 'genre':
        #     query = "SELECT * FROM song s, genre g, belongs_to b WHERE s.s_id = b.s_id AND b.g_id = g.g_id AND g.g_name LIKE %s;"
        #     # print query
        #     cursor = g.conn.execute(query, (search_ph,))
        # elif name == 'label':
        #     query = "SELECT * FROM artist a, label l, has_signed h WHERE a.a_id = h.a_id AND l.l_id = h.l_id AND l.l_name LIKE %s;"
        #     # print query
        #     cursor = g.conn.execute(query, (search_ph,))
        # elif name == 'playlist':
        #     query = "SELECT * FROM playlist p, contains_ c, song s WHERE p.p_id = c.p_id AND c.s_id = s.s_id AND p.p_name LIKE %s;"
        #     # print query
        #     cursor = g.conn.execute(query, (search_ph,))
        # else:
        #     query = "SELECT * FROM artist a, performs_at p, concert c WHERE p.a_id = a.a_id AND p.c_id = c.c_id AND c.c_name LIKE %s;"
        #     # print query
        #     cursor = g.conn.execute(query, (search_ph,))
        # Get fields
        _fields = cursor.keys()
        # print _fields
        # Get unique set of fields
        # fields = sorted(list(set(_fields))) not used as order is not maintained
        fields = []
        for x in _fields:
            if x not in fields:
                fields.append(x)
        # print fields
        output = []
        for result in cursor:
            row = ()
            for f in fields:
                # print result[f]
                row += (result[f],)
            output.append(row)
        output = sorted(output)
        # Format fields correctly, but only after to prevent type issues
        fields = [(f,) for f in fields]
        cursor.close()
        context = dict(search=str(search), t_name=str(name).title(), table=output, fields=fields)
        return render_template("search.html", **context)


ListSearch_View = List_Search.as_view('List_Table')
# Can always use defaults={'search': None} as a arg if need be
app.add_url_rule('/<name>', view_func=ListSearch_View)
app.add_url_rule('/<name>/search', view_func=ListSearch_View)


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
      """
      This function handles command line parameters.
      Run the server using
          python server.py
      Show the help text using
          python server.py --help
      """

      HOST, PORT = host, port
      print "running on %s:%d" % (HOST, PORT)
      app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()

# #
# # This is an example of a different path.  You can see it at:
# # 
# #     localhost:8111/another
# #
# # Notice that the function name is another() rather than index()
# # The functions for each app.route need to have different names
# #
# @app.route('/another')
# def another():
#   return render_template("another.html")


# # Example of adding new data to the database
# @app.route('/add', methods=['POST'])
# def add():
#   name = request.form['name']
#   g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
#   return redirect('/')


# @app.route('/login')
# def login():
#     abort(401)
#     this_is_never_executed()


# if __name__ == "__main__":
#   import click

#   @click.command()
#   @click.option('--debug', is_flag=True)
#   @click.option('--threaded', is_flag=True)
#   @click.argument('HOST', default='0.0.0.0')
#   @click.argument('PORT', default=8111, type=int)
#   def run(debug, threaded, host, port):
#     """
#     This function handles command line parameters.
#     Run the server using:

#         python server.py

#     Show the help text using:

#         python server.py --help

#     """

#     HOST, PORT = host, port
#     print "running on %s:%d" % (HOST, PORT)
#     app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


#   run()
