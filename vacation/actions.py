# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_dm.actions.action import Action
from rasa_dm.events import SetSlot


class ActionSearchVacations(Action):
    def name(self):
        return 'search_vacations'

    @staticmethod
    def extract_slots(tracker):
        filters = dict()
        for name, slot in tracker.slots.items():
            if slot.value:
                filters[name] = slot.value
        return filters

    def run(self, dispatcher, tracker, domain):
        vacations = [
            {"name": "1.东京一周游", "reviews": 4.5},
            {"name": "2.冲绳岛海滩五日游，大折扣", "reviews": 5.}
        ]
        filters = self.extract_slots(tracker)
        description = "; ".join([c["name"] for c in vacations])
        dispatcher.utter_message("{}".format(description))
        return [SetSlot("vacations", vacations)]


class ActionShowRecommendReason(Action):
    def name(self):
        return 'show_venue_reviews'

    def run(self, dispatcher, tracker, domain):
        venues = tracker.get_slot("venues")
        dispatcher.utter_message("venues from slots: {}".format(venues))
        return []

