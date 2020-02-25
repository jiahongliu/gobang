import pygame
from sys import exit
from pygame.locals import *
import sys
import random


pygame.init()
i,j = None,None
bg=pygame.image.load('bkyellow.jpg')#加载背景图片
white=pygame.image.load('white.png')#加载白子图片
black=pygame.image.load('black.png')#加载黑子图片

# sound=pygame.mixer.music.load('sound.mp3')#加载音效mp3

font1 = pygame.font.Font('jhl.TTF', 35)#加载字体信息
win_text = font1.render(u"白子胜  !!!", True,(255,0,255))
lose_text = font1.render(u"黑子胜  !!!", True, (255,255,0))
play_text = font1.render(u"再玩一局", True,(255,255,255))
menu_text = font1.render(u'主菜单', True, (255,255,255))

difficulty_text=font1.render(u'选择难度',True,(255,255,255))
easy_text=font1.render(u'简单',True,(255,255,255))
difficult_text=font1.render(u'困难',True,(255,255,255))

font2 = pygame.font.Font('jhl.TTF',15)
text5 = font2.render(u'点 击 鼠 标 右 键 悔 棋', True, (0,0,0))

#登录选项
text1 = font1.render(u"玩家与玩家", True,(255,255,255))
text2 = font1.render(u'玩家与电脑', True,(255,255,255))
text3 = font1.render(u'声音：  开', True,(255,255,255))
text4 = font1.render(u'声音：  关', True,(255,255,255))

all_chess=[]#存位置

bw_in=[[0 for i in range(15)] for i in range(15)]#储存黑白子情况 0无子 1白子 2黑子

tuple_score=[None]*10
tuple_score[0]=7                #没有子
tuple_score[1]=35				#一个己方子
tuple_score[2]=800				#两个己方子
tuple_score[3]=15000			#三个己方子
tuple_score[4]=800000			#四个己方子
tuple_score[5]=15				#一个对方子
tuple_score[6]=400				#两个对方子
tuple_score[7]=8000			    #三个对方子
tuple_score[8]=100000			#四个对方子
tuple_score[9]=0				#又有白又有黑

#根据黑白子情况返回分数
def chess_check(black_num,white_num):
    global tuple_score
    if black_num==0 and white_num==0:#没有子 7分
        pos_tuple_score=tuple_score[0]
    elif black_num>0 and white_num>0: 	#又有白又有黑 0分
        pos_tuple_score=tuple_score[9]
    else:                             	#只有黑或者只有
        if black_num != 0:				#计算黑子
            pos_tuple_score=tuple_score[black_num]
        if white_num != 0:				#计算白子
            pos_tuple_score=tuple_score[white_num+4]
    return pos_tuple_score##计算一个空位的分数（需要棋谱数组和空位位置，返回该位置的分数）

#判断位置的分数
def chess_score(array,chess_pos):
    pos_score=0#记录子的数值
    x=chess_pos[0]
    y=chess_pos[1]
    black_num=0#记录黑子数量
    white_num=0#记录白子数量
    ##竖列
    for i in range(5):#1234  统计竖列所有五元组的得分总和
        for j in range(5):#01234 统计一个五元组的得分
            if [x-j+i,y] in array[::2]:#黑子判断横向
                black_num+=1
            if [x-j+i,y] in array[1::2]:#白子判断横向
                white_num+=1
        pos_score=pos_score+chess_check(black_num, white_num)#计算一个元组
        white_num=0
        black_num=0
    #横列
    for i in range(5):#1234  统计竖列所有五元组的得分总和
        for j in range(5):#01234 统计一个五元组的得分
            if [x,y-j+i] in array[::2]:#黑子判断竖向
                black_num+=1
            if [x,y-j+i] in array[1::2]:#白子判断竖向
                white_num+=1
        pos_score=pos_score+chess_check(black_num, white_num)#计算一个元组
        white_num=0
        black_num=0
	##左斜/
    for i in range(5):#1234  统计竖列所有五元组的得分总和
        for j in range(5):#01234 统计一个五元组的得分
            if [x+j-i,y-j+i] in array[::2]:#黑子判断右下斜
                black_num+=1
            if [x+j-i,y-j+i] in array[1::2]:#白子判断右下斜
                white_num+=1
        pos_score=pos_score+chess_check(black_num, white_num)#计算一个元组
        white_num=0
        black_num=0
	##右斜\
    for i in range(5):#1234  统计竖列所有五元组的得分总和
        for j in range(5):#01234 统计一个五元组的得分
            if [x-j+i,y-j+i] in array[::2]:#黑子判断左下斜
                black_num+=1
            if [x-j+i,y-j+i] in array[1::2]:#白子判断左下斜
                white_num+=1
        pos_score=pos_score+chess_check(black_num, white_num)#计算一个元组
        white_num=0
        black_num=0
    return pos_score

#找到分数最大的位置
def find_maxscore(array):
    if array==[]:
        best_pos=[7,7]
    else:
        chess_score_array=[]
        for row in range(15):
            for col in range(15):
                chess_pos = [row,col]
                if chess_pos not in array:
                    pos_score=chess_score(array,chess_pos)
                    chess_score_array.append([pos_score, row, col])
        chess_score_array.sort(reverse=True)
        #随机落子
        if chess_score_array[0][0]-chess_score_array[2][0]<50:
            choose_pos=random.randint(0,2)
        elif chess_score_array[0][0]-chess_score_array[1][0]<100:
            choose_pos=random.randint(0,1)
        else :
            choose_pos=0
        pc_pressed_x=chess_score_array[choose_pos][1]
        pc_pressed_y=chess_score_array[choose_pos][2]
        best_pos=[pc_pressed_x,pc_pressed_y]
		#print(best_pos)
    return best_pos

#定义一个函数判断输赢
def is_win():
    global bw_in
    for x in range(15):
        for j in range(11):
            b=j+1
            c=j+2
            d=j+3
            e=j+4
            if bw_in[x][j]==bw_in[x][b]==bw_in[x][c]==bw_in[x][d]==bw_in[x][e]==2:
                return 'blk'
            if bw_in[x][j]==bw_in[x][b]==bw_in[x][c]==bw_in[x][d]==bw_in[x][e]==1:
                return 'wht'
            if bw_in[j][x]==bw_in[b][x]==bw_in[c][x]==bw_in[d][x]==bw_in[e][x]==2:
                return 'blk'
            if bw_in[j][x]==bw_in[b][x]==bw_in[c][x]==bw_in[d][x]==bw_in[e][x]==1:
                return 'wht'
    for xx in range(11):
        for yy in range(11):
            if bw_in[xx][yy]==bw_in[xx+1][yy+1]==bw_in[xx+2][yy+2]==bw_in[xx+3][yy+3]==bw_in[xx+4][yy+4]==1:
                return 'wht'
            if bw_in[xx][yy]==bw_in[xx+1][yy+1]==bw_in[xx+2][yy+2]==bw_in[xx+3][yy+3]==bw_in[xx+4][yy+4]==2:
                return 'blk'
            if bw_in[14-xx][yy]==bw_in[13-xx][yy+1]==bw_in[12-xx][yy+2]==bw_in[11-xx][yy+3]==bw_in[10-xx][yy+4]==1:
                return 'wht'
            if bw_in[14-xx][yy]==bw_in[13-xx][yy+1]==bw_in[12-xx][yy+2]==bw_in[11-xx][yy+3]==bw_in[10-xx][yy+4]==2:
                return 'blk'

#主函数
def main():

    is_end=False
    is_paly=False
    is_AI=False
    #标志做出选择
    is_choose=False

    is_have_sound=True

    is_people=False

    is_white=False
    is_black=False

    is_sound=False

    is_menu=False

    is_playagain=False

    while True:
        is_check=0
        screen = pygame.display.set_mode((600,600))
        screen.blit(bg,(0,0))
        screen.blit(text5,(230,0))

        if not is_choose:
            screen.blit(text1,(220,120))
            screen.blit(text2,(220,220))
            if not is_have_sound:
                screen.blit(text4,(220,320))
            else:
                screen.blit(text3,(220,320))

        if not is_end:
            if is_AI:
                hh=find_maxscore(all_chess)
                all_chess.append(hh)
                is_sound=True
                is_AI=False
                is_paly=True
        
        if is_people:
            is_paly=True
        
        # if is_sound:
        #     pygame.mixer.music.play(0)
        #     pygame.mixer.music.set_volume(1)
        #     is_sound=False
        
        # pygame中有鼠标 键盘 手柄 用户定义等各种事件
        for event in pygame.event.get():
            #接收到退出事件后退出程序
            if event.type == QUIT:
                pygame,quit()
                exit()

            if event.type==pygame.MOUSEBUTTONDOWN:#鼠标左键点击添加白子坐标
                if event.button == 1:
                    if not is_choose:
                        pos=pygame.mouse.get_pos()
                        if 220<=pos[0]<=395 and 120<=pos[1]<=155:#人人
                            is_choose=True
                            is_people=True
                        if 220<=pos[0]<=395 and 220<=pos[1]<=255:#人机
                            is_choose=True
                            is_AI=True
                        if 220<=pos[0]<=395 and 320<=pos[1]<=355:#声音
                            is_have_sound=not is_have_sound
                    
                    if is_end:
                        poss=pygame.mouse.get_pos()
                        if 160<=poss[0]<=300  and 300<=poss[1]<=335:
                            is_playagain=True
                        if 320<=poss[0]<=390  and 300<=poss[1]<=335:
                            is_menu=True
                            is_choose=False

                    if not is_end:
                        if is_paly:
                            pressed_x,pressed_y = pygame.mouse.get_pos()
                            poinx=int(pressed_x/40)
                            poiny=int(pressed_y/40)
                            if bw_in[poinx][poiny]==0:
                                chess_k=[poinx,poiny]
                                all_chess.append(chess_k)
                                if not is_people:
                                    is_paly=False
                                    is_AI=True
                                # is_sound=True

                if event.button == 3:
                    if len(all_chess)>=2:
                        for chess in all_chess[-2:]:
                            x1,y1=chess
                            bw_in[x1][y1]=0
                        del all_chess[-2:]
                            
        #添加白子
        for chess_jj in all_chess[1::2]:
            d=40
            i_tmp,j_tmp =chess_jj
            # 判断标号是否有效
            if i_tmp in range(15) and j_tmp in range(15):
                i = i_tmp
                j = j_tmp            
            if not i is None and not j is None:
                bw_in[i][j]=1                            
                piece_chessboard_x,piece_chessboard_y = i*d+15,j*d+15                
                    # 放置白棋
                # if is_check==1:
                screen.blit(white,(piece_chessboard_x-16,piece_chessboard_y-16))

                
        #添加黑子
        for chess_jj in all_chess[::2]:
            d=40
            i_tmp,j_tmp =chess_jj
            # 判断标号是否有效
            if i_tmp in range(15) and j_tmp in range(15):
                i = i_tmp
                j = j_tmp
            
            if not i is None and not j is None:
                bw_in[i][j]=2                            
                piece_chessboard_x,piece_chessboard_y = i*d+15,j*d+15                
                    # 放置黑棋
                # if is_check==1:
                screen.blit(black,(piece_chessboard_x-16,piece_chessboard_y-16))
                                
        
        # 鼠标的坐标
        mouse_x,mouse_y = pygame.mouse.get_pos()
        if not is_end:
                # 棋子跟随鼠标移动
            if is_paly:
                if not is_people:
                    screen.blit(white,(mouse_x-16,mouse_y-16))
                
                if is_people:
                    if len(all_chess)%2==0:
                        screen.blit(black,(mouse_x-16,mouse_y-16))
                    if len(all_chess)%2==1:
                        screen.blit(white,(mouse_x-16,mouse_y-16))

                #pygame.mouse.set_visible(False)#隐藏鼠标
                
        if is_win()=='wht':
            is_white=True
            is_end=True
        elif is_win()=='blk':
            is_black=True
            is_end=True

        if is_end:
            if is_black:
                screen.blit(lose_text,(220,220))
            elif is_white:
                screen.blit(win_text,(220,220))
            screen.blit(play_text,(160,300))
            screen.blit(menu_text,(320,300))

        if is_menu:
            for chess in all_chess:
                x1,y1=chess
                bw_in[x1][y1]=0
            all_chess.clear()
            is_end=False
            is_paly=False
            is_AI=False
            #标志做出选择
            is_choose=False
            is_people=False
            is_white=False
            is_black=False
            is_menu=False

        
        if is_playagain:
            for chess in all_chess:
                x1,y1=chess
                bw_in[x1][y1]=0
            all_chess.clear()
            is_playagain=False
            is_end=False
            if not is_people:
                is_paly=False
                is_AI=True
            elif is_people:
                is_people=True               
        #刷新一下画面
        pygame.display.flip()
        pygame.display.update()

if __name__ == '__main__':
    main()
    # FPS=30
    # FPSclock=pygame.time.Clock()
    # FPSclock.tick(FPS) 
    #控制动画帧数
