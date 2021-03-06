#coding=utf8

from django.shortcuts import render

from django.http import HttpResponse
import datetime
from Utils.SearchResultHub import SearchResultHub
from Utils import LogParser
from Utils import AnnoLogParser
from Utils import SessionAnnoLogParser
from Utils import QuestionnaireLogParser
from Utils import QuerySatisfactionLogParser
from Utils import SERPAnalyzer
from Utils import RecordAnnoLogParser
from Utils import RelAnnoLogParser
from Utils.LogHub import LogHub
from django.template import loader
from django.shortcuts import render_to_response
from django import template
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, models
import random

import sys
import urllib
from anno.models import Task
from anno.models import RecordFile
reload(sys)
def hello(request):
    return HttpResponse('hello world')

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def search(request, taskid, query, pageid):

    # print 'view search', query
    srh = SearchResultHub()
    query = urllib.unquote(query)

   # query = query.decode('cp936','ignore').decode('utf8')

    # print urllib.quote(query)
    results = srh.getResult(query, 10*(int(pageid)-1), 10)
    results_count = srh.getCount(query)
    max_pageid = results_count / 10

    t = template.Template(open('templates/out.html').read())
    next_pageid = ''
    if int(pageid) < max_pageid:
        next_pageid = str(int(pageid)+1)
    page_str = ''.join([str(x) for x in range(1, max_pageid+1)])
    c = template.Context({'resultlist': [r.content for r in results],
                          'taskid': taskid,
                          'query': query,
                          'pageid': pageid,
                          'page_str': page_str,
                          'next_pageid': next_pageid})
    # fout = open('temp/test.html','w')
    # fout.write(t.render(c).decode('utf8','ignore').encode('utf8'))
    # fout.close()
    return HttpResponse(t.render(c))


def show_page(request, taskid, query, pageid):
    srh = SearchResultHub()
    query = urllib.unquote(query)

    results = srh.getResult(query, 10*(int(pageid)-1), 10)
    results_count = srh.getCount(query)
    max_pageid = results_count / 10

    t = template.Template(open('templates/out_page.html').read())
    next_pageid = ''
    if int(pageid) < max_pageid:
        next_pageid = str(int(pageid)+1)
    page_str = ''.join([str(x) for x in range(1, max_pageid+1)])
    result_list = SERPAnalyzer.add_character_bounding_box(results)
    c = template.Context({'resultlist': result_list,
                          'taskid': taskid,
                          'query': query,
                          'pageid': pageid,
                          'page_str': page_str,
                          'next_pageid': next_pageid})
    # fout = open('temp/test.html','w')
    # fout.write(t.render(c).decode('utf8','ignore').encode('utf8'))
    # fout.close()
    return HttpResponse(t.render(c))


def train(request,userid):
    html = '<html><body> It is the '+userid +' train task </body></html>'
    return HttpResponse(html)
def validate(request,taskid):
    html = '<html><body> It is the '+taskid +' task. </body></html>'
    return HttpResponse(html)

def login(request):
    return HttpResponse(open('templates/login.html').read())

def tasks(request, sID):
    tlist = list(Task.objects.filter(task_id__lte=12))
    if sID == '2013310564':
        tlist = [Task.objects.get(task_id=13)]
    random.seed(int(sID))
    random.shuffle(tlist)
    print 'len tlist', len(tlist)
    for t in tlist:
        print t.task_id
    html = template.Template(open('templates/tasks.html').read())
    c = template.Context({'tasks':tlist,'tasknum':len(tlist)})
    respon = HttpResponse(html.render(c))
    respon.set_cookie('studentID', value=sID, max_age=None, expires=None, path='/', domain=None, secure=None)
    return respon

def annolist(request, taskid):
    try:
        studentID = request.COOKIES['studentID']
    except:
        return HttpResponse('ERROR: UNKNOWN STUDENT ID')
    lh = LogHub()
    queries = lh.getQueriesWithSIDandTaskID(studentID,int(taskid))
    html = template.Template(open('templates/annolist.html').read())
    c = template.Context({'querynum': len(queries), 'taskid': taskid, 'querylist': queries})
    return HttpResponse(html.render(c))


def annotation(request, taskid, query):
    try:
        studentID = request.COOKIES['studentID']
    except:
        return HttpResponse('ERROR: UNKNOWN STUDENT ID')
    lh = LogHub()
    results = lh.getClickedResults(studentID, taskid, query)
    # print 'len result:', len(results)
    t = template.Template(open('templates/annotation.html').read())
    c = template.Context({'resultlist': [r.content for r in results],
                          'taskid': taskid,
                          'query': query})
    return HttpResponse(t.render(c))


def questionnaire(request, task_id):
    task = Task.objects.get(task_id=int(task_id))
    t = template.Template(open('templates/questionnaire.html').read())
    c = template.Context({'task': task})
    return HttpResponse(t.render(c))


def description(request, task_id, init_query):
    task = Task.objects.get(task_id=int(task_id))
    t = template.Template(open('templates/description.html').read())
    c = template.Context({'task': task, 'initQuery': init_query})
    return HttpResponse(t.render(c))


def list_all_queries(request):
    results = LogParser.get_queries(None)
    t = template.Template(open('templates/queries.html').read())
    c = template.Context({'queries': results})
    return HttpResponse(t.render(c))


@csrf_exempt
def log(request):
    message = urllib.unquote(request.POST[u'message']).encode('utf8')
    # print message
    # print type(message)
    LogParser.insertMessageToDB(message)
    return HttpResponse('OK')


@csrf_exempt
def log_annotation(request):
    message = urllib.unquote(request.POST[u'message'])
    # print message
    AnnoLogParser.insertMessageToDB(message)
    return HttpResponse('OK')


@csrf_exempt
def log_session_annotation(request):
    message = urllib.unquote(request.POST[u'message'])
    # print message
    SessionAnnoLogParser.insertMessageToDB(message)
    return HttpResponse('OK')


@csrf_exempt
def log_questionnaire(request):
    message = urllib.unquote(request.POST[u'message'])
    # print message
    QuestionnaireLogParser.insertMessageToDB(message)
    return HttpResponse('OK')

@csrf_exempt
def log_query_satisfaction(request):
    message = urllib.unquote(request.POST[u'message'])
    # print message
    QuerySatisfactionLogParser.insertMessageToDB(message)
    return HttpResponse('OK')

@csrf_exempt
def log_record_annotation(request):
    message = urllib.unquote(request.POST[u'message'])
    print message
    RecordAnnoLogParser.insertMessageToDB(message)
    return HttpResponse('OK')


@csrf_exempt
def debug_log(request):
    message = urllib.unquote(request.POST[u'message'])
    print message
    fout = open('log.txt', 'a')
    print >>fout, message.encode('utf8')
    return HttpResponse('OK')


def recordannolist(request, annotatorID):
    respon = HttpResponse(open('templates/recordannolist.html').read())
    respon.set_cookie('annotatorID', value=annotatorID, max_age=None, expires=None, path='/', domain=None, secure=None)
    return respon


def recordanno(request,task_id):
    t = template.Template(open('templates/recordanno.html').read())
    print task_id,type(task_id)
    rlist = list()
    r = list(RecordFile.objects.filter(task_id=int(task_id)))
    random.seed()
    random.shuffle(r)
    task = Task.objects.get(task_id=int(task_id))
    c = template.Context({'task':task, 'records' : r})
    respon = HttpResponse(t.render(c))
    return respon


def init_query_list(request, annotatorID):
    t = template.Template(open('templates/init_queries.html').read())
    tlist = list(Task.objects.filter(task_id__lte=12))
    c = template.Context({'tasks': tlist, 'tasknum': len(tlist)})
    response = HttpResponse(t.render(c))
    response.set_cookie('annotatorID', value=annotatorID, max_age=None, expires=None, path='/', domain=None, secure=None)
    return response


def rel_annotation(request, taskid, query):
    try:
        annotatorID = request.COOKIES['annotatorID']
    except ValueError:
        return HttpResponse('ERROR: UNKNOWN annotator ID')
    lh = LogHub()
    results = lh.getViewedResults(taskid, query)
    # print 'len result:', len(results)
    task = Task.objects.filter(task_id=int(taskid))[0]
    t = template.Template(open('templates/rel_annotation.html').read())
    c = template.Context({'resultlist': [r.content for r in results],
                          'task_desc': task.content,
                          'taskid': taskid,
                          'query': query})
    return HttpResponse(t.render(c))


@csrf_exempt
def log_rel_annotation(request):
    message = urllib.unquote(request.POST[u'message'])
    # print message
    RelAnnoLogParser.insertMessageToDB(message)
    return HttpResponse('OK')


