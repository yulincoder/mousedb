# -*- coding: utf-8 -*-

# Copyright (c) 2016, Zhang Te
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# Neither the name of the Harrison Erd nor the names of its contributors
# may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "
# AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

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
        self.KEY_VALUE = 0
        
        if os.path.exists(self.abs_location):
            self._loaddb()
        else:   
            self.db = {}
            self._dumpdb()
        
    
    
    def createtable(self,items):
        ''' Create a table in database object,and a object will support only one table.
            The 0 of index in items is the key value.
        -------------------------------------------------------------------------------
            在一个数据库对象中建立一张表，并且一个对象管理只能是一张表。其中items第一个
            元素为主键。
        '''
        self.items = items
        self.db[u'items'] = items
        self.db[items[self.KEY_VALUE]] = {}
        self._dumpdb()
        
        
        
    def insertrow(self,data):
        ''' Insetr a row data into table.
        ---------------------------------
            向表中插入一行数据。
        '''
        row = dict(zip(self.items[1:],data[1:]))
        self.db[self.items[self.KEY_VALUE]][data[0]] = row
        self._dumpdb()
        
        
        
    def update(self,key,item,value):
        ''' Update a value of the special key and item.
        ------------------------------------------------
            根据主键和索引更新数据。
        '''
        if self.db[self.items[self.KEY_VALUE]].has_key(key):
            curr = self.db[self.items[self.KEY_VALUE]][key]
            if curr.has_key(item):
                curr[item] = value
                self._dumpdb()
                return True
        return False
        
        
        
    def delrow(self,key):
        ''' Delete a row.
        -----------------
            删除一行。
        '''
        if self.db[self.items[self.KEY_VALUE]].has_key(key): 
            self.db[self.items[self.KEY_VALUE]].pop(key)
            self._dumpdb()
            

    
    def findrow(self,key):
        ''' Find the special row.
        -------------------------
            查找指定行。
        '''
        if self.db[self.items[self.KEY_VALUE]].has_key(key):
            return {key:self.db[self.items[self.KEY_VALUE]][key]}
            
            
            
    def findvalue(self,key,item):
        ''' Find a value reply on key and item.
        ---------------------------------------
            根据主键值和表项查找值
        '''
        if self.db[self.items[self.KEY_VALUE]].has_key(key) and item in self.db[self.items[self.KEY_VALUE]][key]:
            return self.db[self.items[self.KEY_VALUE]][key][item]
            
            
        
    def print_table(self):
        ''' Print database with json fromat.
        ------------------------------------
            打印表。
        '''
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
        with open(self.abs_location,'r') as f:    
            self.db = json.loads(f.read().encode('utf-8'))
            self.items = self.db['items']

    
    
    def _dumpdb(self):
        ''' Write/save reload the json dump into the file.
        --------------------------------------------------
            将数据库数据生成json格式并存入磁盘文件。
        '''
        if self.fsave:
            with open(self.abs_location,'w') as f:
                f.write(json.dumps(self.db).encode('utf-8'))