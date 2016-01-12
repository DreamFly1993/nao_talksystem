# coding: utf-8
#from naoqi import ALProxy
import time
import jieba.posseg as pseg


# jieba.load_userdict("C:\Python26\userdict.txt")

base_move = ['HeadYaw','HeadPitch','RShoulderPitch','RShoulderRoll','RElbowYaw'
             ,'RElbowRoll','RWristYaw','RHand','LShoulderPitch','LShoulderRoll'
             ,'LElbowYaw','LElbowRoll','LWristYaw','LHand','LHipYawPitch','RHipYawPitch'
             ,'LHipRoll','LHipPitch','LKneePitch','LAnklePitch','LAnkleRoll','RHipRoll'
             ,'RHipPitch','RKneePitch','RAnklePitch','RAnkleRoll']


####动作集合需要拓展：
Action_Dict = {u'点头':'nodHead',u'表示同意':'nodHead',u'点下头':'nodHead',
             u'点个头':'nodHead',u'点点头':'nodHead',u'摇头':'shakeHead',
             u'摇个头':'shakeHead',u'摇下头':'shakeHead',
               u'摇摇头':'shakeHead',u'走':'Walk',u'前进':'Walk',u'前行':'Walk',u'行进':'Walk',u'行走':'Walk',
             u'转':'Turn',u'转身':'Turn',u'转向':'Turn',u'转个身':'Turn',u'转过来':'Turn',u'掉头':'Turn',
             u'后退':'WalkBack'}

#   点头速度字典##词性a
speed_Dict = {u'慢吞吞':'slow',u'慢':'slow',u'慢慢':'slow',u'缓慢':'slow', u'极慢':'slow',u'比较慢':'slow',u'较慢':'slow'
            ,u'快':'quick',u'快速':'quick',u'很快':'quick',u'快点':'quick'}

#   点头次数字典###词性m
number_Dict = {
    u'一次': 1, u'一下': 1, u'一': 1, u'两次': 2, u'两下': 2, u'两': 2,
    u'三次': 3, u'三下': 3, u'三': 3, u'四次': 4, u'四下': 4, u'四': 4,
    u'五次': 5, u'五下': 5, u'五': 5, u'六次': 6, u'六下': 6, u'六': 6,
    u'七次': 7, u'七下': 7, u'七': 7, u'八次': 8, u'八下': 8, u'八': 8,
    u'九次': 9, u'九下': 9, u'九': 9, u'十次': 10, u'十下': 10, u'十': 10
}

Direc_Dict={u'前':'Forward',u'往前':'Forward',u'向前':'Forward',u'朝前':'Forward',
            u'左':'Left',u'往左':'Left',u'向左':'Left',u'朝左':'Left',
            u'右':'Right',u'往右':'Right',u'向右':'Right',u'朝右':'Right',
            u'后':'Back',u'往后':'Back',u'向后':'Back',u'朝后':'Back',
           }

Unit_Dict={u'米':'M',u'm':'M',
           u'分米':'DM',u'dm':'DM',
           u'厘米':'CM',u'cm':'CM'
           }
Fre_Dict= {u'快':'Fast',u'飞快':'Fast',u'快速':'Fast',
           u'慢':'Slow',u'缓慢':'Slow',u'慢慢':'Slow',
           }

Ch_Num={u'一':1,u'二':2,u'两':2,u'三':3,u'四':4,u'五':5,u'六':6,u'七':7,u'八':8,u'九':9,u'十':10,u'零':0}
Ch_Multi={u'十':10,u'百':100,u'千':1000,u'零':0}



def NAO_Motion_Switch(Verb,timesnum,Speed,self,Direc,Ch_Fre,Lenth):
    if Verb in Action_Dict: #如果存在这个键
        if Action_Dict[Verb]=='nodHead':##如果是点十次头以上未解决！！！！
            if timesnum in number_Dict:
                nodHead(self, number_Dict[timesnum], Speed)
            else:
                nodHead(self, 3, Speed)
        elif Action_Dict[Verb]=='shakeHead':##若添加动作从这个层次添加elif
            if timesnum in number_Dict:##如果是摇十次头以上未解决！！！！
                shakeHead(self, number_Dict[timesnum], Speed)
            else:
                shakeHead(self,3,Speed)
        elif Ch_Fre=='No':
            if Action_Dict[Verb]=='Walk':
                if  Direc in Direc_Dict:
                    if  Direc_Dict[Direc]=='Forward':
                        self.walkTo(Lenth,0,0)
                    if  Direc_Dict[Direc]=='Left':
                        self.walkTo(0,Lenth,0)
                    if  Direc_Dict[Direc]=='Right':
                        self.walkTo(0,(-1)*Lenth,0)
                    if  Direc_Dict[Direc]=='Back':
                        self.walkTo((-1)*Lenth,0,0)
                else:
                    self.walkTo(Lenth,0,0)

            elif  Action_Dict[Verb]=='Turn':
                if  Direc in Direc_Dict:
                    if  Direc_Dict[Direc]=='Left':
                        TurnLeft(self)
                    elif  Direc_Dict[Direc]=='Right':
                        TurnRight(self)
                    elif  Direc_Dict[Direc]=='Back':
                        TurnRound(self)
                    else:
                        print u"执行转身"
                        TurnRound(self)
                else:
                    print u"执行转身"
                    TurnRound(self)
            elif  Action_Dict[Verb]=='WalkBack':
                self.walkTo((-1)*Lenth,0,0)
        elif Ch_Fre!='No':
            if Ch_Fre in Fre_Dict:
                if Fre_Dict[Ch_Fre]=='Fast':
                    Frequency=1.0
                    Step=1.0
                if Fre_Dict[Ch_Fre]=='Slow':
                    Frequency=0.1
                    Step=0.1
            if Verb in Action_Dict: #如果存在这个键
                if Action_Dict[Verb]=='Walk':
                    if Direc in Direc_Dict:
                        if Direc_Dict[Direc]=='Forward':
                            self.setWalkTargetVelocity(Step, 0, 0,Frequency)
                            time.sleep(0.5)
                            To_wait=Lenth/self.getRobotVelocity ()[0]-0.5
                            print To_wait
                            time.sleep(To_wait)
                            self.setWalkTargetVelocity(0, 0, 0,0)
                        if Direc_Dict[Direc]=='Left':
                            self.setWalkTargetVelocity(0,Step,0,Frequency)
                            time.sleep(0.5)
                            To_wait=Lenth/self.getRobotVelocity ()[1]-0.5
                            time.sleep(To_wait)
                            self.setWalkTargetVelocity(0, 0, 0,0)
                        if Direc_Dict[Direc]=='Right':
                            self.setWalkTargetVelocity(0,(-1)*Step,0,Frequency)
                            time.sleep(0.5)
                            To_wait=(-1)*Lenth/self.getRobotVelocity ()[1]-0.5
                            time.sleep(To_wait)
                            self.setWalkTargetVelocity(0, 0, 0,0)
                        if Direc_Dict[Direc]=='Back':
                            self.setWalkTargetVelocity((-1)*Step, 0, 0,Frequency)
                            time.sleep(0.5)
                            To_wait=(-1)*Lenth/self.getRobotVelocity ()[0]-0.5
                            time.sleep(To_wait)
                            self.setWalkTargetVelocity(0, 0, 0,0)
                    else:
                        self.setWalkTargetVelocity(Step, 0, 0,Frequency)
                        time.sleep(0.5)
                        To_wait=Lenth/self.getRobotVelocity ()[0]-0.5
                        time.sleep(To_wait)
                        self.setWalkTargetVelocity(0, 0, 0,0)
                elif Action_Dict[Verb]=='Turn':
                    if  Direc in Direc_Dict:
                        if  Direc_Dict[Direc]=='Left':
                            TurnLeft(self)
                        if  Direc_Dict[Direc]=='Right':
                            TurnRight(self)
                        if  Direc_Dict[Direc]=='Back':
                            TurnRound(self)
                        else:
                            print u"执行转身"
                            TurnRound(self)
                    else:
                        print u"执行转身"
                        TurnRound(self)
                elif Action_Dict[Verb]=='WalkBack':
                    self.setWalkTargetVelocity((-1)*Step, 0, 0,Frequency)
                    time.sleep(0.5)
                    To_wait=(-1)*Lenth/self.getRobotVelocity ()[0]-0.5
                    time.sleep(To_wait)
                    self.setWalkTargetVelocity(0,0,0,0)
    else:
        print '进入附加的动作'


def to(str_num):
    first = str_num[:2]
    _sum = 0

    if len(first) == 1:
        return Ch_Num[first]
    elif len(first) == 0:
        return 0
    else:
        a = first[:1]
        b = first[1:]

        if a in Ch_Num:
            if b in Ch_Multi:
                _sum = Ch_Num[a]*Ch_Multi[b]
        c = str_num[2:]
        return _sum + to(c)


###建立功能层函数1=点头0=摇头
def nodHead(self, timesnum, speed):
    name = "HeadPitch"
    angleLists = [1.0,0.0]
    t = 0.5
    isAbsolute = True
    if speed_Dict[speed] == 'quick':
        t = 0.25
        times = [t, 2*t]
        for i in range(0, timesnum):
            self.angleInterpolation(name,angleLists,times,isAbsolute)
    elif speed_Dict[speed] == 'slow':
        t = 1
        times = [t,2*t]
        for i in range(0,timesnum):
            self.angleInterpolation(name,angleLists,times,isAbsolute)
    else:
        times = [t,2*t]
        for i in range(0,timesnum):
            self.angleInterpolation(name,angleLists,times,isAbsolute)


# 摇头函数
def shakeHead(self, timesnum, speed):
    name = "HeadYaw"
    angleLists = [1.0,0.0,-1.0,0]
    t = 0.5
    isAbsolute = True
    if speed_Dict[speed] =='quick':
        t=0.25
        times = [t,2*t,3*t,4*t]
        for i in range(0,timesnum):
            self.angleInterpolation(name,angleLists,times,isAbsolute)
    elif speed_Dict[speed] == 'slow':
        t=1
        times = [t,2*t,3*t,4*t]
        for i in range(0,timesnum):
            self.angleInterpolation(name,angleLists,times,isAbsolute)
    else:
        times = [t,2*t,3*t,4*t]
        for i in range(0,timesnum):
            self.angleInterpolation(name,angleLists,times,isAbsolute)


# 一些简单移动函数
def TurnLeft(self):
   self.walkTo(0, 0, 1.57)


def TurnRight(self):
   self.walkTo(0,0,-1.57)


def WalkForward(self,DistanceX):
   self.walkTo(DistanceX,0,0)


def WalkBack(self,DistanceX):
   self.walkTo((-1)*DistanceX,0,0)


def TurnRound(self):
   self.walkTo(0,0,-3.14)


def StopMoving(self):
    self.setWalkTargetVelocity(0,0,0,0)


# 判断一个unicode是否为汉字
def is_chinese(uchar):
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            print "是汉字"
            return True
        else:
            print "不是汉字"
            return False


#判断一个unicode是否为数字
def is_number(uchar):
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False



#main主函数开始处：
#连接机器人基础信息
PORT = 9559
# robotIP = "10.108.225.116"#10.108.225.229"
robotIP = "127.0.0.1"

# 程序开始部分：

NAOmotion = ALProxy("ALMotion", robotIP, PORT) # 初始化
memProxy = ALProxy("ALMemory", robotIP, PORT)

#初始化默认参数值
Ch_Action = 'NO'
CH_timesnum = u'一次'
CH_Speed = u'慢'
Ch_Direc = 'No'
Ch_Fre = 'No'

# 没有说明距离的情况下默认走
FinalLenth_M = 0.15
inst = 'OK'
isAbsolute = True
num_dict = []

print '现在开始 Starting NOW :'
while inst != 'exit':
    inst = raw_input(u"(必须要有速度信息,exit结束)请输入你的指令:")
    ##匹配方式和分词有很大问题
    words=pseg.cut(inst)
    ###需要采用重复提取方式 否则有可能出错 词性不一致
    for w in words:
        print w.word,w.flag
        if w.flag=='m':
            CH_timesnum=w.word
            if is_number(w.word):#阿拉伯数字的char型
                Float_Lenth=float(w.word)
            if is_chinese(w.word):#中文unicode的char型
                 y=w.word
                 temp=to(y.replace(u'零',u'零零'))
                 print type(temp),temp
                 Float_Lenth=float(temp)
        if w.flag=='v':
            Ch_Action=w.word
        if w.flag=='f':
            Ch_Direc=w.word
        if w.flag=='a':
            CH_Speed=w.word
            Ch_Fre=w.word
        if w.flag=='d':
            CH_Speed=w.word
        if w.flag=='q'or'eng':
            Ch_Unit=w.word
            if Ch_Unit in Unit_Dict:
                if Unit_Dict[Ch_Unit]=='CM':
                    FinalLenth_M=0.01*Float_Lenth
                elif Unit_Dict[Ch_Unit]=='DM':
                    FinalLenth_M=0.1*Float_Lenth
                elif Unit_Dict[Ch_Unit]=='M':
                    FinalLenth_M=Float_Lenth
             #else:                          #不写单位默认是m
                  #FinalLenth_M=Float_Lenth
                print u"执行运动",FinalLenth_M,'米'

    if (Ch_Action=='NO') :#or (CH_Speed=='NO')
        #存在没匹配的信息
        print '存在未匹配的信息'
        print '请重新输入'
    else:
        #信息全部都匹配了（名称、速度）
        if CH_timesnum in number_Dict:
            if number_Dict[CH_timesnum]=='one':
                num_of_action = 1
            elif number_Dict[CH_timesnum]=='two':
                num_of_action = 2
            elif number_Dict[CH_timesnum]=='three':
                num_of_action = 3
            elif number_Dict[CH_timesnum]=='four':
                num_of_action = 4
            elif number_Dict[CH_timesnum]=='five':
                num_of_action = 5
            elif number_Dict[CH_timesnum]=='six':
                num_of_action = 6
            elif number_Dict[CH_timesnum]=='seven':
                num_of_action = 7
            elif number_Dict[CH_timesnum]=='eight':
                num_of_action = 8
            elif number_Dict[CH_timesnum]=='nine':
                num_of_action = 9
            elif number_Dict[CH_timesnum]=='ten':
                num_of_action = 10
            else:
                num_of_action = 1
        else:
            num_of_action = 1
        if Ch_Action in Action_Dict:
            ##存入动作
            file_move_past = open('./movement_past.txt', 'a')#打开文件
            file_move_past.writelines([Action_Dict[Ch_Action], '\t', str(num_of_action),'\t',speed_Dict[CH_Speed],'\n'])
            file_move_past.close()
            #加上运动频率的量
            ##处理行内容 匹配 修改频率
            file_move_fre = open('D:/For NAO/test/3.29/movement_frequence.txt','a+')
            line=file_move_fre.readline()
            movement_flag = 0
            lines = []
            while line:
                str_tmp = line[:line.find('\t')]
                if Action_Dict[Ch_Action] == str_tmp:
                    movement_flag = 1
                    num_tmp =line[line.find('\t')+1:]
                    num = int(num_tmp) + 1
                    line= line.replace(num_tmp,str(num))
                    line = line + '\n'
                lines.append(line)
                line = file_move_fre.readline()
            file_move_fre.close()
            if movement_flag == 1:
                file_move_fre = open('D:/For NAO/test/3.29/movement_frequence.txt','w+')
                file_move_fre.writelines(lines)
                file_move_fre.close()
                print '运动频率已经修改'
            else:
                file_move_fre = open('D:/For NAO/test/3.29/movement_frequence.txt','a')
                #如果运动在字典中但频率文件没有（第一次调用该动作）
                file_move_fre.write(Action_Dict[Ch_Action]+'\t'+str(1)+'\n')
                file_move_fre.close()
            NAO_Motion_Switch(Ch_Action,CH_timesnum,CH_Speed,NAOmotion,Ch_Direc,Ch_Fre,FinalLenth_M)
            #函数需要添加已知动作，没有整合师兄的动作
        else:
            move_page = 0
            #词都有，动作没有
            move_in_txt = ''
            #先从movement.txt中寻找看有没有教过机器人
            file_move = open('./movement.txt', 'r+')
            line = file_move.readline()
            while line:
                #print line
                if line.find('YY') != -1:
                    move_page = move_page + 1
                    line_tmp = line
                    while line_tmp.find('\t') != -1:
                        num_tmp = line.find('\t')
                        line_tmp = line_tmp[num_tmp + 1:]
                        str_tmp = line_tmp[:line_tmp.find('\t')]
                        str_tmp = str_tmp.decode('gbk').encode('utf-8')
                        Ch_Action_tmp = Ch_Action.encode('utf-8')
                        if Ch_Action_tmp == str_tmp:
                            move_in_txt = str_tmp
                            #判断得到动作交给过机器人
                            break
                if move_in_txt == '':
                    line=file_move.readline()
                else:
                    break
            #print 'move_in_txt'
            #print move_in_txt
            file_move.close()
            #print 'find that in ' + str(move_page)
            if move_in_txt != '':
                print 'previous action have been taught!'
                #该从文件中读取move_in_txt的具体动作了 名字为中文的
                file_move_ed = open('D:/For NAO/test/3.29/movement.txt','r+')
                name_list = []
                angle_list = []
                time_list = []
                move_count = 0
                move_flag = 0
                move_page_tmp = 0
                while line:
                    #读入一行，读入信息
                    while move_page_tmp!=move_page:
                        line = file_move_ed.readline()
                        if line.find('YY') != -1:
                            move_page_tmp=move_page_tmp +1
                            continue
                        else:
                            #print 'move_page_tmp=  ' + str(move_page_tmp)
                            if line.find('YY')!= -1:
                                #print'Find YY '
                                #print line
                                if move_flag == 0:
                                    move_flag = 1
                                    line = file_move_ed.readline()
                                else:
                                    print 'Reading movements complete.'
                                    break
                            else:
                                #print 'Reload information：'
                                #print line
                                move_count= move_count + 1
                                num_tmp=line.find('\t')
                                inf_tmp=line[:num_tmp]
                                #print inf_tmp
                                name_list.append(inf_tmp)
                                line=line[num_tmp+1:]
                                #多关节位置没解决(动作学习时加一个标志如A)
                                num_tmp=line.find('\t')
                                inf_tmp=line[:num_tmp]
                                int_tmp=float(inf_tmp)
                                #print inf_tmp
                                angle_list.append(int_tmp)
                                line=line[num_tmp+1:]
                                #多时序没解决(读到结尾\n)
                                num_tmp=line.find('\t')
                                inf_tmp=line[:num_tmp]
                                int_tmp=float(inf_tmp)
                                #print inf_tmp
                                time_list.append(int_tmp)
                                line=line[num_tmp+1:]
                                line = file_move_ed.readline()
                                #信息读取完成
                file_move_ed.close()
                #做出该动作！！！！！！
                print 'Now i will do it as you order.'
                #先把angle time 数据编程列表类型
                for j in range(0,num_of_action):
                    for i in range(move_count):
                        NAOmotion.angleInterpolation(name_list[i],angle_list[i],time_list[i],isAbsolute)
                        #print i
            else:
                print '动作没交给过机器人'
                name_tmp = ''
                angleLists_tmp = ''
                times_tmp = ''
                #动作教学开始处
                print "这个动作我不知道，你想要教我吗？是的话告诉我"
                print "y for yes , n for no"
                inst_tmp = raw_input('想说什么：')
                if inst_tmp == 'y':
                    file_move= open('D:/For NAO/test/3.29/movement.txt','a')
                    file_move.writelines(['YY','\t'])
                    #Ch_Action=Ch_Action.encode('utf')
                    #file_move.writelines([Ch_Action,'\t'])#!!!!!!!!
                    #file_move.write('\t')
                    inst_tmp = raw_input('想教我这个动作刚才输入的的名字？：')
                    while inst_tmp != 'exit':
                        file_move.writelines([inst_tmp, '\t'])
                        inst_tmp = raw_input('想教我这个动作还有没有其他的名字？(输入exit可继续)：')
                        #inst_tmp = inst_tmp.encode('utf')
                    file_move.write('\n')
                    #开始输入运动具体信息：
                    inst_tmp = raw_input('（输入结束完成具体指令教学）需要运动的关节是哪里？（例如：‘HeadYaw’）：')
                    while inst_tmp != 'exit':
                        if inst_tmp in base_move:
                            #查看是否存在这个关节
                            #这个关节存在
                            name_list = []
                            angle_list = []
                            time_list = []
                            file_move.writelines([inst_tmp, '\t'])
                            inst_tmp = raw_input('请输入运动的关节位置信息(输入到exit为结尾)：')
                            while inst_tmp != 'exit':
                                angle_list.append(inst_tmp)
                                inst_tmp = raw_input('请输入运动的关节位置信息(输入到exit为结尾)：')
                            file_move.writelines(angle_list)
                            file_move.writelines('\t')
                            inst_tmp = raw_input('请输入运动的时间信息(输入到exit为结尾)：')
                            while inst_tmp != 'exit':
                                time_list.append(inst_tmp)
                                inst_tmp = raw_input('请输入运动的时间信息(输入到exit为结尾)：')
                            file_move.writelines(time_list)
                            file_move.writelines('\n')
                            inst_tmp = raw_input('（输入 exit 完成具体指令教学）需要运动的关节是哪里？（例如：‘HeadYaw’）：')
                        else:
                            # 这个关节不存在
                            print '这个关节我没有'
                            inst_tmp = raw_input('（输入 exit 完成具体指令教学）需要运动的关节是哪里？（例如：‘HeadYaw’）：')

                    file_move.close()
                    print "是否需要作出此动作？"
                    print "y for yes , n for no"
                    inst_tmp = raw_input('想说什么：')
                    if inst_tmp == 'y':
                        print 'previous action have been taught!'
                        #该从文件中读取move_in_txt的具体动作了 名字为中文的
                        file_move_ed = open('D:/For NAO/test/3.29/movement.txt','r+')
                        name_list = []
                        angle_list = []
                        time_list = []
                        move_count = 0
                        move_flag = 0
                        move_page_tmp = 0
                        while line:
                        #读入一行，读入信息
                            while move_page_tmp!=move_page:
                                line = file_move_ed.readline()
                                if line.find('YY') != -1:
                                    move_page_tmp=move_page_tmp +1
                                    continue
                                else:
                                    print 'move_page_tmp=  ' + str(move_page_tmp)
                                    if line.find('YY')!= -1:
                                        print'Find YY '
                                        print line
                                        if move_flag == 0:
                                            move_flag = 1
                                            line = file_move_ed.readline()
                                        else:
                                            print 'Reading movements complete.'
                                            break
                                    else:
                                        move_count = move_count + 1
                                        num_tmp = line.find('\t')
                                        inf_tmp = line[:num_tmp]
                                        # print inf_tmp
                                        name_list.append(inf_tmp)
                                        line = line[num_tmp+1:]
                                        # 多关节位置没解决(动作学习时加一个标志如A)
                                        num_tmp = line.find('\t')
                                        inf_tmp = line[:num_tmp]
                                        int_tmp = float(inf_tmp)
                                        # print inf_tmp
                                        angle_list.append(int_tmp)
                                        line = line[num_tmp+1:]
                                        # 多时序没解决(读到结尾\n)
                                        num_tmp = line.find('\t')
                                        inf_tmp = line[:num_tmp]
                                        int_tmp = float(inf_tmp)
                                        # print inf_tmp
                                        time_list.append(int_tmp)
                                        line = line[num_tmp+1:]
                                        line = file_move_ed.readline()
                                        # 信息读取完成
                        file_move_ed.close()

                        #做出该动作！！！！！！
                        print 'Now i will do it as you order.'

                        #先把angle time 数据编程列表类型
                        for j in range(0,num_of_action):
                            for i in range(move_count):
                                NAOmotion.angleInterpolation(name_list[i],angle_list[i],time_list[i],isAbsolute)

                else:
                    print 'OK 那你想让我做什么'
                    inst = raw_input(u"(必须要有速度信息,exit结束)请输入你的指令:")
else:
    StopMoving(NAOmotion)
    print "Good Bye！"
