import threading
from time import sleep
import PySimpleGUI as Sg
import requests
from loguru import logger

Sg.theme('DarkAmber')

layout = [[Sg.Text('Access token here:'), Sg.Input(key='access_token')],
          [Sg.ProgressBar(size=(20, 20), key='-PROG-', max_value=200, visible=False)],
          [Sg.Text('Completed', visible=False, key='-COMPL-')],
          [Sg.Button('Delete all groups', key='-OK-')]]

window = Sg.Window('Clear groups', layout)


class Main:
    def __init__(self, access_token: str):
        """
        Main functions for deleting videos in VK
        :param access_token: token from VK
        """
        self.access_token = access_token

    def get_groups(self) -> list:
        url = "https://api.vk.com/method/groups.get"
        params = {'access_token': self.access_token, 'v': '5.131'}

        resp = requests.get(url, params=params).json()
        if 'response' not in resp:
            logger.critical('Error getting groups')
            window['-COMPL-'].update('Error getting groups', visible=True)
            return []
        if resp['response']['count'] == 0:
            self.helper.logger.critical('No groups found')
            window['-COMPL-'].update('No groups found', visible=True)
            return []

        return resp['response']['items']

    def group_delete(self, group_id: str) -> bool:
        params = {'access_token': self.access_token, 'v': '5.131', 'group_id': group_id}
        resp = requests.get("https://api.vk.com/method/groups.leave", params=params).json()

        if resp['response'] == 1:
            logger.info(f'Group clear: {group_id}')
            return True
        else:
            logger.critical(f'Error: {resp}')


def event_ok(values_s):
    ll = Main(access_token=values_s['access_token'])
    groups = ll.get_groups()

    if not groups: return False

    window['-PROG-'].update(max=len(groups), current_count=0, visible=True)

    for i in range(len(groups)):
        ll.group_delete(groups[i])
        window['-PROG-'].update(i + 1)
        sleep(3)
    window['-COMPL-'].update(visible=True)


while True:
    event, values = window.read()

    if values['access_token'] == '':
        window['-COMPL-'].update('Access token is empty', visible=True)
        continue

    if event == '-OK-':
        thread = threading.Thread(target=event_ok, args=(values,)).start()

    if event == Sg.WIN_CLOSED:
        window.close()
        break
