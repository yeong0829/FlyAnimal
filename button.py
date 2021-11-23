from tkinter import *

root = Tk()  # 창 생성

root.title("test")   #창 제목
root.geometry("1900x1000")   #창의 가로*세로+x좌표+y좌표 - 좌표는 위치 고정/지정(컴퓨터 화면 기준) - 중간에 고정하기
root.resizable(0,0)   # 창 크기 조절 가능 True-가능/False-불가능


btn = Button(root)  # root라는 창에 버튼을 생성
btn.config(width=20, height=20)  # 버튼의 크기 설정 ( 버튼 크기 고정 )
btn.config(padx=20, pady=20)   #버튼의 크기 절정(글자 수에 따라 크기 달라짐/값은 글자와 버튼 테드리 사이의 거리값)
btn.config(text="버튼")

btn.pack()          # 만든 버튼을 창에 배치

root.mainloop()