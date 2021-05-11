import flask
from flask import request, jsonify, Blueprint
import sqlite3
import asyncio
import random
import GetApiVnxpress
import threading
#from flask_swagger_ui import get_swaggerui_blueprint


print("function of Server")
app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#root link
@app.route('/', methods=['GET'])
def home():
    return '''<h1>SCAN API WEB</h1>
            <p>HERE IS SERVER SUPPORT FOR SCAN API WEBSITE</p>'''


#get all domain exists in database
@app.route('/api/resources/domain/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    allDomain = cur.execute('SELECT * FROM DOMAIN;').fetchall()
    return jsonify(allDomain)

#define error return 
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

#get domain exist in database
@app.route('/api/resources/domain/', methods=['GET'])
def api_filter():
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query_parameters = request.args
    id = query_parameters.get('id')
    domain = query_parameters.get('domain')
    query = "SELECT * FROM DOMAIN WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if domain:
        query += ' domain=? AND'
        to_filter.append(domain)

    if not (id or domain):
        return page_not_found(404)

    query = query[:-4] + ';'
    print("query[:-4]", query[:-4])
    print("query: ", query)
    results = cur.execute(query, to_filter).fetchall()
    return jsonify(results)

#get item test exist in database
@app.route('/api/resources/domain/test', methods=['GET'])
def api_filterTest():
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query_parameters = request.args
    id = query_parameters.get('id')
    domain = query_parameters.get('domain')
    query = "SELECT test.information FROM test JOIN DOMAIN ON test.parent_id = DOMAIN.id WHERE"
    to_filter = []

    if id:
        query += ' DOMAIN.id=? AND'
        to_filter.append(id)
    if domain:
        query += ' DOMAIN.domain=? AND'
        to_filter.append(domain)

    if not (id or domain):
        return page_not_found(404)

    query = query[:-4] + ';'
    print("query[:-4]", query[:-4])
    print("query: ", query)
    results = cur.execute(query, to_filter).fetchall()
    return jsonify(results)

#get item API exist in database
@app.route('/api/resources/domain/API', methods=['GET'])
def api_filterAPI():
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query_parameters = request.args
    id = query_parameters.get('id')
    domain = query_parameters.get('domain')
    query = "SELECT * FROM API JOIN DOMAIN ON API.domain_id = DOMAIN.id WHERE"
    to_filter = []

    if id:
        query += ' DOMAIN.id=? AND'
        to_filter.append(id)
    if domain:
        query += ' DOMAIN.domain=? AND'
        to_filter.append(domain)

    if not (id or domain):
        return page_not_found(404)

    query = query[:-4] + ';'
    print("query[:-4]", query[:-4])
    print("query: ", query)
    results = cur.execute(query, to_filter).fetchall()
    return jsonify(results)

#run get API of web
@app.route('/api/resources/domain/API/run', methods=['GET'])
def api_getAPI():
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query_parameters = request.args
    id = query_parameters.get('id')
    depth = int(query_parameters.get('depth'))
    print(type(depth))
    domain = query_parameters.get('domain')
    query = "SELECT DOMAIN.domain FROM DOMAIN WHERE"
    to_filter = []

    if id:
        query += ' DOMAIN.id=? AND'
        to_filter.append(id)
    if domain:
        query += ' DOMAIN.domain=? AND'
        to_filter.append(domain)

    if not (id or domain):
        return page_not_found(404)

    query = query[:-4] + ';'
    print("query[:-4]", query[:-4])
    print("query: ", query)
    results = cur.execute(query, to_filter).fetchall()
    #run scan API
    try:
        threadHref = threading.Thread(target=GetApiVnxpress.funtionForHrefElement, args=(depth, results[0]['domain'],), daemon=True)
        threadHref.start()
    except Exception as e:
        print("main api scan: ", e)
        pass
    return jsonify(results)

#post domain to database
@app.route('/api/post/domain', methods = ['POST'])
def api_post():
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    insert_parameters = request.args
    domain = insert_parameters.get('domain')
    query = "SELECT DOMAIN.id FROM DOMAIN where DOMAIN.domain ==?;"
    domainExist = cur.execute(query, [domain,]).fetchall()
    if len(domainExist) > 0:
        resp = jsonify('domain is exist!')      
        resp.status_code = 200
        return resp

    else:
        cur.execute("INSERT INTO DOMAIN (domain) VALUES(?)",(domain,))
        conn.commit()
        resp = jsonify('User added successfully!')      
        resp.status_code = 200
        return resp


if __name__ == '__main__':
    app.run()