# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import random
import re
from rasa_dm.actions.action import ACTION_LISTEN_NAME
from rasa_dm.interpreter import NaturalLanguageInterpreter
from SlotRecog.Business.Travel.all_fields import All_Fields

logger = logging.getLogger(__name__)


class NERInterpreter(NaturalLanguageInterpreter):

    def __init__(self):
        self.all_fields = All_Fields()
        self.step = "Travel_OpenQuestion"
        self.greet_pattern = re.compile("你好|您好|hello|hi|嗨|在吗|哈喽")
        self.deny_pattern = re.compile("不|没")
        self.affirm_pattern = re.compile("好的|行啊|是的|对的|ok|好滴|好啊")
        self.thank_pattern = re.compile("谢谢|感谢|多谢")
        self.bye_pattern = re.compile("88|再见|拜拜")
        self.travel_pattern = re.compile("旅游|出去玩")

    def extract_intent_and_entities(self, user_input):
        """
        Item	id	int	对应的id
            name	string	对应的中文名
        SlotPair	SightPoi	list<Item>	用户希望经过的景点
            TopicLabel	list<Item>	主题标签
            destCity	List<Item>	目的地城市
            destProvince	List<Item>	目的地省份
            destCountry	List<Item>	目的地国家
            City	List<Item>	城市
            TripType	string	出行方式：DIY/PKG
            startCity	Item	出发城市
            Duration	int	出行天数
            StartDate	string	yyyy-MM-dd
            EndDate	string	yyyy-MM-dd
            Date	string	yyyy-MM-dd
            StarLevel	int	钻级   默认情况下为-1
            IsOverseas	int	1为海外  0非海外 默认情况下为-1
            备注：
            1、检索必备条件是
              1）topic/destCity/destProvince/destCountry
              2）startDate/endDate
              3）startCity
        """
        entities = []
        try:
            intent = "inform"

            # why this param is always required?
            pre_hotel_info = {'Poi': {}, 'TopicLabel': {}, 'TripType': '','City': {'destCity':{},   'destProvince':{},'destCountry':{},'UnknowCity':{},'startCity': {}}, 'Date':{'Days':'','StartDate':'',       'EndDate':'', 'UnknowDate':'' },'DepartDate':'','Level': -1, 'IsOverseas':-1,'error':''}
            # parse entity
            result = self.all_fields.parse_all_fields(user_input, self.step, pre_hotel_info)

            print (repr(result).decode('unicode-escape'))
            start_city = result.get("City").get("startCity")
            dest_city = result.get("City").get("destCity")
            dest_province = result.get("City").get("destProvince")
            dest_country = result.get("City").get("destCountry")
            city = result.get("City").get("UnknownCity")

            start_date = result.get("Date").get("StartDate")
            end_date = result.get("Date").get("EndDate")
            topic_label = result.get("TopicLabel").get("TopicLabel")
            if start_city:
                entity = {"entity": "startCity", "value": start_city.values()[0]}
                entities.append(entity)
            if dest_city:
                entity = {"entity": "destCity", "value": dest_city.values()[0]}
                entities.append(entity)
            if start_date:
                entity = {"entity": "startDate", "value": start_date}
                entities.append(entity)
            if end_date:
                entity = {"entity": "startDate", "value": end_date}
                entities.append(entity)
            if topic_label:
                entity = {"entity": "topicLabel", "value": topic_label.values()}
                entities.append(entity)
            if len(entities) == 0:
                if self.greet_pattern.search(user_input):
                    intent = "greet"
                elif self.deny_pattern.search(user_input):
                    intent = "deny"
                elif self.thank_pattern.search(user_input):
                    intent = "thankyou"
                elif self.bye_pattern.search(user_input):
                    intent = "goodbye"
                elif self.affirm_pattern.search(user_input):
                    intent = "affirm"
                elif self.travel_pattern.search(user_input):
                    intent = "travel"
                else:
                    intent = "default"
            print(intent, entities)
            return intent, entities
        except Exception as e:
            return None, []

    def parse(self, text):
        intent, entities = self.extract_intent_and_entities(text)
        return {
            'text': text,
            'intent': {
                'name': intent,
                'confidence': 1.0,
            },
            'intent_ranking': [{
                'name': intent,
                'confidence': 1.0,
            }],
            'entities': entities,
        }

