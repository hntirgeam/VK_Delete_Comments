import vk_api
file = open('','')
content = file.read().splitlines()

vk_session = vk_api.VkApi('', '')
vk_session.auth()
vk = vk_session.get_api()
i = 0;
while i<len(content):
    str = content[i]
    owner_id = str[(str.find('wall') + 4):str.find('')]
    if str.find('&') != -1:
        comment_id = str[(str.find('reply=') + 6):str.find('&')]
    else:
        comment_id = str[(str.find('reply=') + 6):]
    vk.wall.deleteComments(owner_id = owner_id, comment_id = comment_id)

