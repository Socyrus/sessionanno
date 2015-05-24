#!/usr/bin/env python
# encoding: utf-8

import urllib2
import re

response = urllib2.urlopen('http://127.0.0.1:8000/admin/allQueries/')
html = response.read()

p = re.compile(r'/SERP/(\d{1,2})/(.*?)/(\d{1,2})/')
searchRes = p.findall(html)


outputFile = open('result.txt', 'w')
count = 0
maxCount = 2  #how many htmls will you create?
htmls = []
for a in searchRes:
    count = count + 1
    url = 'http://127.0.0.1:8000/SERP'
    for temp in a:
        url = url + '/' + temp
    print url

    response = urllib2.urlopen(url)
    html = response.read()
    htmls.append(html.replace('\n','')+'\n')

    if count == maxCount:
        break

outputFile.writelines(htmls)
outputFile.close()

inputFiles = open('result.txt','r')  # check result
count = 0
for line in inputFiles.readlines():
    count = count + 1
print count
inputFiles.close()

