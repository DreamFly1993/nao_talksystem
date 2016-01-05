# __Author__ = yazhao
# Coding='utf-8'
import random
import time


class PTalkingSys(object):

    def __init__(self):
        print 'Talking system for naoqi'
        self.state_m = 6
        self.action_n = 6
        self.q_lambda = 0.8
        self.matrix_q = [[0 for _ in range(self.action_n)] for _ in range(self.state_m)]
#        self.matrix_r = [[0 for _ in range(self.action_n)]] * self.state_m

        self.matrix_r = [[-1, -1, -1, -1, 0, -1], [-1, -1, -1, 0, -1, 100],
                         [-1, -1, -1, 0, -1, -1], [-1, 0, 0, -1, 0, -1],
                         [0, -1, -1, 0, -1, 100], [-1, 0, -1, -1, 0, 100]]
        self.matrix_trans = dict()
        print 'initiate finished'

    def count_qvalue(self, state, act):
        q_reward = self.matrix_r[state][act]
        state_new = self.matrix_q

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

    @staticmethod
    def parse_sentence(sentence):
        print 'parsing sentence module'
        print sentence
        return ''

    @property
    def constant(self):
        return ["Cons"]

    def __get_weather(self):
        self.constant
        print ''

a = PTalkingSys()
a.q_learning_moudle(10)
