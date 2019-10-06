import os
import vk_api

path_to_comments = input

for root, dirs, files in os.walk(path_to_comments, topdown=False):
    for name in files:
        print(os.path.join(root, name))
    for name in dirs:
        print(os.path.join(root, name))
