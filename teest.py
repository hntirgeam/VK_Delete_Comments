import vk_api
import os
import wx


def remove_wall_posts():
    vk_session = vk_api.VkApi('', '')
    vk_session.auth()

    vk = vk_session.get_api()
    j = 0
    while True:
        posts = vk.wall.get()
        i = 0
        while True:
            try:
                post_id = posts["items"][i]["id"]
                vk.wall.delete(post_id=post_id)
                i += 1
            except:
                break


def create_all_urls():
    try:
        file2 = open(r"C:\Users\kmacr\Desktop\AllComments.txt", 'w')
        k = 1
        while k <= 62:
            file_name = r"C:\Users\kmacr\Desktop\comments\comments" + str(k) + ".html"
            file1 = open(file_name, "r")
            content = file1.read().splitlines()
            i = 0
            str1 = 'https://vk.com'
            while i < len(content):
                if content[i].find(str1) != -1:
                    tmp = content[i]
                    tmp = tmp[tmp.find(str1):]
                    tmp = tmp[:(tmp.find('>') - 1)]
                    file2.write(tmp)
                    file2.write('\n')
                i += 1
            k += 1
    finally:
        file1.close()
        file2.close()


def remove_all_comments():
    try:
        file1 = open("/home/fujig/Desktop/AllComments.txt", 'r')
        file2 = open("/home/fujig/Desktop/notDeleted2.txt", 'a')
        file3 = open("/home/fujig/Desktop/loh.txt", 'r')
        content = file1.read().splitlines()
        logpass = file3.read().splitlines()

        vk_session = vk_api.VkApi(logpass[0], logpass[1])
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
                #  я в душее неебу, почему файл нужно открывать в except. Без этого неработает
            except:
                file2 = open(r"/home/fujig/Desktop/notDeleted.txt", 'a')
                k += 1
                print("Не удолило", k)
                file2.write(str1)
                file2.write('\n')

    finally:
        file1.close()
        file2.close()
