import os
from tkinter import *
#from PIL import Image, ImageSequence
#import natsort
#import imageio

# class MyFrame(Frame):  # 클래스 정의
#     def __init__(self, master):
#         img = PhotoImage(file="C:\\Users\\주서영\\Desktop\\프로젝트\\Fly Animal_PythonProject\\images\\animal1.gif")  # 이미지 읽고
#         lbl = Label(image=img)  # 이미지 넣어
#         lbl.image = img  # 레퍼런스 추가
#         lbl.pack()
#
#
# def main():  # 메인함수로 정의
#     root = Tk()
#     root.title('이미지 보기')
#     root.geometry('1000x500')
#     root.resizable(0, 0)
#     myframe = MyFrame(root)  # 클래스 사용
#     root.mainloop()
#
#
# if __name__ == '__main__':  # 메인함수 호출
#     main()


root = Tk()
root.title('test')
root.geometry('1000x500')
root.resizable(0, 0)

directory = r"C:\Users\주서영\Desktop\프로젝트\Fly Animal_PythonProject\images\a1"
file_type = r'.png'
save_gif_name = r'a1_gif'
speed_sec = {'duration': 1.}

image = []
file_list = natsort.natsorted(os.listdir(directory))
for file in file_list:
    if file.endswith(file_type):
        file_path = os.path.join(directory, file)
        image.append(imageio.imread(file_path))

imageio.mimsave('{0}/{1}.gif'.format(directory, save_gif_name), image, **speed_sec)
root.mainloop()

