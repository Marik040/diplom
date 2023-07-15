from datetime import datetime

import vk_api

from db import Db
from config import access_token

from object.User import User


class VKTools():
    def __init__(self, acces_token):
        self.api = vk_api.VkApi(token=acces_token)
        self.db = Db()


    def get_profile_info(self, user_id):

        info, = self.api.method('users.get',
                                {'user_id': user_id,
                                 'fields': 'city,bdate,sex,relation'
                                 }
                                )
        user: User = User(
            info['id'],
            info['first_name'] + ' ' + info['last_name'],
            info['sex'] if 'sex' in info else None,
            info['city']['id'] if 'city' in info else None,
            info['bdate'] if 'bdate' in info else None,
            info['relation'] if 'relation' in info else None
        )
        self.db.add_new_user(user)
        return user

    def serch_users(self, user: User, offset:int):
        sex = 1 if user.sex == 2 else 2
        city = user.city
        age = user.get_age()
        users = self.api.method('users.search',
                                {'count': 10,
                                 'offset': offset,
                                 'age_from': age['age_from'],
                                 'age_to': age['age_to'],
                                 'sex': sex,
                                 'city': city,
                                 'status': 6,
                                 'is_closed': False
                                 }
                                )
        try:
            users = users['items']
        except KeyError:
            return []

        result_users = []

        for user in users:
            if user['is_closed'] == False:
                seachUser = User(
                user['id'],
                user['first_name'] + ' ' + user['last_name'],
                '','','', '')
                result_users.append(seachUser)

        return result_users


    def get_photos(self, user_id):
        photos = self.api.method('photos.get',
                                 {'user_id': user_id,
                                  'album_id': 'profile',
                                  'extended': 1
                                  }
                                 )
        try:
            photos = photos['items']
        except KeyError:
            return []

        res = []

        for photo in photos:
            res.append({'owner_id': photo['owner_id'],
                        'id': photo['id'],
                        'likes': photo['likes']['count'],
                        'comments': photo['comments']['count'],
                        }
                       )

        res.sort(key=lambda x: x['likes'] + x['comments'] * 10, reverse=True)

        return res

    def add_seach_user(self, user:User, id_user:int):
       return self.db.add_seach_user(user, id_user)

if __name__ == '__main__':
    bot = VKTools(access_token)
    params = bot.get_profile_info(789657038)
    users = bot.serch_users(params)
