#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import types


def get_session():

    url = 'http://challenge.shopcurbside.com/get-session'
    r = requests.get(url)

    # print(r.text)

    return r.text


def get_base_secrets(session, sid):
    """ ugly brute force attempt

    """

    url = 'http://challenge.shopcurbside.com/'
    startIDs = ['34ffe00db65f4576b5add43dda39ff99',
                'ebdf4d2f11514626a1b07d745d4a0fc6',
                '64bbc0003e824075ad59fb5cfaaac4cd']
    headers = {'Session': session}

    r = requests.get(url + startIDs[sid], headers=headers)
    j = json.loads(r.content.lower())

    # j['next']

    for line in j['next']:
        r2 = requests.get(url + line, headers=headers)
        j2 = json.loads(r2.content.lower())

        # if 'secret' in j2: print j2['secret']#print j2

        if 'error' in j2:
            headers = {'Session': get_session()}
            r2 = requests.get(url + line, headers=headers)
            j2 = json.loads(r2.content.lower())

        if 'secret' in j2:  # print j2
            print j2['secret']

        if type(j2['next']) is not types.ListType:

            r3 = requests.get(url + j2['next'], headers=headers)
            j3 = json.loads(r3.content.lower())

            if 'error' in j3:
                headers = {'Session': get_session()}
                r3 = requests.get(url + j2['next'], headers=headers)
                j3 = json.loads(r3.content.lower())

            if 'secret' in j3:  # print j2
                print j3['secret']
        else:

            for aline in j2['next']:

                # print aline
                # h = get_session()

                r3 = requests.get(url + str(aline), headers=headers)
                j3 = json.loads(r3.content.lower())

                if 'error' in j3:
                    headers = {'Session': get_session()}
                    r3 = requests.get(url + aline, headers=headers)
                    j3 = json.loads(r3.content.lower())

                if 'secret' in j3:  # print j2
                    print j3['secret']

                # print("j3 - "+str(j3))
                # print(len(j3['next']))

                if type(j3['next']) is not types.ListType:

                    # print("j3 has length one")
                    # h = get_session()

                    r4 = requests.get(url + j3['next'], headers=headers)
                    j4 = json.loads(r4.content.lower())

                    if 'error' in j4:
                        headers = {'Session': get_session()}
                        r4 = requests.get(url + j3['next'],
                                headers=headers)
                        j4 = json.loads(r4.content.lower())

                    print j4
                else:
                    for threeLine in j3['next']:

                        # h = get_session()

                        r4 = requests.get(url + str(threeLine),
                                headers=headers)
                        j4 = json.loads(r4.content)

                        if 'error' in j4:
                            headers = {'Session': get_session()}
                            r4 = requests.get(url + str(threeLine),
                                    headers=headers)
                            j4 = json.loads(r4.content.lower())

                        print j4


def get_display_data(aUrl, nexts, someHeaders):
    r = requests.get(aUrl + str(nexts), headers=someHeaders)
    j = json.loads(r.content.lower())
    if 'next' in j:  # print(j['next'])
        print ''
    if 'error' in j:
        if j['error'] == 'Page not found':
            print 'err'
        else:

            # return

            someHeaders['Session'] = get_session()
            print '''

 got a new session 
 ''' + str(someHeaders)

            # print(j)
            # if str(j['error']) == "Page not found":

            get_display_data(aUrl, nexts, someHeaders)
    elif j['depth'] == 4:

            # print("hi")
            # return

        print j
    else:

        # return

        try:
            get_display_data(aUrl, j['next'], someHeaders)
        except:
            print ''


def get_level_secrets(aUrl, nexts, someHeaders):

    # headers = {'Session':session}

    if type(nexts) is not types.ListType:

       # no loopy

        get_display_data(aUrl, nexts, someHeaders)
    else:

        # loopy

        for someLine in nexts:
            get_display_data(aUrl, nexts, someHeaders)


def start(rec):
    if rec:

        # Recursive attempt

        url = 'http://challenge.shopcurbside.com/'
        startIDs = ['34ffe00db65f4576b5add43dda39ff99',
                    'ebdf4d2f11514626a1b07d745d4a0fc6',
                    '64bbc0003e824075ad59fb5cfaaac4cd']
        headers = {'Session': get_session()}

        get_level_secrets(url, startIDs, headers)
    else:

        # brute force

        get_base_secrets(get_session(), 0)
        get_base_secrets(get_session(), 1)
        get_base_secrets(get_session(), 2)


if __name__ == '__main__':

    # pass in True to see recursive implementation output.

    start(False)

			
