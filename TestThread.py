import requests
from time import sleep

url = "http://192.168.100.233/ISAPI/PTZCtrl/channels/1/continuous"

payloadLeftAbove = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><PTZData><pan>-60</pan><tilt>60</tilt></PTZData>"
payloadAbove = '<?xml version: \"1.0\" encoding="UTF-8"?><PTZData><pan>0</pan><tilt>60</tilt></PTZData>'
payloadRightAbove = "<?xml version:\"1.0\" encoding=\"UTF-8\"?><PTZData><pan>60</pan><tilt>60</tilt></PTZData>"

payloadLeft = "<?xml version: \"1.0\" encoding=\"UTF-8\"?><PTZData><pan>-60</pan><tilt>0</tilt></PTZData>"
payloadRight = "<?xml version: \"1.0\" encoding=\"UTF-8\"?><PTZData><pan>60</pan><tilt>0</tilt></PTZData>"

payloadLeftBottom = "<?xml version: \"1.0\" encoding=\"UTF-8\"?><PTZData><pan>-60</pan><tilt>-60</tilt></PTZData>"
payloadBottom = "<?xml version: \"1.0\" encoding=\"UTF-8\"?><PTZData><pan>0</pan><tilt>-60</tilt></PTZData>"
payloadRightBottom = "<?xml version: \"1.0\" encoding=\"UTF-8\"?><PTZData><pan>60</pan><tilt>-60</tilt></PTZData>"

payloadCancel = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><PTZData><pan>0</pan><tilt>0</tilt></PTZData>"

payloadAutoPan = "<?xml version: \"1.0\" encoding=\"UTF-8\"?><autoPanData><autoPan>60</autoPan></autoPanData>"
payloadStopAutoPan = "<?xml version: \"1.0\" encoding=\"UTF-8\"?><autoPanData><autoPan>0</autoPan></autoPanData>"

payloadZoomOut = "<?xml version: \"1.0\" encoding=\"UTF-8\"?><PTZData><zoom>-60</zoom></PTZData>"
payloadZoomIn = "<?xml version: \"1.0\" encoding=\"UTF-8\"?><PTZData><zoom>60</zoom></PTZData>"
payloadZoomStop = "<?xml version: \"1.0\" encoding=\"UTF-8\"?><PTZData><zoom>0</zoom></PTZData>"

headers = {
  'Connection': 'keep-alive',
  'Cache-Control': 'max-age=0',
  'Accept': '*/*',
  'X-Requested-With': 'XMLHttpRequest',
  'If-Modified-Since': '0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': 'http://192.168.100.233',
  'Referer': 'http://192.168.100.233/doc/page/preview.asp',
  'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
  'Cookie': 'language=vi; WebSession_872ecca789=ab703ef7be5a702c342da7d123147fe4c903ea96bb8292bd6e39d422bafdd55a; _wnd_size_mode=4'
}

def leftAboveMove():
    response = requests.request("PUT", url, headers=headers, data=payloadLeftAbove)
    sleep(0.5)
    response = requests.request("PUT", url, headers=headers, data=payloadCancel)

def AboveMove():
    response = requests.request("PUT", url, headers=headers, data=payloadAbove)
    sleep(0.5)
    response = requests.request("PUT", url, headers=headers, data=payloadCancel)

def rightAboveMove():
    response = requests.request("PUT", url, headers=headers, data=payloadRightAbove)
    sleep(0.5)
    response = requests.request("PUT", url, headers=headers, data=payloadCancel)

def rightMove():
    response = requests.request("PUT", url, headers=headers, data=payloadRight)
    sleep(0.5)
    response = requests.request("PUT", url, headers=headers, data=payloadCancel)

def leftMove():
    response = requests.request("PUT", url, headers=headers, data=payloadLeft)
    sleep(0.5)
    response = requests.request("PUT", url, headers=headers, data=payloadCancel)

def autoPanMove():
    response = requests.request("PUT", url, headers=headers, data=payloadAutoPan)

def stopAutoPanMove():
    response = requests.request("PUT", url, headers=headers, data=payloadStopAutoPan)

def zoomOut():
    response = requests.request("PUT", url, headers=headers, data=payloadZoomOut)
    sleep(0.5)
    response = requests.request("PUT", url, headers=headers, data=payloadZoomStop)

def zoomOut():
    response = requests.request("PUT", url, headers=headers, data=payloadZoomIn)
    sleep(0.5)
    response = requests.request("PUT", url, headers=headers, data=payloadZoomStop)


if __name__ == "__main__":
    #rightAboveMove()
    autoPanMove()