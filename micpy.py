from mpython import *
import network
import time
import audio
import urequests
import json
import machine
import ubinascii

my_wifi = wifi()

my_wifi.connectWiFi("5566", "asdqwe123")

def on_button_a_down(_):
    time.sleep_ms(10)
    if button_a.value() == 1: return
    rgb[0] = (int(102), int(0), int(0))
    rgb.write()
    time.sleep_ms(1)
    oled.fill(0)
    oled.DispChar("按下A键开始识别", 0, 0, 1)
    oled.DispChar(get_asr_result(2), 0, 16, 1)
    oled.show()
    rgb[0] = (0, 0, 0)
    rgb.write()
    time.sleep_ms(1)

def get_asr_result(_time):
    audio.recorder_init()
    audio.record("temp.wav", int(_time))
    audio.recorder_deinit()
    _response = urequests.post("http://119.23.66.134:8085/file_upload",
        files={"file""temp.wav", "audio/wav")},
        params={"appid":"1", "mediatype":"2", "deviceid":ubinascii.hexlify(machine.unique_id()).decode().upper()})
    rsp_json = _response.json()
    _response.close()
    if "text" in rsp_json:
        return rsp_json["text"]
    elif "Code" in rsp_json:
        return "Code:%s" % rsp_json["Code"]
    else:
        return rsp_json

button_a.irq(trigger=Pin.IRQ_FALLING, handler=on_button_a_down)


oled.fill(0)
oled.DispChar("按下A键开始识别", 0, 0, 1)
oled.show()[/mw_shl_code]