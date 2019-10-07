import os
import vk_api
import webbrowser

print('Инструкцию можно (желательно) посмотреть в видео по ссылке: ', '\n')


def get_comments_paths():
    print('Введите путь к папке с комментариями (папку можно просто перетащить в окно терминала)', '\n')
    folder_path = input()

    user_files = [f.name for f in os.scandir(folder_path)]
    print('Загружены файлы:')
    paths_to_comments = []
    for file in user_files:
        if folder_path[-1] == '/' or folder_path[-1] == '\\':
            paths_to_comments.append(folder_path + file + '\n')
            print(folder_path + file)
        else:
            paths_to_comments.append(folder_path + '/' + file)
            print(folder_path + '/' + file + '\n')
    return paths_to_comments


path = get_comments_paths()


def get_comments_urls(path_to_comment):
    all_urls = []
    for open_and_find in path_to_comment:
        try:
            file_with_comments = open(open_and_find, 'r', encoding="ISO-8859-1")
            content = file_with_comments.read().splitlines()
            i = 0
            str1 = 'https://vk.com'
            while i < len(content):
                if content[i].find(str1) != -1:
                    tmp = content[i]
                    tmp = tmp[tmp.find(str1):]
                    tmp = tmp[:(tmp.find('>') - 1)]
                    all_urls.append(tmp)
                i += 1
        finally:
            file_with_comments.close()
    return all_urls


urls = get_comments_urls(path)


print('Для удаления постов/комментариев/лайков нужно войти в аккаунт или получить токен из приложения.', '\n',
      'Если вы готовы ввести логин и пароль, введите 1. Если нет, то введите 2.', '\n')
password_or_token = str(input())
if password_or_token == '1':
    print('Введите логин:')
    login = input()
    print('Введите пароль')
    password = input()
    vk_session = vk_api.VkApi(login, password)
    vk_session.auth()
    vk = vk_session.get_api()
elif password_or_token == '2':
    print('')  # сюда заебенить инструкцию для получения токена
    webbrowser.open('https://yandex.ru')
    token = input()
    vk_session = vk_api.VkApi(token)  # сюда токен засунуть блятб
    vk_session.auth()
    vk = vk_session.get_api()
elif password_or_token != '1' and password_or_token != '2':
    print('Введён неверный параметр')


def delete_comments(content):
    i = 0
    comments_deleted = 0
    comments_not_deleted = 0
    while i < len(content):
        str1 = content[i]
        i += 1
        owner_id = str1[(str1.find('wall') + 4):str1.find('_')]
        if str1.find('&') != -1:
            comment_id = str1[(str1.find('reply=') + 6):str1.find('&')]
        else:
            comment_id = str1[(str1.find('reply=') + 6):]
        print(owner_id, comment_id)
        try:
            vk.wall.deleteComment(owner_id=owner_id, comment_id=comment_id)
            comments_deleted += 1
            print("Удалено", comments_deleted)
            #  я в душее неебу, почему файл нужно открывать в except. Без этого не работает
        except:
            comments_not_deleted += 1
            print("Не удалено:", comments_not_deleted)


delete_comments(urls)
