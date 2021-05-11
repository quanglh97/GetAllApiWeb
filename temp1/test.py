import flask
from flask import request, jsonify, Blueprint
import sqlite3
import asyncio
import random
import GetApiVnxpress
import threading
from fastapi import FastAPI
import uvicorn
from typing import Optional

app = FastAPI()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#root link
@app.get("/")
async def home():
    return '''<h1>SCAN API WEB</h1>
            <p>HERE IS SERVER SUPPORT FOR SCAN API WEBSITE</p>'''


#get all domain exists in database
@app.get('/api/resources/domain/all')
def api_all():
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    allDomain = cur.execute('SELECT * FROM DOMAIN;').fetchall()
    return allDomain

#get domain exist in database
@app.get('/api/resources/domain/')
def api_filter(id: Optional[str] = None, domain: Optional[str] = None):
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    # query_parameters = request.args
    # id = query_parameters.get('id')
    # domain = query_parameters.get('domain')
    query = "SELECT * FROM DOMAIN WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if domain:
        query += ' domain=? AND'
        to_filter.append(domain)

    query = query[:-4] + ';'
    print("query[:-4]", query[:-4])
    print("query: ", query)
    results = cur.execute(query, to_filter).fetchall()
    return results

# #get item API exist in database
@app.get('/api/resources/domain/API')
async def api_filterAPI(id: Optional[str] = None, domain: Optional[str] = None):
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    # query_parameters = request.args
    # id = query_parameters.get('id')
    # domain = query_parameters.get('domain')
    query = "SELECT * FROM API JOIN DOMAIN ON API.domain_id = DOMAIN.id WHERE"
    to_filter = []
    if id:
        query += ' DOMAIN.id=? AND'
        to_filter.append(id)
    if domain:
        query += ' DOMAIN.domain=? AND'
        to_filter.append(domain)

    query = query[:-4] + ';'
    print("query[:-4]", query[:-4])
    print("query: ", query)
    results = cur.execute(query, to_filter).fetchall()
    return results

# #run get API of web
@app.get('/api/resources/domain/API/run')
async def api_getAPI(depth: int, id: Optional[str]=None, domain: Optional[str]= None):
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

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
        print("API scan: ", e)
    return results

# #post domain to database
@app.post('/api/post/domain')
def api_post(domain: str):
    conn = sqlite3.connect('GET_API_DATABASE.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    # insert_parameters = request.args
    # domain = insert_parameters.get('domain')
    query = "SELECT DOMAIN.id FROM DOMAIN where DOMAIN.domain ==?;"
    domainExist = cur.execute(query, [domain,]).fetchall()
    if len(domainExist) > 0:
        resp = 'domain is exist!'     
        return resp

    else:
        cur.execute("INSERT INTO DOMAIN (domain) VALUES(?)",(domain,))
        conn.commit()
        resp = 'User added successfully!'  
        return resp


if __name__  == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port = 8005)