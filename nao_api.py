# coding: utf-8
from naoqi import ALProxy
import random

__base_move = ['HeadYaw', 'HeadPitch', 'RShoulderPitch', 'RShoulderRoll', 'RElbowYaw',
               'RElbowRoll', 'RWristYaw', 'RHand', 'LShoulderPitch', 'LShoulderRoll',
               'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand', 'LHipYawPitch',
               'RHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'LAnklePitch',
               'LAnkleRoll', 'RHipRoll', 'RHipPitch', 'RKneePitch', 'RAnklePitch',
               'RAnkleRoll']

#global __action_dict
action_dict = {u'抬手': 'HandUp', u'伸手': 'HandOut', u'挠头': 'HeadScratch'}

# __action_dict = {u'点头': 'nodHead', u'表示同意': 'nodHead', u'点下头': 'nodHead',
#                 u'点个头': 'nodHead', u'点点头': 'nodHead', u'摇头': 'shakeHead',
#                 u'摇个头': 'shakeHead', u'摇下头': 'shakeHead',
#                 u'摇摇头': 'shakeHead', u'走': 'Walk', u'前进': 'Walk', u'前行': 'Walk',
#                 u'行进': 'Walk', u'行走': 'Walk', u'转': 'Turn', u'转身': 'Turn',
#                 u'转向': 'Turn', u'转个身': 'Turn', u'转过来': 'Turn',u'掉头': 'Turn',
#                 u'后退': 'WalkBack', u'抬手': 'HandUp', }

#   点头速度字典##词性a
speed_Dict = {u'慢吞吞': 'slow', u'慢': 'slow', u'慢慢': 'slow',
              u'缓慢': 'slow', u'极慢': 'slow', u'比较慢': 'slow',
              u'较慢': 'slow', u'快': 'quick', u'快速': 'quick',
              u'很快': 'quick', u'快点': 'quick'}

#   点头次数字典###词性m
__number_dict = {
    u'一次': 1, u'一下': 1, u'一': 1, u'两次': 2, u'两下': 2, u'两': 2,
    u'三次': 3, u'三下': 3, u'三': 3, u'四次': 4, u'四下': 4, u'四': 4,
    u'五次': 5, u'五下': 5, u'五': 5, u'六次': 6, u'六下': 6, u'六': 6,
    u'七次': 7, u'七下': 7, u'七': 7, u'八次': 8, u'八下': 8, u'八': 8,
    u'九次': 9, u'九下': 9, u'九': 9, u'十次': 10, u'十下': 10, u'十': 10
}

__direct_dict = {u'前': 'Forward', u'往前': 'Forward', u'向前': 'Forward', u'朝前': 'Forward',
                 u'左': 'Left', u'往左': 'Left', u'向左': 'Left', u'朝左': 'Left',
                 u'右': 'Right', u'往右': 'Right', u'向右': 'Right', u'朝右': 'Right',
                 u'后': 'Back', u'往后': 'Back', u'向后': 'Back', u'朝后': 'Back'}

__unit_dict = {u'米': 'M', u'm': 'M',
               u'分米': 'DM', u'dm': 'DM',
               u'厘米': 'CM', u'cm': 'CM'
               }
__fre_dict = {u'快': 'Fast', u'飞快': 'Fast', u'快速': 'Fast',
              u'慢': 'Slow', u'缓慢': 'Slow', u'慢慢': 'Slow',
              }

__ch_num = {u'一': 1, u'二': 2, u'两': 2, u'三': 3, u'四': 4,
            u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九':9,
            u'十': 10, u'零':0
            }

__ch_multi = {u'十': 10, u'百': 100, u'千': 1000, u'零': 0}


#   Naoqi api class
class NaoApi(object):

    # ALProxy.getJointName("Body") 获取每一个部位的电机名称 Body, LArm, LLeg, RLeg, RArm
    # ALProxy.angleInterpolation(name, angleLists, timeLists, isAbsolutes)
    #       absolute angle or relative angle
    # ALProxy.angleInterpolation("HeadYaw", 1.0, 1.0, True)
    # ALProxy.angleInterpolation("Head", [-1.0, -1.0], 1.0, True)
    # ALProxy.angleInterpolation("HeadYaw", [1.0, -1.0, 1.0, -1.0, 0.0],
    #                            [1.0,  2.0, 3.0,  4.0, 5.0], True)
    # ALProxy.angleInterpolation(["HeadYaw", "HeadPitch"], [[1.0, -1.0, 1.0, -1.0], [-1.0]],
    #                            [[1.0,  2.0, 3.0,  4.0], [5.0]], True)
    def __init__(self):
        print '连接至nao'
        self.__if_end = False
        robot_port = 9559
        robot_ip = '127.0.0.1'
        # 初始化动作模块
        self.motion_proxy = ALProxy("ALMotion", robot_ip, robot_port)
        self.memory_proxy = ALProxy("ALMemory", robot_ip, robot_port)

    def shake_head(self, act_parameter):
        """
        :param act_parameter: action parameters(shake times, shake speed)
        :return: true or false
        ALProxy.angleInterpolation(name, angleLists, timeLists, isAbsolutes)
        """
        print 'shake head'
        print act_parameter
        if type(act_parameter) != 'list':
            print u'参数错误'

        if len(act_parameter) != 2:
            print u'参数错误'

        # 摇头次数
        duration_num = act_parameter[0]
        # 动作时间
        act_time = act_parameter[1]

        if act_parameter[1] == 0:
            act_time = random.random() + 0.5

        if act_parameter[0] == 0:
            duration_num = random.randrange(0, 5)

        angles = random.random()
        for i in range(duration_num):
            self.motion_proxy.angleInterpolation("HeadYaw", angles, act_time, True)

    def do_action(self, act_name, act_parameter):
        print 'do action'
        act_name = act_name.decode('utf-8')
        if act_name in action_dict:
            print u'当前动作一直'
            act_code = action_dict[act_name]


    @property
    def set_to_end(self):
        self.__if_end = True
        return self.__if_end

