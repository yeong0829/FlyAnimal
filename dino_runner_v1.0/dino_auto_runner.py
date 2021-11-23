import pyautogui
import time
import numpy as np
import matplotlib.pyplot as plt
import mss

################## Settings
range_LT = (250, 360)
range_RB = (780, 410)
range_img = (range_LT[0], range_LT[1], range_RB[0], range_RB[1])
mon = {"top": range_img[1], "left": range_img[0], "width": range_img[2]-range_img[0], "height": range_img[3]-range_img[1]}
sct = mss.mss()

window_size = 30
sub_max = 50*100*255
patch_withe = np.ones([50,50])*255

frame_diff = 100
dec_thr = 120
dec_jump_thr = 40
pyautogui.PAUSE = 0
###############################


################# Variables
cnt = 1 # Frame count

r1_on = 0
r2_on = 0

r1_ini = 1
r2_ini = 1

prev_dec_f = 0
prev_cnt = 0
short_jump = 0
jump_cnt = 0
whole_jump = 0


cnt_decs = 0 # number of [trees or birds]
cnt_dec_stack = np.zeros(5) # Frames of [trees or birds]
space_stack = np.zeros(5)
cnt_space = 0
#################################

print('trex algorithm start!')

while True:
    start = time.time()
    img = np.asarray(sct.grab(mon))
    gimg = img[:,:,0]
    np_img = np.array(gimg)
        
    img_region1 = patch_withe - np_img[:, 280:330]
    img_region2 = patch_withe - np_img[:, 480:530]
    
    region1_sum = img_region1.sum()/255
    region2_sum = img_region2.sum()/255
    
    
    ################# Region 2 detection ##################
    # 감지된 객체들의 시작 위치를 순서대로 저장
    if region2_sum > dec_thr: # Region 2 장애물 감지
        r2_on = 1 # 장애물 감지 toggle on
        
       
        
        if r2_ini == 1: # 객체 시작 타이밍
            
            dec_diff = cnt - prev_dec_f
            if dec_diff < dec_jump_thr:
                short_jump = 1
            
            r2_ini = 0
            cnt_dec_stack[cnt_decs] = cnt # 객체가 감지된 순간 저장
            cnt_decs = cnt_decs + 1 # 감지된 객체 stack 에 저장
            prev_dec_f = cnt # 이전 객체 감지 시간
        
 
    if r2_on == 1: # no more detecting
        if region2_sum < dec_thr:
            
            r2_ini = 1
            r2_on = 0
    
    ################# Region 1 detection ##################
    if region1_sum > dec_thr: # Region 1 장애물 감지   
        r1_on = 1 
        
        if r1_ini == 1: # start
            r1_ini = 0
            
            r2_cnt = cnt_dec_stack[0]
            if r2_cnt == 0:
                print( 'Waiting...')
            else:
                # 장애물 감지가 된것들에 대한 처리
                cnt_decs = cnt_decs - 1
                cnt_dec_stack[0:3] = cnt_dec_stack[1:4]
                cnt_dec_stack[4] = 0
                
                # 객체 속도 계산
                frame_diff = cnt - r2_cnt
                
                # 뛰는 시간 저장
                if frame_diff > 20:
                    space_stack[cnt_space] = cnt + frame_diff + 3
                elif frame_diff == 20:
                    space_stack[cnt_space] = cnt + frame_diff
                elif frame_diff == 19:
                    space_stack[cnt_space] = cnt + frame_diff
                elif frame_diff == 18:
                    space_stack[cnt_space] = cnt + frame_diff
                elif frame_diff == 17:
                    space_stack[cnt_space] = cnt + frame_diff
                elif frame_diff == 16:
                    space_stack[cnt_space] = cnt + frame_diff - 1
                else:
                    space_stack[cnt_space] = cnt + frame_diff - 1
                    
                cnt_space = cnt_space + 1
                

    if r1_on == 1: # no more detecting
        if region1_sum < dec_thr:
            r1_ini = 1
            r1_on = 0
            

    ################# 점프 처리 ##################   
    if space_stack[0] == cnt: # jump 명령 스택
        
        whole_jump = whole_jump + 1
        pyautogui.keyDown('up')
        jump_cnt = space_stack[0]
        print(' %d th jump! [speed' % whole_jump , 40-frame_diff, 'distance', dec_diff, ']')
        
        prev_cnt = cnt
        space_stack[0:3] = space_stack[1:4]
        space_stack[4] = 0
        cnt_space = cnt_space - 1 
    
    # 짧은 점프 조건
    if cnt - jump_cnt > 2 and cnt-jump_cnt < 5:
        if short_jump or frame_diff <  9 : # 객체 사이 거리가 짧거나 속도가 빠를경우
 
            pyautogui.keyUp('up') # duration 만큼은 키를떼어주도록,
            
            
            if cnt - jump_cnt == 4:
                short_jump = 0
                print('  short jump!')    
    
    cnt = cnt + 1 # frame count