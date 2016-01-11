#Coding = 'utf-8'
import random

class OrderRoom(object):
    def __init__(self, q_num, ac_num):
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
        self.state_num = 3
        self.act_num = 5
        self.matrix_q = [[0 for _ in range(self.act_num)] for _ in range(self.state_num)]
        self.matrix_r = [[100, 1, 50, 1, 75],
                         [10, 100, 50, 75, 1],
                         [1, 10, 100, 10, 1]]
        self.q_lambda = 0.8

    def q_learning_teach(self, if_cancel):
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
        while if_cancel:
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

    def __del__(self):
        print 'del function'

