from tkinter import *
import tkinter
import image
#import pygame
#from PIL import Image, ImageSequence



t = Tk()  # 창 생성

t.title("test")   #창 제목
t.geometry("1000x500")   #창의 가로*세로+x좌표+y좌표 - 좌표는 위치 고정/지정(컴퓨터 화면 기준) - 중간에 고정하기
t.resizable(0,0)   # 창 크기 조절 가능 True-가능/False-불가능


# width = 1000
# height = 500
#img = PhotoImage(file = "C:\\Users\\주서영\\Desktop\\프로젝트\\Fly Animal_PythonProject\\images\\t3.png")   # 배경이미지 넣기,
#result[0].save('animal1.gif', save_all=True, optimize=True, append_images=result[1:], loop=0)
# img = img.resize((width,height), Image.ANTIALIAS)
# photoImg =  Image.PhotoImage(img)
# b = Button(master,image=photoImg, command=callback, width=50)
# b.pack()

#mg_label = Label(image=img)
#img_label.place(x=50, y=400)   # 이미지 위치 조정

#img_label.place()

# img = PhotoImage(file = "C:\\Users\\주서영\\Pictures\\bg.png")
# img_size = resize((1000, 500))


# test1 = PhotoImage(file="C:\\Users\\주서영\\Desktop\\프로젝트\\Fly Animal_PythonProject\\images\\animal1.gif")
# test1_label = Label(t, image=test1)
# test1_label.pack()

#t['bg'] = '#49A'   # 배경색


# label=Label(t, text="안녕하세요.")  # 글씨 넣기
# label.pack()   # 글씨 위치 조정?

#gif 넣기
# g = tkinter.PhotoImage(file="C:\\Users\\주서영\\Desktop\\프로젝트\\Fly Animal_PythonProject\\images\\t3.png")
# label = tkinter.Label(image=g)
# label.pack()

t.mainloop()   # 창 종료 - *항상 마지막에 넣기*