-*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import httplib2
import os
from datetime import datetime
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
        cls.all_vga_list = []
        
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


    def add_date(self,sheet_name):
        range_name = '%s!G1' %(sheet_name)
        value_input_option = 'RAW'
        
        date = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        values = [[date]]
        
        body = {
            'values': values        
        }
        
        result = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheetId, range=range_name, valueInputOption=value_input_option, body=body).execute()

        
    def remove_items(self,sheet_name):       
        while self.i != 0:
            range_name = '%s!A%d:D' %(sheet_name,self.i)
            body = {}
            result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=range_name).execute()
            values = result.get('values', [])
            if not values:
                range_name = '%s!A2:D%d' %(sheet_name,self.i)
                clear_values = self.service.spreadsheets().values().clear(spreadsheetId=self.spreadsheetId, range=range_name, body=body).execute()
                self.i = 0
            else:
                self.i += 1
        self.i = 2

            
    def add_items(self,sheet_name):
        range_name = '%s!A%d:D' %(sheet_name,self.i)
        value_input_option = 'RAW'
            
        values = self.all_vga_list
            
            
        body = {
            'values': values        
        }
            
        result = self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheetId, range=range_name, valueInputOption=value_input_option, body=body).execute()
        
        self.add_date(sheet_name)
        
        self.i += 1

    
    def open_spider(self, spider):
        if spider.name == "rx470":
            self.remove_items("RX 470")
        elif spider.name == "rx480":
            self.remove_items("RX 480")
        elif spider.name == "rx570":
            self.remove_items("RX 570")
        elif spider.name == "rx580":
            self.remove_items("RX 580")
 
       
    def close_spider(self, spider):
        if spider.name == "rx470":
            self.add_items("RX 470")
        elif spider.name == "rx480":
            self.add_items("RX 480")
        elif spider.name == "rx570":
            self.add_items("RX 570")
        elif spider.name == "rx580":
            self.add_items("RX 580")
        self.all_vga_list = []
        self.i = 2
 
    
    def process_item(self, item, spider):
        vga_list = list(item.values())
        self.all_vga_list.append(vga_list)
        
        return item
