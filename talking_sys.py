# coding: utf-8
import random
import jieba
import jieba.posseg as pseg
from utils import Write2Log as tolog
import time
import order_room
import nao_api
import get_weather


class PTalkingSys(object):

    def __init__(self):
        """
        demonstrating robot, mainly used for show MDS or DS
        Introduces: system contains
            1) active function units lists
            2) all function units
            3) history action lists(talking sentences, parsing answers)
        :return:
        """
        print 'Talking system for naoqi'
        self.state_m = 6
        self.action_n = 6
        self.q_lambda = 0.8
        self.__unit_time = time.time()
        self.word2mean = {'会议室': 'room', '开会': 'room', '天气': 'weather', '摘要': 'abstract'}
        self.matrix_q = [[0 for _ in range(self.action_n)] for _ in range(self.state_m)]
#        self.matrix_r = [[0 for _ in range(self.action_n)]] * self.state_m

        # active unit queue
        self.__active_unit = []
        # history unit queue
        self.__history_unit = []

        self.matrix_r = [[-1, -1, -1, -1, 0, -1], [-1, -1, -1, 0, -1, 100],
                         [-1, -1, -1, 0, -1, -1], [-1, 0, 0, -1, 0, -1],
                         [0, -1, -1, 0, -1, 100], [-1, 0, -1, -1, 0, 100]]

        self.matrix_trans = dict()
        print 'initiate finished'

    def q_learning_moudle(self, exploid_num):
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
        :return:
        """
        print 'q_learning for training'
        print '__begin__'
        self.q_lambda = 0.8
        for i in range(exploid_num):
            print i
            cur_state = random.randrange(0, 6)
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

    @property
    def unit_time(self):
        return self.__unit_time

    @unit_time.setter
    def unit_time(self, value):
        self.__unit_time = value

    def sen_parse(self, in_sen):
        print u'sentence parsing unit'
        print 'input_sen: ' + in_sen
        print len(in_sen)
        in_sen = raw_input('please input the sentence you want to say: ')
        print type(in_sen)
        in_sen = in_sen.decode('utf-8')
        print len(in_sen)
        in_list = pseg.cut(in_sen)
        for w in in_list:
            print w.word + w.flag

    def do_work(self, cur_sen):
        if '会议室' in cur_sen or '开会' in cur_sen:
            active_unit = order_room.OrderRoom()
            self.__active_unit.append(active_unit)
            while active_unit.do_work(pseg.cut(cur_sen)) != '':
                cur_sen = raw_input('\t: ')
        if '天气' in cur_sen:
            weather = get_weather.GetWeather()
            if '今天' in cur_sen:
                weather.date = [0]
            elif '近两天' in cur_sen:
                weather.date = [0, 1]
            elif '近几天' in cur_sen:
                weather.date = [0, 1, 2]
            sen = weather.get_weather_data()
            nao_api.naoqi_api().say_something(sen)
            print 'get weather'
        print 'order end!'

if __name__ == '__main__':
    a = PTalkingSys()
    input_seg = raw_input('\t: ')
    while input_seg != 'exit':
        a.do_work(input_seg)
        input_seg = raw_input('\t: ')

#    b = pseg.cut('帮我定一个下午十点，200人左右的会议室')
#    for work in b:
#        print work.word + ' ' + work.flag

#   a.q_learning_moudle(10)
