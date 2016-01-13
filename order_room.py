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
        self.state_num = 3
        self.act_num = 5
#        self.matrix_q = [[0 for _ in range(self.act_num)] for _ in range(self.state_num)]
        self.matrix_r = [[100, 1, 50, 1, 75],
                         [10, 100, 50, 75, 1],
                         [1, 10, 100, 10, 1]]
        self.matrix_q = self.matrix_r
        self.__enum_state = {'START': -1, 'STOP': -2, 'FORCE_QUIT': -3,
                             'UNKNOWN': 0, 'UNCONFIRMED': 1, 'KNOWN': 2}
        self.__enum_action = {'ASK': 0, 'CONFIRM': 1, 'TRANS': 2, 'CONFIRM_TRANS': 3, 'ASK_TRANS': 4}
        self.q_lambda = 0.8
        self.__waiting_time = 0

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

    @property
    def change_times(self):
        return self.__change_times

    @property
    def unit_time(self):
        return self.__unit_time

    @unit_time.setter
    def unit_time(self, value):
        self.__unit_time = value

    @property
    def waiting_time(self):
        if self.__waiting_time:
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

class OrderRoom(object):
    def __init__(self):
        self.room_time = RoomParameters()
        self.room_time.unit_state = 'START'
        self.room_place = RoomParameters()
        self.room_place.unit_state = 'START'
        self.room_costs = RoomParameters()
        self.room_costs.unit_state = 'START'
        self.room_attend = RoomParameters()
        self.room_attend.unit_state = 'START'

    def do_work(self, input_pair):
        print 'do work'
        return self.parsing_sen(input_pair)

    def parsing_sen(self, input_pair):
        """
        :param input_pair: word pos pair after jieba.posing
        :return: true or false
            True: this sentence is talking about room-oder or room-order is already finished.
            False: others
        """
#        if self.__unit_state == 'START':
#            self.__action_cur_state = 'UNKNOWN'
#            self.__change_times = 0

        # get words and word flags
        word_list = []
        flag_list = []
        for cur_pair in input_pair:
            word_list.append(cur_pair.word)
            flag_list.append(cur_pair.flag)

        print flag_list
        print word_list
        tmp_list = [0, 0, 0, 0]
        if 'ns' in flag_list:
            print 'place'
            action = self.room_place.get_best_action()
            print action
            tmp_list[0] = 1
            nao_api.naoqi_api().say_something("你好")
            nao_api.naoqi_api().head_scratch([0, 0])

        if 't' in flag_list:
            print 'time'
            action = self.room_time.get_best_action()
            print action
            tmp_list[3] = 1
            idx = flag_list.index('t')

        if 'm' in flag_list:
            idx = flag_list.index('m')
            print type(word_list[idx])
            if u'点' in word_list[idx] and tmp_list[3] != 1:
                print 'time'
                action = self.room_time.get_best_action()
                print action
                tmp_list[3] = 1
            elif u'人' in word_list[idx] or (idx + 1 < len(word_list) and u'人' in word_list[idx + 1]):
                print 'attendance number'
                action = self.room_attend.get_best_action()
                print action
                tmp_list[2] = 1
            elif u'元' in word_list[idx] or (idx + 1 < len(word_list) and u'元' in word_list[idx + 1]):
                print 'costs'
                action = self.room_costs.get_best_action()
                print action
                tmp_list[1] = 1

if __name__ == '__main__':
    a = OrderRoom()
    b = raw_input('\t: ')
    while b != 'exit':
        a.parsing_sen(pseg.cut(b))
        b = raw_input('\t: ')

