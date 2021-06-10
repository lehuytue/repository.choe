# Module: main
# Author: Choehn
# Created on: 7 - 6 - 2021
"""
Example video plugin that is compatible with Kodi 19.x "Matrix" and above
"""
# import CommonFunctions as common
import logging
import sys
from urllib.parse import urlencode, parse_qsl
import xbmcgui
import xbmcplugin
import xbmcaddon
import fshareapi
import thuvienhd

if hasattr(sys.modules["__main__"], "xbmc"):
    xbmc = sys.modules["__main__"].xbmc
else:
    import xbmc

# Get the plugin url in plugin:// notation.
_URL = sys.argv[0]
# Get the plugin handle as an integer number.
_HANDLE = int(sys.argv[1])

__settings__ = xbmcaddon.Addon(id='plugin.video.fvideo')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
searchnum = __settings__.getSetting('search_num')
sharinglist = __settings__.getSetting('sharinglist')
fuseragent = __settings__.getSetting('fuseragent')

fuser = fshareapi.login_api('FVideo-5ENIJN', __settings__.getSetting('username'), __settings__.getSetting('password'),
                            __settings__.getSetting('fappkey'))
# print('download_api main : ', fuser['token'])

# Danh sach phim
VIDEOS = {'Hanh dong': [{'name': 'Phim 1',
                         'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/crab-screenshot.jpg',
                         'video': 'https://download028.fshare.vn/dl/y-7TGXkhiJM945obCcRt3i5jU8Rgl0PHNoEEyoMBVV-WSeXCMHcZuSYQZeamWzmbK5k8HuotwqPJWvAB/%28Hard%20Sub%20Vi%E1%BB%87t%29%20-%20LONDON%20HAS%20FALLEN.mp4',
                         'genre': 'Animals'},
                        {'name': 'Phim 2',
                         'thumb': 'http://www.vidsplay.com/wp-content/uploads/2017/04/alligator-screenshot.jpg',
                         'video': 'https://download028.fshare.vn/dl/y-7TGXkhiJM945obCcRt3i5jU8Rgl0PHNoEEyoMBVV-WSeXCMHcZuSYQZeamWzmbK5k8HuotwqPJWvAB/%28Hard%20Sub%20Vi%E1%BB%87t%29%20-%20LONDON%20HAS%20FALLEN.mp4',
                         'genre': 'Animals'}
                        ]}


# This function raises a keyboard for user input
def getUserInput(title=u"Input", default=u"", hidden=False):
    # log("", 5)
    result = None

    # Fix for when this functions is called with default=None
    if not default:
        default = u""

    keyboard = xbmc.Keyboard(default, title)
    keyboard.setHiddenInput(hidden)
    keyboard.doModal()

    if keyboard.isConfirmed():
        result = keyboard.getText()

    # log(repr(result), 5)
    return result


def addDir(lable, title, genre, thumb, fanart, icon, url):
    # Create a list item with a text label and a thumbnail image.
    list_item = xbmcgui.ListItem(label=lable)
    list_item.setArt({'thumb': thumb,
                      'icon': icon,
                      'fanart': fanart})
    list_item.setInfo('video', {'title': title,
                                'genre': genre,
                                'mediatype': 'video'})
    is_folder = True
    # Add our item to the Kodi virtual folder listing.
    xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # 1: Info; 2: Warning; 3: Error
    xbmc.log(url, 1)


def addLink(lable, title, genre, thumb, fanart, icon, url):
    # Create a list item with a text label and a thumbnail image.
    list_item = xbmcgui.ListItem(label=lable)
    # Set additional info for the list item.
    # 'mediatype' is needed for skin to display info for this ListItem correctly.
    list_item.setInfo('video', {'title': title,
                                'genre': genre,
                                'mediatype': 'video'})
    # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
    # Here we use the same image for all items for simplicity's sake.
    # In a real-life plugin you need to set each image accordingly.
    list_item.setArt({'thumb': thumb
                         , 'icon': icon
                         , 'fanart': fanart}
                     )
    # Set 'IsPlayable' property to 'true'.
    # This is mandatory for playable items!
    list_item.setProperty('IsPlayable', 'true')
    is_folder = False
    # Add our item to the Kodi virtual folder listing.
    xbmcplugin.addDirectoryItem(_HANDLE, url, list_item, is_folder)
    # 1: Info; 2: Warning; 3: Error
    xbmc.log(url, 1)


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(_URL, urlencode(kwargs))


def sharingTogether():
    list = sharinglist.split(",")
    for item in list:
        name = item.strip()
        url = get_url(action='getFromfile', filename=name)
        # addDir(lable, title, genre, thumb, fanart, icon, url)
        addDir(name, name, '', '', '', '', url)


def getFromfile(name):
    try:
        # 1: Info; 2: Warning; 3: Error
        xbmc.log('FVideo resourcefilepath: ' + xbmc.translatePath(__settings__.getAddonInfo('profile')) + name, 1)
        file = open(xbmc.translatePath(__settings__.getAddonInfo('profile')) + name, 'r')
        # file = open(url,'r')
        for line in file.readlines():
            try:
                list = line.split("##")
                href = list[1].strip()
                name = list[0].encode("utf-8")
                if href.find('fshare.vn/file') > 0:
                    addLink(name, get_url(action='play', video=href))
                elif href.find('fshare.vn/folder') > 0:
                    # addDir(lable, title, genre, thumb, fanart, icon, url)
                    addDir(name, name, '', '', '', '', get_url(action='viewFshareFolde', video=href))
            except:
                pass
        file.close()
    except:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('FVideo - message', 'Data not found')
        pass


def getFshareDowloadUrl(url):
    download_info = {
        'data_url': url,
        'password': 'lht2468',
        'token': fuser['token'],
        'user_agent': fuseragent,
        'cookie': fuser['session_id']
    }
    ret = fshareapi.download_api(download_info['data_url'], download_info['password'], download_info['token'],
                                 download_info['user_agent'], download_info['cookie'])
    print('ret: ', ret)
    return ret['location']


def Idfilm():
    sinput = getUserInput('Film ID', '1H2KCTR2SHS7E57')
    if sinput is not None:
        href = 'https://www.fshare.vn/file/' + sinput
        url = get_url(action='play', video=href)
        # addLink(lable, title, genre, thumb, fanart, icon, url)
        addLink(href, href, '', '', '', '', get_url(action='play', video=href))


def get_categories():
    """
    Get the list of video categories.

    Here you can insert some parsing code that retrieves
    the list of video categories (e.g. 'Movies', 'TV-shows', 'Documentaries' etc.)
    from some site or API.

    .. note:: Consider using `generator functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :return: The list of video categories
    :rtype: types.GeneratorType
    """
    return VIDEOS.keys()


def get_videos(category):
    """
    Get the list of videofiles/streams.

    Here you can insert some parsing code that retrieves
    the list of video streams in the given category from some site or API.

    .. note:: Consider using `generators functions <https://wiki.python.org/moin/Generators>`_
        instead of returning lists.

    :param category: Category name
    :type category: str
    :return: the list of videos in the category
    :rtype: list
    """
    return VIDEOS[category]


def list_categories():
    # Get video categories
    categories = get_categories()
    # Iterate through categories
    for category in categories:
        # Example: plugin://plugin.video.example/?action=listing&category=Animals
        url = get_url(action='listing', category=category)
        # addDir(lable, title, genre, thumb, fanart, icon, url)
        addDir(category, category, '', '', '', '', url)


def list_videos(category):
    videos = get_videos(category)
    # Iterate through videos.
    for video in videos:
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/wp-content/uploads/2017/04/crab.mp4
        url = get_url(action='play', video=video['video'])
        # addLink(lable, title, genre, thumb, fanart, icon, url)
        addLink(video['name'], video['name'], '', '', '', '', url)


def thuvienhd_getall(url):
    # Get video categories
    items = thuvienhd.getAll(url)
    # Iterate through categories
    for item in items:
        url = get_url(action='thuvienhdgetdetail', href=item['href'])
        # addDir(lable, title, genre, thumb, fanart, icon, url)
        addDir(item['name'], item['name'], '', item['src'], item['src'], '', url)


def thuvienhdsearch():
    sinput = getUserInput(u'Từ khóa', '')
    if sinput is not None:
        href = 'https://thuvienhd.com/?s=' + sinput.replace(' ', '+')
        # Get video categories
        items = thuvienhd.search(href)
        # Iterate through categories
        for item in items:
            url = get_url(action='thuvienhdgetdetail', href=item['href'])
            # addDir(lable, title, genre, thumb, fanart, icon, url)
            addDir(item['name'], item['name'], '', item['src'], item['src'], '', url)


def thuvienhdgetdetail(url):
    # Get video categories
    items = thuvienhd.getDetail(url)
    # Iterate through categories
    for item in items:
        url = get_url(action='play', video=item['href'])
        # addDir(lable, title, genre, thumb, fanart, icon, url)
        addLink(item['name'], item['name'], '', item['src'], item['src'], '', url)


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=getFshareDowloadUrl(path))
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_HANDLE, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        elif params['action'] == 'Idfilm':
            Idfilm()
        elif params['action'] == 'sharingTogether':
            sharingTogether()
        elif params['action'] == 'getFromfile':
            getFromfile(params['filename'])
        elif params['action'] == 'thuvienhd_getall':
            thuvienhd_getall(params['url'])
        elif params['action'] == 'thuvienhdsearch':
            thuvienhdsearch()
        elif params['action'] == 'thuvienhdgetdetail':
            thuvienhdgetdetail(params['href'])
        else:
            raise ValueError('Invalid paramstring: {}!'.format(paramstring))
    else:
        # addDir(lable, title, genre, thumb, fanart, icon, url)
        addDir('HOT', '', '', '', '', '', get_url(action='thuvienhd_getall', url='https://thuvienhd.com/trending'))
        addDir(u'Thuyết minh', '', '', '', '', '',
               get_url(action='thuvienhd_getall', url='https://thuvienhd.com/genre/thuyet-minh-tieng-viet'))
        addDir(u'Lồng tiếng', '', '', '', '', '',
               get_url(action='thuvienhd_getall', url='https://thuvienhd.com/genre/long-tieng-tieng-viet'))
        addDir(u'TVB', '', '', '', '', '', get_url(action='thuvienhd_getall', url='https://thuvienhd.com/genre/tvb'))
        addDir(u'Mới nhất', '', '', '', '', '', get_url(action='thuvienhd_getall', url='https://thuvienhd.com/recent'))
        addDir('Xem theo ID (Vi du: KIMSN1RFJ7)', '', '', '', '', '', get_url(action='Idfilm'))
        addDir(u'Tìm kiếm', '', '', '', '', '', get_url(action='thuvienhdsearch'))
        # addDir('Chia se cho nhau', get_url(action='sharingTogether'))


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])

# xbmcplugin.addSortMethod(_HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
# Finish creating a virtual folder.
xbmcplugin.endOfDirectory(_HANDLE)
