import sys
import urllib2
import json

import xbmcgui
import xbmcplugin
from urlparse import parse_qsl

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

def play():
	response = urllib2.urlopen('https://mfwkweb-api.clarovideo.net/services/player/getmedia?api_version=v5.8&authpn=html5player&authpt=ad5565dfgsftr&format=json&region=colombia&device_id=c89db753d8cab3022e37691a5643e25b&device_category=web&device_model=html5&device_type=html5&device_so=Chrome&device_manufacturer=windows&HKS=(8cc331b0ebdfe8ab592a13b703068e15)&stream_type=dashwv&group_id=717024&preview=0&css=0&device_name=Chrome&crDomain=https://www.clarovideo.com')

	data = json.load(response)

	device_id = data['entry']['device_id']
	token = json.loads(data['response']['media']['challenge'])['token']

	play_item = xbmcgui.ListItem(path='https://latamliveclarovideo.akamaized.net/Content/dash_fk/Live/Channel(CONCERT_CHANNEL_HD)/manifest.mpd')
	play_item.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
	play_item.setProperty('inputstream.adaptive.license_key', 'https://widevine-vod.clarovideo.net/licenser/getlicense|Content-Type=|{"token":"'+token+'","device_id":"'+device_id+'","widevineBody":"b{SSM}"}|')
	play_item.setProperty('inputstream.adaptive.server_certificate', 'CrYCCAMSEHL+DSD08domI9jFJXcARnkYtpOAqgUijgIwggEKAoIBAQDEG8PxTwiALyDHGvKZjJxo7G6+XKHnjV4p2F+TvUng79fyRvk8rpEjl4k+V4V4YIfEIh2ZirIE3J8kCsNWvkdX3ZAsUVrEBf2mzpGTfsMGWsLbVPCMutqR/eLGpI2mAwkdyTEhoGsvDXv0ty5Q+z1YccFHyfNPVUfkEsYT8kyR/9f+gNvxWSNQcKfbM3DBhZNkvH3msCZnvGIZl/HvLU8hfe8ycMRExXKwVlpaCbe/0wMEanq38ENMhKJSrtWGQbFFMSMOyEWQwqhP0yY+zl4wQ+AC6VA5rVlegSa2u8+yGKTZwlLScQ/vd/y9p8vQEBDMAC5RP9hH8NfH6RaxovozAgMBAAE6CWRsYXR2Lm5ldBKAA2S7G3l4ei75sFFlhp5nFe8Vj/F8y4/0WNsliYzeEwFkZnrQS2ikJcgV7mPAre3i+TT07opXOJOSjkBk18G2/YOwK3DSXK2EpGCBEWOnncpPI2aHoy0zGvH8tdbGaMplYivD3agR14LVsQUx0YI3hO09OrUMscqgUonjEn3/TTgooLRRGtshRBqIcp0Ob/Cv3Dc6ech61j1/lK+8Lnt7U5Rzy0lCtbEqLXWL2QdoEMoROJ70Vkvv3SshpEtzn65yA87o2mkSRK1yZG7xk1IWQ+VOpXIgHrR8icsVaSvlK85L984Ziv8xFsp/cCqTMxBZplFviYv4Tkzv2H09qfg3OmeDfUWxg+u5YKJik9bu2iWFyBju/AQRfkUqvWaknV0sNm6keZmgVUe25k7H22hID4LuLxTTJcGPIJ1ZJayXYa/YE9ZnryqTgUyjawCIXS0+X4OaLs6FA2x0eXWQL6rjdutfts3m2vHySEn27730deLw86AxB78jcir7jhXNXvGzCQ==');
	play_item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
	play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
	play_item.setMimeType('application/dash+xml')
	play_item.setContentLookup(False)

	xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring

	params = dict(parse_qsl(sys.argv[2][1:]))
	if params and params['action'] == 'play':
		play()
	else:
		xbmcplugin.setPluginCategory(_handle, 'Samples')
		xbmcplugin.setContent(_handle, 'videos')
		list_item = xbmcgui.ListItem(label='Claro')
		list_item.setProperty('IsPlayable', 'true')
		list_item.setInfo('video', {'mediatype': 'video'})
		xbmcplugin.addDirectoryItem(_handle, _url + '?action=play', list_item, False)
		xbmcplugin.endOfDirectory(_handle)