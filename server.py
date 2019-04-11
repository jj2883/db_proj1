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
import psycopg2
from psycopg2.extensions import AsIs
from sqlalchemy_utils import database_exists, create_database
from flask.views import MethodView

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response



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
#DATABASEURI = "postgresql://jad2267:jj2883@34.73.21.127/proj1part2"
DATABASEURI = "postgresql://jj2883:2360@34.73.21.127/proj1part2"



engine = create_engine(DATABASEURI,isolation_level="AUTOCOMMIT")

engine.execute(open("tables.sql", "r").read())
engine.execute(open("data.sql", "r").read())



@app.before_request
def before_request():

  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):

  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def index():

  names = ['Team','Player', 'Game', 'Statline']
  context = dict(entities = names)


 
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
        if name == 'player':
            # Need %% to escape %
#            query = "SELECT * FROM player p, team t,  (select * from play_for_) pf where p.player_id = pf.player_id AND t.team_id=pf.team_id like %s;"
            query = "SELECT * FROM player p, team t, (select * from play_) pl, (select * from statline) s, (select * from play_for_) pf where p.player_id = pf.player_id AND t.team_id=pf.team_id AND pl.home_team_id=t.team_id AND pl.away_team_id = t.team_id AND s.game_id =pl.game_id AND s.player_id=p.player_id;"
            # print query
            cursor = g.conn.execute(query, (search_ph,))
#            cursor = g.conn.execute(query)
        elif name == 'team':
            query = "SELECT * FROM player p, game g, coach c, team t,(select * from coaches_ ) co, (select * from play_for_)pf, (select * from play_)pl where p.player_id=t.player_id AND pl.home_team_id=t.team_id and pl.away_team_id=t.team_id and co.team_id = t.team_id;"
            #query = "SELECT * FROM artist a, album al, (select a_id, al_id from contributes_to) c WHERE a.a_id = c.a_id AND al.al_id = c.al_id AND a.a_name LIKE %s;"
            # print query
            cursor = g.conn.execute(query, (search_ph,))
        elif name == 'statline':
#            query = "SELECT * FROM artist a, song s, (select a_id, s_id from contributes_to) c WHERE a.a_id = c.a_id AND s.s_id = c.s_id AND s.s_name LIKE %s;"
            query = "SELECT * FROM player p, team t, (select * from play_) pl, (select * from statline) s, (select * from play_for_) pf where p.player_id = pf.player_id AND t.team_id=pf.team_id AND pl.home_team_id=t.team_id AND pl.away_team_id = t.team_id AND s.game_id =pl.game_id AND  s.player_id=p.player_id;"
            # print query
            cursor = g.conn.execute(query, (search_ph,))
        elif name == 'game':
            query = "SELECT * FROM player p, team t, (select * from play_) pl, (select * from statline) s, (select * from play_for_) pf where p.player_id = pf.player_id AND t.team_id=pf.team_id AND pl.home_team_id=t.team_id AND pl.away_team_id = t.team_id AND s.game_id =pl.game_id AND s.player_id=p.player_id;"
#            query = "SELECT * FROM song s, genre g, belongs_to b WHERE s.s_id = b.s_id AND b.g_id = g.g_id AND g.g_name LIKE %s;"
            # print query
            cursor = g.conn.execute(query, (search_ph,))

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