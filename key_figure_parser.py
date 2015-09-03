#!/usr/bin/env python
#encoding: utf8

import json
import csv
import sys
import os.path
import datetime


def addDate(m, d, add=1):
    day_cons=[31,28,31,30,31,30,31,31,30,31,30,31]
    if((d + add) > day_cons[m-1]):
        d = d + add - day_cons[m-1]
        m += 1
    else:
        d += add
    return (m,d)
    
def csv2json(infile, outfile, xe=False):
    dates = []
    with open(infile) as datafile:
        #unkown birthday character fake birth var
        no_birth_m = 1
        no_birth_d = 20
        
        for row in csv.DictReader(datafile, delimiter=','):
            if row['Show']=='Y':
                dates.append({
                    #'headline':  '<abbr title="%s">%s</abbr>' %(row['NameR'], row['Name']),
                    'headline':  '%s' %(row['Name']),
                    'text':      '<span>%s</span><br/><br/>' \
                                 '<div><span class="label label-default">%s</span></div><br/>' \
                                 '<div class="table-responsive"><table class="table table-striped table-hover table"><thead><tr></tr></thead><tbody>' \
                                 '<tr><td>Height:</td><td align="right">%s cm</tr>' \
                                 '<tr><td>Weight:</td><td align="right">%s kg</tr>' \
                                 '<tr><td>Blood:</td><td align="right">%s</tr>' \
                                 '<tr><td>B/W/H:</td><td align="right">%s/%s/%s</tr>' \
                                 '<tr><td>Cup:</td><td align="right">%s</tr>' \
                                 '<tr><td>CV:</td><td align="right">%s</tr>' \
                                 '</tbody></table></div>' \
                            %(row['NameR'], '</span></div><br/><div><span class=\"label label-default\">'.join(row['Game'].split('/')), row['Height'], 
                              row['Weight'], row['Blood'], row['B'], row['W'], row['H'], row['Cup'], row['CV']),
                    'startDate': '2000,%s,%s,0,0,0' %(row['BirthMonth'], row['BirthDay']),
                    #'type':      'default',
                    #'tag':       row['Tag'],
                    'asset':    {
                        #'caption':   row['NameR'],
                        'credit':    '<a href=\"http://key.visualarts.gr.jp\">© Visual Art\'s / Key</a>',
                        'thumbnail': 'img_thumb/%s' %row['ThumbPic'],
                        'media':     'img/%s' %row['Pic'],
                    }
                })
                if not os.path.isfile('img/'+row['Pic']):
                    dates[len(dates)-1]['asset']['media']='img/key_logo.png'
                if not os.path.isfile('img_thumb/'+row['ThumbPic']):
                    dates[len(dates)-1]['asset']['thumbnail']='img_thumb/key_logo.png'
                
                #for unknown birthday character, we fake their birthday to be year 2001, month and day increases per character
                if row['BirthMonth']== '不明' or row['BirthMonth']=='' or row['BirthMonth']=='0':
                    dates[len(dates)-1]['startDate']='2001,%s,%s,0,0,1' %(no_birth_m, no_birth_d)
                    (no_birth_m, no_birth_d) = addDate(no_birth_m, no_birth_d, add=4)
                    
                if row['Height']=='不明' or row['Weight']=='不明' or row['Height']=='' or row['Weight']=='':
                        dates[len(dates)-1]['text'] = dates[len(dates)-1]['text'].replace('不明 cm','不明').replace('不明 kg','不明')
                
                ##~~x~~e~~
                if xe:
                    row['Cup']= row['Cup'].replace('Est. ','')
                    if row['Cup']=='G' or row['Cup']=='F' or row['Cup']=='E':
                        dates[len(dates)-1]['tag']='>D cup'
                    elif row['Cup']=='A' or row['Cup']=='AA':
                        dates[len(dates)-1]['tag']='A/AA cup'
                    elif row['Cup']=='不明' or row['Cup']=='':
                        dates[len(dates)-1]['tag']='? cup'
                    else:
                        dates[len(dates)-1]['tag']=row['Cup']+' cup'
                        
    info_page={}
    info_page['headline']='Attention'
    info_page['text']='注意'
    info_page['asset']={}
    info_page['asset']['media']='<blockquote>There are no official birthday info for characters in the following slides, so timeline at bottom is virtual.<br/><br/>' \
            '之后页面里的人物没有来自官方的生日资料，因此页面底部的时间轴是虚拟的。</blockquote>'
    info_page['startDate']='2001,1,10,0,0,1'
    dates.append(info_page)
    
    #sort by date, for show today's nearest birthday character
    dates.sort(key= lambda x: datetime.datetime.strptime(x['startDate'], '%Y,%m,%d,%H,%M,%S'))
    
    title_page = {}
    if xe:
        title_page['headline'] = 'Key Character Birthday Timeline XE'
    else:
        title_page['headline'] = 'Key Character Birthday Timeline'
    title_page['text'] = \
        'Last update: 2015/08<br/>webpage made by <a href=\"https://twitter.com/lovegoodbest\">goodbest</a>@<a href=\"http://keyfc.net\">KeyFC</a><br/><br/>' \
        '<p>Special thanks to:<br/>slk000, 幾星霜の観測者, <a href=\"http://www.weibo.com/1415459877\">JimRaynor_2001</a></p>'
    title_page['type'] = 'default'
    title_page['asset'] = {}
    title_page['asset']['media'] = 'img/key_logo.png'
    title_page['date'] = dates
    
    with open (outfile, 'w') as output:
        json.dump({'timeline': title_page}, output)


#json2csv('ksl.json', 'ksl.csv')
csv2json('key_figure.csv', 'key_figure.json')
csv2json('key_figure.csv', 'key_figure_xe.json', xe=True)







