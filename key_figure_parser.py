#!/usr/bin/env python
#encoding: utf8

import json
import csv
import sys
import os.path
import datetime


# def json2csv(infile, outfile):
#     with open(infile) as datafile:
#         data = json.load(datafile)
#         dates = data['timeline']['date']
#         dates.sort(key = lambda x: (x['asset']['caption']))
#
#     with open(outfile, 'w') as output:
#         output.write('caption\tstartdate\theadline\ttext\tmedia\tthumbnail\tcredit\n')
#         for row in dates:
#             output.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %(row['asset']['caption'].encode('utf-8'), row['startDate'].encode('utf-8'),
#             row['headline'].encode('utf-8'), row['text'].encode('utf-8'),row['asset']['media'].encode('utf-8'),
#             row['asset']['thumbnail'].encode('utf-8'), row['asset']['credit'].encode('utf-8')))


def csv2json(infile, outfile, xe=False):
    dates = []
    with open(infile) as datafile:
        for row in csv.DictReader(datafile, delimiter=','):
            if row['Show']=='Y':
                dates.append({
                    'headline':  '%s' %(row['Name']),
                    'text':      '<div><span class="label label-default">%s</span></div><br/>' \
                                 '<div class="table-responsive"><table class="table table-striped table-hover table"><thead><tr></tr></thead><tbody>' \
                                 '<tr><td>Height:</td><td align="right">%s cm</tr>' \
                                 '<tr><td>Weight:</td><td align="right">%s kg</tr>' \
                                 '<tr><td>Blood:</td><td align="right">%s</tr>' \
                                 '<tr><td>B/W/H:</td><td align="right">%s/%s/%s</tr>' \
                                 '<tr><td>Cup:</td><td align="right">%s</tr>' \
                                 '<tr><td>CV:</td><td align="right">%s</tr>' \
                                 '</tbody></table></div>' \
                                %(row['Game'], row['Height'], row['Weight'], row['Blood'], row['B'], row['W'], row['H'], row['Cup'], row['CV']),
                    'startDate': '2000,%s,%s,0,0,0' %(row['BirthMonth'], row['BirthDay']),
                    #'endDate':   '2000,%s,%s' %(row['BirthMonth'], str(int(row['BirthDay'])+1)),
                    #'type':      'default',
                    #'tag':       row['Tag'],
                    'asset':    {
                        #'caption':   row['Name'],
                        'credit':    'Copyright: Key / Visual Art\'s',
                        'thumbnail': 'img_thumb/%s' %row['THPic'],
                        'media':     'img/%s' %row['Pic'],
                    }
                })
                if not os.path.isfile('img/'+row['Pic']):
                    dates[len(dates)-1]['asset']['media']='img/key_logo.png'
                if not os.path.isfile('img_thumb/'+row['THPic']):
                    dates[len(dates)-1]['asset']['thumbnail']='img_thumb/key_logo.png'
                if row['BirthMonth']== '不明' or row['BirthMonth']=='' or row['BirthMonth']=='0':
                    dates[len(dates)-1]['startDate']='2001,1,1,0,0,1'
                if row['Height']=='不明' or row['Weight']=='不明' or row['Height']=='' or row['Weight']=='':
                        dates[len(dates)-1]['text'] = dates[len(dates)-1]['text'].replace('不明 cm','不明').replace('不明 kg','不明')
                
                ##~~~~~~
                if xe:
                    row['Cup']= row['Cup'].replace('目測','')
                    if row['Cup']=='G' or row['Cup']=='F' or row['Cup']=='E':
                        dates[len(dates)-1]['tag']='>D杯'
                    elif row['Cup']=='A' or row['Cup']=='AA':
                        dates[len(dates)-1]['tag']='A/AA杯'
                    elif row['Cup']=='不明' or row['Cup']=='':
                        dates[len(dates)-1]['tag']='?杯'
                    else:
                        dates[len(dates)-1]['tag']=row['Cup']+'杯'
    #sort by date, for show today's nearest birthday character
    dates.sort(key= lambda x: datetime.datetime.strptime(x['startDate'], '%Y,%m,%d,%H,%M,%S'))
    
    data = {}
    if xe:
        data['headline'] = 'Key Character Birthday Timeline XE'
    else:
        data['headline'] = 'Key Character Birthday Timeline'
    data['text'] = \
        'Last update: 2015/03<br/>webpage made by <a href=\"https://twitter.com/lovegoodbest\">goodbest</a>@<a href=\"http://keyfc.net\">KeyFC</a><br/><br/>' \
        '<p>Special Thanks to:<br/>slk000, 幾星霜の観測者, <a href=\"http://www.weibo.com/1415459877\">JimRaynor_2001></a></p>'
    data['type'] = 'default'
    data['asset'] = {}
    data['asset']['media'] = 'img/key_logo.png'
    data['date'] = dates
    
    with open (outfile, 'w') as output:
        json.dump({'timeline': data}, output)


#json2csv('ksl.json', 'ksl.csv')
csv2json('key_figure.csv', 'key_figure.json')
csv2json('key_figure.csv', 'key_figure_xe.json', xe=True)







