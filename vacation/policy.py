# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
from rasa_dm.actions.action import ACTION_LISTEN_NAME
from rasa_dm.agent import Agent
from rasa_dm.domain import TemplateDomain
from rasa_dm.policies import Policy
import numpy as np
from rasa_dm.util import one_hot

logger = logging.getLogger(__name__)


class SimplePolicy(Policy):
    def predict_action_probabilities(self, tracker, domain):
        # type: (DialogueStateTracker, Domain) -> List[float]

        if tracker.latest_action_id_str == ACTION_LISTEN_NAME:
            key = tracker.latest_message.intent["name"]
            print(tracker.slots)
            if key in ["inform", "travel"]:
                if tracker.get_slot("startDate") is None:
                    action = domain.index_for_action("action_ask_start_date")
                elif tracker.get_slot("destCity") is None:
                    if tracker.get_slot("topicLabel") is None:
                        action = domain.index_for_action("action_ask_dest_place")
                    else:
                        action = domain.index_for_action("action_on_it")
                        print(domain.index_for_action("action_search_vacations"))
                        tracker.trigger_follow_up_action(domain.action_for_name("action_search_vacations"))
                # elif tracker.get_slot("topicLabel") is None:
                #    action = responses["ask_topic_label"]
                # elif tracker.get_slot("startCity") is None:
                #    action = responses["ask_start_city"]
                # elif tracker.get_slot("endDate") is None:
                #    action = responses["ask_duration"]
                else:
                    action = domain.index_for_action("action_on_it")
                    tracker.trigger_follow_up_action(domain.action_for_name("action_search_vacations"))
            elif key == "deny":
                action = domain.index_for_action("action_ask_moreupdates")
            elif key == "greet":
                action = domain.index_for_action("action_greet")
            elif key in ["goodbye", "thankyou"]:
                action = domain.index_for_action("action_goodbye")
                tracker.reset()
            else:
                action = domain.index_for_action("action_default")
            return one_hot(action, domain.num_actions)
        else:
            return np.zeros(domain.num_actions)

