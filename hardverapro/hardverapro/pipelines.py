# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

class GoogleAPIPipeline(object):
    @classmethod
    def __init__(cls):
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'Google Sheets API for Scrapy'
        
        cls.i = 2
        
        working_dir = os.getcwd()
        credential_dir = os.path.join(working_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-scrapy.json')
        store = Storage(credential_path)
        cls.credentials = store.get()
        if not cls.credentials or cls.credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            cls.credentials = tools.run_flow(flow, store)
        http = cls.credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?''version=v4')
        cls.service = discovery.build('sheets', 'v4', http=http,discoveryServiceUrl=discoveryUrl)
        cls.spreadsheetId = '1SOial1KEWrdAcF8qzUHbuIQ5cp5cK4JMiDq2jqkmE1o'

        
    def remove_items(self,spider,spider_name,sheet_name):       
        if spider.name == spider_name:
            while self.i != 0:
                range_name = '%s!A%d:D' %(sheet_name,self.i)
                body = {}
                result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=range_name).execute()
                values = result.get('values', [])
                if not values:
                    self.i = 0
                else:
                    clear_values = self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheetId, range=range_name, body=body).execute()
                    self.i += 1
            self.i = 2

            
    def add_items(self,spider,spider_name,sheet_name,item):
        if spider.name == spider_name:
            range_name = '%s!A%d:D' %(sheet_name,self.i)
            value_input_option = 'RAW'
            
            vga_list = list(item.values())
            vga_szoveg = str(vga_list[0])
            vga_ar = str(vga_list[1])
            vga_varos = str(vga_list[2])
            vga_link = str(vga_list[3])
            
            values = [[vga_szoveg,vga_ar,vga_varos,vga_link]]
            
            
            body = {
                'values': values        
            }
            
            result = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheetId, range=range_name, valueInputOption=value_input_option, body=body).execute()
            
            self.i += 1

    
    def open_spider(self, spider):
        self.remove_items(spider,"rx470","RX 470")
        self.remove_items(spider,"rx480","RX 480")
        self.remove_items(spider,"rx570","RX 570")
        self.remove_items(spider,"rx580","RX 580")
 
       
    def close_spider(self, spider):
        self.i = 2
 
    
    def process_item(self, item, spider):
        self.add_items(spider,"rx470","RX 470",item)
        self.add_items(spider,"rx480","RX 480",item)
        self.add_items(spider,"rx570","RX 570",item)
        self.add_items(spider,"rx580","RX 580",item)
        
        return item
