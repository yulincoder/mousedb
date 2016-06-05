# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 00:07:32 2016

@author: tete
"""

import os
import json

def load(location,option = True):
    return mousedb(location,option)

class mousedb:
    
    def __init__(self,location,option = True):
        ''' Creates a database object with the location.If the file dose not exist
        it will be created on the frist update.If the option is True then the file 
        will be stored disk ,else it is still stay in memory.
        --------------------------------------------------------------------------
        根据输入的路径实例化一个数据库对象，如果路径不存在则在第一次实例化时新建文件
        否则只是打开文件。option参数如果是True则数据存储与磁盘，False则存储于内存。        
        '''
        self.loco = location
        self.fsave = option
        self.abs_location = os.path.abspath(location)
        
        if os.path.exists(self.abs_location):
            #pass            
            self._loaddb()
        else:   
            self.db = {}
            self._dumpdb()
        print 'log:load successful.'
        
    
    def cre_table(self,items):
        ''' Create a table in database object,and a object will support only one table.
            The 0 of index in items is the key value.
        -------------------------------------------------------------------------------
            在一个数据库对象中建立一张表，并且一个对象管理只能是一张表。其中items第一个
            元素为主键。
        '''
        self.items = items
        self.KEY_VALUE = 0
        self.db[items[self.KEY_VALUE]] = {}
        
        
    def insert_row(self,data):
        ''' Insetr a row data into table.
        ---------------------------------
            向表中插入一行数据。
        '''
        fromat = {data[0]:{}} 
        self.db[self.items[self.KEY_VALUE]] = fromat
        
        print '---',self.db
        row = dict(zip(self.items[1:],data[1:]))
        #self.db[self.items[self.KEY_VALUE]][data[self.KEY_VALUE]] = row
        self._dumpdb()
        
    def input_table(self):
        if self.fsave:
            with open(self.abs_location,'r') as f:
                data = json.loads(f.read().decode('utf-8'))
                print data
        
        
        
    def _loaddb(self):
        ''' Load or reload the json info from the file. 
        ----------------------------------------------
            从文件中以加载数据到内存中，并将json格式数据
            进行解析。
        '''
        print '_loaddb'
        with open(self.abs_location,'r') as f:    
            self.db = json.loads(f.read())

    
    def _dumpdb(self):
        ''' Write/save reload the json dump into the file.
        --------------------------------------------------
            将数据库数据生成json格式并存入磁盘文件。
        '''
        print '_dumpdb'
        if self.fsave:
            with open(self.abs_location,'w') as f:
                f.write(json.dumps(self.db).encode('utf-8'))