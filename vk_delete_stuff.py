#!/usr/bin/env python3
# coding=utf-8

from os import path, remove, scandir
import vk_api


def get_comments_paths():
    print('Введите путь к папке с комментариями (папку можно просто перетащить в окно терминала)')
    folder_path = input()

    user_files = [f.name for f in scandir(folder_path)]
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


def create_html_log_template():
    log_file_descriptor = open(log_file_name, "w+")
    log_file_descriptor.write('''
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">
<HTML>
    <HEAD>
        <TITLE>VK deletion log</TITLE>
    </HEAD>
    <BODY>
    ''')
    log_file_descriptor.close()


def delete_comments(content):
    i = 0
    comments_deleted = 0
    comments_not_deleted = 0

    create_html_log_template()

    while i < len(content):
        str1 = content[i]
        i += 1
        owner_id = str1[(str1.find('wall') + 4):str1.find('_')]
        if str1.find('&') != -1:
            comment_id = str1[(str1.find('reply=') + 6):str1.find('&')]
        else:
            comment_id = str1[(str1.find('reply=') + 6):]
        info_about_comment = f"{owner_id}{comment_id}"
        print(info_about_comment)
        if info_about_comment.count("://"):
            log_file_descriptor = open(log_file_name, "a")
            log_file_descriptor.write("<a href=\"https://" + info_about_comment[3:] + "\">link</a></br>" + "\n")
            log_file_descriptor.close()
        try:
            vk.wall.deleteComment(owner_id=owner_id, comment_id=comment_id)
            comments_deleted += 1
            print("Удалено", comments_deleted)
        except:
            comments_not_deleted += 1
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
            except:
                print('Что-то пошло не так')
                break


def answer_checker():
    user_ans = input("Вы согласны? (y/Y): ")
    if user_ans.lower() == "y":
        pass
    else:
        print("Отмена")
        exit(0)


def vk_json_remover():
    if path.exists("vk_config.v2.json"):
        try:
            remove("vk_config.v2.json")
        except:
            print("Ошибка при удалении файла vk_config.v2.json")


if __name__ == '__main__':
    log_file_name = 'vk_del.html'
    print('Выберите режим работы:', '\n', '1)Удаление комментариев', '\n', '2)Удаление постов',
          '\n', '3)Удаление комментариев и постов')
    
    mode = input("Выбраный режим работы (1,2,3): ")
    if mode not in ("1", "2", "3"):
        print('Нет такого параметра')
        exit(1)

    print(
        'Для удаления комментариев и/или постов нужно авторизироваться, предварительно отключив 2fa (привязку телефона)')
    print('Введите логин/номер телефона:')
    user_login = input()
    print('Введите пароль:')
    user_password = input()
    try:
        vk_session = vk_api.VkApi(user_login, user_password)
        vk_session.auth()
        vk = vk_session.get_api()
    except:
        print("Ошибка авторизации")
        exit(1)

    if mode == '1':
        print("Сейчас все комментарии будут удалены")
        print("Ссылки на комментарии, которые невозможно удалить будут помещены в vk_del.html")
        answer_checker()
        delete_comments(get_comments_urls(get_comments_paths()))
        vk_json_remover()
    elif mode == '2':
        print("Сейчас все посты будут удалены")
        answer_checker()
        delete_wall_posts()
        vk_json_remover()
    elif mode == '3':
        print("Сейчас все комментарии и посты будут удалены")
        answer_checker()
        delete_comments(get_comments_urls(get_comments_paths()))
        delete_wall_posts()
        vk_json_remover()
