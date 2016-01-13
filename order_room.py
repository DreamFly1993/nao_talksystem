# coding: utf-8

import random
import time
import jieba.posseg as pseg
import nao_api

class RoomParameters(object):
    def __init__(self):
        print 'Initial function. You see this means you have new a OrderRoom class'
        """
        slot  value : known | unknown
                    * used for create_sen
        state number: 3 > unknown | know_nconf | known
                    * slot state used for answer
        act   number: 5 > ask | confirm | trans | confirm_trans | ask_trans
                    * slot act used for choose current action
        state trans : self_trans, other_trans
        other actions: change(ones received this ,need to do some change while create sentences)
                    * user's action
                       angry(while doing so many changes need to do something that let uses know you are angry)
                       happy(while angry action is not actived)
                       neutral(most times)
                    * nao action
        """
        self.__unit_time = time.time()
        self.__unit_state = 'START'
        self.__action_cur_state = 'UNKNOWN'
        self.__action_pre_state = ''
        self.__change_times = 0
        self.__slot_value = ''
        self.state_num = 3
        self.act_num = 5
#        self.matrix_q = [[0 for _ in range(self.act_num)] for _ in range(self.state_num)]
        self.matrix_r = [[100, 1, 50, 1, 75],
                         [10, 100, 50, 75, 1],
                         [1, 10, 100, 10, 1]]
        self.__state_trans = [['UNCONFIRMED', 'UNKNOWN', 'UNKNOWN', 'UNKNOWN'],
                              ['UNCONFIRMED', 'KNOWN', 'UNKNOWN', 'UNKNOWN'],
                              ['UNCONFIRMED', 'KNOWN', 'UNKNOWN', 'UNKNOWN']]
        self.matrix_q = self.matrix_r
        self.__enum_state = {'START': -1, 'STOP': -2, 'FORCE_QUIT': -3,
                             'UNKNOWN': 0, 'UNCONFIRMED': 1, 'KNOWN': 2}
        self.__enum_action = {'ASK': 0, 'CONFIRM': 1, 'TRANS': 2, 'CONFIRM_TRANS': 3, 'ASK_TRANS': 4}
        self.__enum_user_action = {'TELL': 0, 'CONFIRM': 1, 'REJECT': 2, 'CHANGE': 3}
        self.q_lambda = 0.8
        self.__waiting_time = -1


    def q_learning_teach(self, if_cancel=False):
        """
        The Q-Learning algorithm goes as follows:
        1. Set the gamma parameter, and environment rewards in matrix R.
        2. Initialize matrix Q to zero.
        3. For each episode:
            Select a random initial state.
            Do While the goal state hasn't been reached.
            1). Select one among all possible actions for the current state.
            2). Using this possible action, consider going to the next state.
            3). Get maximum Q value for this next state based on all possible actions.
            4). Compute: Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]
            5). Set the next state as the current state.
            End Do
        End For
        :param if_cancel:whether stop while not done
        :return:
        """
        print 'q_learning for training'
        print '__begin__'
        while not if_cancel:
            cur_state = input('please input current state: ')
#            cur_state = random.randrange(0, 6)
            print 'cur_state: ' + str(cur_state)
            while cur_state != 5:
                act = random.randrange(0, 6)
                while self.matrix_r[cur_state][act] == -1:
                    act = random.randrange(0, 6)
                next_state = act
                max_value = -1
                for j in range(6):
                    value_q = self.matrix_q[next_state][j]
                    if max_value < value_q:
                        max_value = value_q
                reward = self.matrix_r[cur_state][act]
                self.matrix_q[cur_state][act] = reward + self.q_lambda * max_value
                cur_state = next_state
            print self.matrix_q
        print '__end__'

    def quit_unit(self):
        self.state_num = 'STOP'

    def get_best_action(self):
        act_list = self.matrix_q[self.__enum_state[self.__action_cur_state]][:]
        sum_value = sum(act_list)
        print sum_value
        act = random.randrange(0, sum_value, 1)
        for i in range(self.act_num):
            if act <= act_list[i]:
                return i
            act -= act_list[i]
        self.__action_pre_state = self.__action_cur_state

    def update_state(self, cur_act):
        """
        :param cur_act:'CONFIRM', 'REJECT', 'CHANGE', 'TELL'
        :return: null
        """
        print 'update state'
        self.__action_pre_state = self.__action_cur_state
        print self.__action_cur_state
        int_cur_state = self.__enum_state[self.__action_cur_state]
        int_cur_action = self.__enum_user_action[cur_act]
        self.__action_cur_state = self.__state_trans[int_cur_state][int_cur_action]

    @property
    def change_times(self):
        return self.__change_times

    @change_times.setter
    def change_times(self, value):
        self.__change_times = value

    @property
    def unit_time(self):
        return self.__unit_time

    @unit_time.setter
    def unit_time(self, value):
        self.__unit_time = value

    @property
    def waiting_time(self):
        if self.__waiting_time != -1:
            self.__waiting_time -= self.__waiting_time
        return self.__waiting_time

    @waiting_time.setter
    def waiting_time(self, value):
        self.__waiting_time = value

    @property
    def unit_state(self):
        return self.__unit_state

    @unit_state.setter
    def unit_state(self, value):
        self.__unit_state = value

    @property
    def action_cur_state(self):
        return self.__action_cur_state

    @action_cur_state.setter
    def action_cur_state(self, value):
        self.__action_cur_state = value

    @property
    def slot_value(self):
        return self.__slot_value

    @slot_value.setter
    def slot_value(self, value):
        self.__slot_value = value


class OrderRoom(object):
    def __init__(self):
        # create four parameters of rooms
        self.room_time = RoomParameters()
        self.room_time.unit_state = 'START'
        self.room_place = RoomParameters()
        self.room_place.unit_state = 'START'
        self.room_costs = RoomParameters()
        self.room_costs.unit_state = 'START'
        self.room_attend = RoomParameters()
        self.room_attend.unit_state = 'START'

        self.__if_begin = True
        self.__pre_action = [-1, -1, -1, -1]
        self.__cur_action = [-1, -1, -1, -1]
        self.__user_action = ['', '', '', '']
        self.__user_pre_action = self.__user_action[:]
        self.__slot2func = {u'时间': self.room_time, u'地点': self.room_place,
                            u'人数': self.room_attend, u'预算': self.room_costs}
        self.__name2num = {u'时间': 3, u'地点': 0, u'人数': 2, u'预算': 1}

    def do_work(self, input_pair):
        print 'do work'
        parse_ans = self.parsing_sen(input_pair)

        return True

    def parsing_sen(self, input_pair):
        """
        :param input_pair: word pos pair after jieba.posing
        :return: true or false
            True: this sentence is talking about room-oder or room-order is already finished.
            False: others
        """
        # get words and word flags
        word_list = []
        flag_list = []
        for cur_pair in input_pair:
            word_list.append(cur_pair.word)
            flag_list.append(cur_pair.flag)

        print word_list
        print flag_list
        # 地点 预算 人数 时间
        tmp_list = [0, 0, 0, 0]
        if_confirm = False
        self.__user_pre_action = self.__user_action[:]
        self.__user_action = [-1, -1, -1, -1]
        i = 0
        while i < len(word_list):
            print word_list[i]
            if word_list[i] in [u'地点', u'预算', u'人数', u'时间']:
                if u'对' in word_list[i:]:
                    self.__slot2func[word_list[i]].update_state('CONFIRM')
                    self.__user_action[self.__name2num[word_list[i]]] = 'CONFIRM'
                elif u'不对' in word_list[i:]:
                    self.__slot2func[word_list[i]].update_state('REJECT')
                    self.__user_action[self.__name2num[word_list[i]]] = 'REJECT'
                elif if_confirm:
                    self.__slot2func[word_list[i]].update_state('CONFIRM')
                    self.__user_action[self.__name2num[word_list[i]]] = 'CONFIRM'
            if word_list[i] in [u'恩', u'嗯', u'对的', u'ok', u'好的']:
                if_confirm = True
                i += 1
                continue

            if 'ns' == flag_list[i]:
                print 'place'
#                action = self.room_place.get_best_action()
#                print 'action: ' + str(action)
                tmp_list[0] = 1
#                nao_api.naoqi_api().say_something("你好")
#                nao_api.naoqi_api().head_scratch([0, 0])
                value = word_list[i]
                i += 1
                while i < len(flag_list) and 'm' == flag_list[i]:
                    value += word_list[i]
                    i += 1
                if self.room_place.slot_value != '':
                    self.room_place.change_times = random.randrange(4)
                    self.room_place.update_state('CHANGE')
                    self.__user_action[0] = 'CHANGE'
                else:
                    self.room_place.slot_value = value
                    self.room_place.update_state('TELL')
                    self.__user_action[0] = 'TELL'
                continue
            if 't' == flag_list[i]:
                print 'time'
#                action = self.room_time.get_best_action()
#                print action
                tmp_list[3] = 1
                value = word_list[i]
                i += 1
                print flag_list
                while i < len(flag_list) and 'm' == flag_list[i]:
                    value += word_list[i]
                    i += 1
                print 'value: ' + self.room_time.slot_value
                if self.room_time.slot_value != '':
                    self.room_time.change_times = random.randrange(4)
                    self.room_time.update_state('CHANGE')
                    self.__user_action[3] = 'CHANGE'
                    print 'sfkskfaskfhkfjksdf'
                else:
                    self.room_time.slot_value = value
                    self.room_time.update_state('TELL')
                    self.__user_action[3] = 'TELL'
                print 'i: ' + str(i)
                continue

            if 'm' == flag_list[i]:
                print type(word_list[i])
                if u'点' in word_list[i] and tmp_list[3] != 1:
                    print 'time'
#                    action = self.room_time.get_best_action()
#                    print action
                    tmp_list[3] = 1
                    value = word_list[i]
                    i += 1
                    while i < len(flag_list) and 'm' == flag_list[i]:
                        value += word_list[i]
                    if self.room_time.slot_value != '':
                        self.room_time.change_times = random.randrange(4)
                        self.room_time.update_state('CHANGE')
                        self.__user_action[3] = 'CHANGE'
                    else:
                        self.room_time.slot_value = value
                        self.room_time.update_state('TELL')
                        self.__user_action[3] = 'TELL'
                    continue
                elif u'人' in word_list[i] or (i + 1 < len(word_list) and u'人' in word_list[i + 1]):
                    print 'attendance number'
#                    action = self.room_attend.get_best_action()
#                    print action
                    tmp_list[2] = 1
                    value = word_list[i]
                    i += 1
                    while i < len(flag_list) and 'm' == flag_list[i]:
                        value += word_list[i]
                        i += 1
                    if self.room_attend.slot_value != '':
                        self.room_attend.change_times = random.randrange(4)
                        self.room_attend.update_state('CHANGE')
                        self.__user_action[2] = 'CHANGE'
                    else:
                        self.room_attend.slot_value = value
                        self.room_attend.update_state('TELL')
                        self.__user_action[2] = 'TELL'
                    continue
                elif u'元' in word_list[i] or (i + 1 < len(word_list) and u'元' in word_list[i + 1]):
                    print 'costs'
#                    action = self.room_costs.get_best_action()
#                    print action
                    tmp_list[1] = 1
                    value = word_list[i]
                    i += 1
                    while i < len(flag_list) and 'm' == flag_list[i]:
                        value += word_list[i]
                        i += 1
                    if self.room_costs.slot_value != '':
                        self.room_costs.change_times = random.randrange(4)
                        self.room_costs.update_state('CHANGE')
                        self.__user_action[1] = 'CHANGE'
                    else:
                        self.room_costs.slot_value = value
                        self.room_costs.update_state('TELL')
                        self.__user_action[1] = 'TELL'
                    continue
            i += 1
        if sum(tmp_list) == 0 and not self.__if_begin:
            print 'did not found message about room order!'
            return False

        print 'time: ' + self.room_time.slot_value + \
              '\tplace: ' + self.room_place.slot_value + \
              '\tattend: ' + self.room_attend.slot_value + \
              '\tcosts: ' + self.room_costs.slot_value
        print 'user_action: ' + str(self.__user_action)
        print 'user_pre_act: ' + str(self.__user_pre_action)
        return True

if __name__ == '__main__':
    a = OrderRoom()
    b = raw_input('\t: ')
    while b != 'exit':
        a.parsing_sen(pseg.cut(b))
#        c = pseg.cut(b)
#        for i in c:
#            print i.word + ' ' + i.flag
        b = raw_input('\t: ')

