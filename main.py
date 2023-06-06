import requests
import os
import yadisk
import json
import time


def get_user_data(token):

    id = input('введите id контакта' )
    url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': f'{id}',
              'album_id':'profile',
              'access_token': token,
              'count': 5, 'v': '5.131',
              'extended': '1' }

    response = requests.get(url, params=params)
    data = response.json()
    print('Список файлов получен')
    screen = [] # список для формирования json файла

    if not os.path.exists('images_vk'):
        os.mkdir('images_vk')
        print('Папка images_vk на компьютере создана')
    else:
        print('Папка images_vk на компьютере уже существует, файлы будут записаны туда')


    for item, item_1 in data.items():
        x = item_1['items']
        for photo in x:
            likes = photo['likes']
            names = likes['count'] #количество лайков

            photos = photo['sizes']
            sizes = photos[-1] # фото с большим разрешением
            photo_to_upload = sizes['url'] # ссылка для  фото
            sizes_1 = sizes['type']  # название размера фото

            date = photo['date'] # дата фотографии
            local_time = time.ctime(date)
            local_time = local_time.replace(':', '.') # дата фото форматированная

            names_1 = f"{names},{local_time}" # получили имя для файла
            #print(names_1)
            spiski = dict(zip([names_1], [photo_to_upload]))

            api = requests.get(photo_to_upload)

            for names_1, photo_to_upload in spiski.items(): # скачиваем фото в папку
                with open('images_vk/%s'% f"{names_1}.jpg", 'wb') as file:
                    img = requests.get(photo_to_upload)
                    file.write(img.content)
                    print(f'фото {names_1} скачано в папку')




            # формируем json файл и добавляем в него данные
            outputdata = {'file_name': names_1, 'size': sizes_1}
            screen.append(outputdata)

    files = os.listdir(path="images_vk")   # получаем количество файлов в папке
    print(f'Скачано в папку {len(files)} файлов')

    with open("outputdata.json", "w") as write_file:
        json.dump(screen, write_file)
    print(f'json файл с информацией о фото сформирован')

    files = os.listdir(path="images_vk")
    print(f'Скачано в папку {len(files)} файлов')

    return data

def yandex(TOKEN):
    y = yadisk.YaDisk(token=TOKEN)

    def run(path):
        def download():#функция для загрузки фото
            for address, dirs, files in os.walk(path):
                for images_vk in dirs:
                    path_2 = os.path.abspath('images_vk')
                    y.mkdir(f'path_2')
                    print(f'Папка {images_vk} создана')
                count = 0
                for file in files:

                    path_3 = os.path.abspath('course paper')
                    print(f'Файл {file} загружен')
                    y.upload(f'{address}/{file}', f'{date}/{file}')
                    count += 1
                print(f'Загружено файлов на яндекс диск {count}')



        if y.exists('vk_images'): # проверяем наличие папки на яндекс диске
            print(f'Папка {date} существует, пожалуйста, сохраните файлы этой папки в другом месте, папка будет перезаписана')
            x = input('Данные сохранили?')
            if x == 'да':
                y.remove('vk_images', permanently = True)
                print('Папка vk_images перезаписана')
                time.sleep(4)
                y.mkdir(f'{date}')
                download()

            else:
                print('сначала сохраните данные из действующей папки')


        else:
            y.mkdir(f'{date}')
            print(f'Папка {date} на яндекс диске создана')
            download()


    if __name__ == '__main__':
        date = f'vk_images'
        path = os.path.abspath('images_vk')
        run(path)



if __name__ == '__main__':

    TOKEN = input('введите токен яндекс')

    with open('token.txt', 'r') as token_file: #открывает файл в котором расположен токен VK, добавлен в гитигнор
        token = token_file.readline()
        # print(token)
    data = get_user_data(token)

    yandex(TOKEN)



