import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from config import comunity_token, access_token
from core import VKTools
from object.User import User


class BotInterface():

    def __init__(self, comunity_token, acces_token):

        self.interface = vk_api.VkApi(token=comunity_token)
        self.api = VKTools(acces_token)
        self.user = User

    def message_send(self, user_id, message, attachment=None):
        get_random_id()
        self.interface.method('messages.send',
                              {'user_id': user_id,
                               'message': message,
                               'attachment': attachment,
                               'random_id': get_random_id()
                               }
                              )

    def add_user_info(self):
        flag = False
        if self.user.sex is None:
            self.message_send(self.user.id, 'Не хватает информации о Пол, введите команду Пол=', None)
            flag = True
        if self.user.city is None:
            self.message_send(self.user.id, 'Не хватает информации о Город, введите команду Город=', None)
            flag = True
        if self.user.bdate is None:
            self.message_send(self.user.id, 'Не хватает информации о Дата рождения, введите команду Дата рождения=',
                              None)
            flag = True
        if self.user.relation is None:
            self.message_send(self.user.id, 'Не хватает информации о семейном положении, введите команду Семейное положене=',
                              None)
            flag = True
        return flag
    def event_handler(self):
        longpoll = VkLongPoll(self.interface)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                command = event.text.lower()
                if command == 'привет':
                    self.user = self.api.get_profile_info(event.user_id)
                    self.message_send(event.user_id, f'здравствуй {self.user.name}')
                elif command == 'поиск':
                    if not self.add_user_info():
                        offset = 0
                        count_seach_user = 0
                        while count_seach_user <= 10 :
                            users = self.api.serch_users(self.user, offset)
                            for user_one in users:
                                if self.api.add_seach_user(user_one, self.user.id):
                                    count_seach_user = count_seach_user + 1
                                    photos_user = self.api.get_photos(user_one.id)
                                    attachment = ''
                                    for num, photo in enumerate(photos_user):
                                        attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
                                        if num == 2:
                                            break
                                    self.message_send(event.user_id,
                                                      f'Встречайте {user_one.name}',
                                                      attachment=attachment
                                                      )
                            offset = offset + 10
                elif command == 'пока':
                    self.message_send(event.user_id, 'пока')
                    self.api.db.close();
                elif command.find('пол=', 0) != -1:
                    parts = command.partition('пол=')
                    self.user.sex = parts[2]
                elif command.find('город=', 0) != -1:
                    parts = command.partition('город=')
                    self.user.city = parts[2]
                elif command.find('дата рождения=', 0) != -1:
                    parts = command.partition('дата рождения=')
                    self.user.bdate = parts[2]
                elif command.find('семейное положене=', 0) != -1:
                    parts = command.partition('семейное положене=')
                    self.user.relation = parts[2]

                else:
                    self.message_send(event.user_id, 'команда не опознана')


if __name__ == '__main__':
    bot = BotInterface(comunity_token, access_token)
    bot.event_handler()