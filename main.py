# Программа для чтения видео
# и извлечь кадры

import cv2
import os
from PIL import Image


# Функция для извлечения кадров
def FrameCapture(path):
    # Путь к видеофайлу
    vidObj = cv2.VideoCapture(path)
    # Используется как переменная счетчика
    count = 0
    # проверяет, были ли извлечены кадры
    success = 1
    while success:
        # vidObj объект вызывает чтение
        # функция извлечения кадров
        success, image = vidObj.read()
        # Сохраняет кадры с количеством кадров
        try:
            cv2.imwrite(f"frame{count}.jpg", image)
        except BaseException:
            pass
        count += 1
    return count


def crop_bar(name):
    img = Image.open(name)
    crop = (0, 0, 592, 59)
    img1 = img.crop(crop)
    img1.save('status_bar.jpg')


def reform(n):
    for i in range(int(n) - 1):
        bar = Image.open('status_bar.jpg')
        img = Image.open(f'frame{i}.jpg')
        pas = Image.new(color=0, size=(592, 1280), mode='RGB')
        pas.paste(img, (0, 0, 592, 1280))
        pas.save('reform_frame.jpg')
        pas.paste(bar, (0, 0, 592, 59))
        pas.save(f'reform_frame{i}.jpg')
        os.remove(f'frame{i}.jpg')


def create_video(n):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter('Iphone_video.mp4', fourcc, 31, (592, 1280))
    for i in range(int(n) - 1):
        try:
            img = cv2.imread(f'reform_frame{i}.jpg') # читаем файл изображения
            os.remove(f'reform_frame{i}.jpg')
        except:
            pass
        video.write(img)  # дописываем кадр в видеофайл
    video.release()  # отключаем видеозапись
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Вызов функции для разделания видео на кадры
    count = FrameCapture("IMG_3967.mp4")
    # вызываем операцию для вырезания верхней части картинки
    # и сохроняем её
    name_scrinshot = 'iphone_status.jpg'
    crop_bar(name_scrinshot)
    # Теперь вызываем функцию для пересоздания кадров
    reform(count)
    create_video(count)
