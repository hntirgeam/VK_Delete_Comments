# coding=utf-8
import os
import vk_api

print('Для удаления комментариев и/или постов нужно авторизироваться, предварительно отключив 2fa (привязку телефона)')

access_token = input('Введите свой VK API access_token (берется по ссылке в описании, начинается с "vk"): ')

vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()

print('Выберите режим работы:', '\n', '1)Удаление комментариев', '\n', '2)Удаление постов',
      '\n', '3)Удаление и комментариев и постов')
mode = input()


def get_comments_paths():
    print('Введите путь к папке с комментариями без кавычек (папку можно просто перетащить в окно терминала)')
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


def get_comments_urls(path_to_comment):
    all_urls = []
    for open_and_find in path_to_comment:
        try:
            file_with_comments = open(open_and_find, 'r', encoding="ISO-8859-1")
            content = file_with_comments.read().splitlines()
            i = 0
            str1 = 'https://vk.com'
            while i < len(content):
                if content[i].find(str1) != - 1:
                    tmp = content[i]
                    tmp = tmp[tmp.find(str1):]
                    if tmp.find('>') == - 1:
                        all_urls.append(tmp)
                    else:
                        tmp = tmp[:(tmp.find('>') - 1)]
                        all_urls.append(tmp)
                i += 1
        finally:
            file_with_comments.close()
    return all_urls




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
        except Exception as e:
            comments_not_deleted += 1
            print(e)
            print("Не удалено", comments_not_deleted)


def delete_wall_posts():
    while True:
        posts = vk.wall.get()
        posts_index = 0
        while True:
            try:
                post_id = posts["items"][posts_index]["id"]
                vk.wall.delete(post_id=post_id)
                posts_index += 1
            except Exception as e:
                print('Что-то пошло не так: -', e)
                break


if mode == '1':
    delete_comments(get_comments_urls(get_comments_paths()))
elif mode == '2':
    delete_wall_posts()
elif mode == '3':
    delete_comments(get_comments_urls(get_comments_paths()))
    delete_wall_posts()
else:
    print('Нет такого параметра')
