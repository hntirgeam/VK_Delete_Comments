import os
import vk_api



try:
    file1 = open("/home/fujig/Desktop/AllComments.txt", 'r')
    file2 = open(r"/home/fujig/Desktop/notDeleted2.txt", 'a')
    file3 = open("/home/fujig/Desktop/loh.txt", 'r')
    content = file1.read().splitlines()
    logpass = file3.read().splitlines()

    vk_session = vk_api.VkApi(logpass[0], logpass[1])
    #  сюда токен засунуть блятб
    vk_session.auth()
    vk = vk_session.get_api()
    i = 0
    k = 0
    j = 0
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
            j += 1
            print("Удолило", j)
            #  я в душее неебу, почему файл нужно открывать в except. Без этого не работает
        except:
            file2 = open(r"/home/fujig/Desktop/notDeleted.txt", 'a')
            k += 1
            print("Не удолило", k)
            file2.write(str1)
            file2.write('\n')

finally:
    file1.close()
    file2.close()

#  получаем на вход папку
#  код берет все файлы из папки и запускает
