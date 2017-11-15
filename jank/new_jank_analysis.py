#!/usr/bin/env python
# coding = utf-8
import json
import sys
import pickle
from matplotlib import pyplot

FILE_NAME = ''

LAUNCH_TIME_DICT= {}

TOP_LAUNCH_COUNT_APP_OLD = [
"com.android.settings/.SubSettings",
"com.android.mms/.ui.SingleRecipientConversationActivity",
"com.miui.securitycenter/com.miui.wakepath.ui.ConfirmStartActivity",
"com.android.browser/.BrowserActivity",
"com.tencent.mm/.plugin.profile.ui.ContactInfoUI",
"com.tencent.mm/.ui.chatting.gallery.ImageGalleryUI",
"com.tencent.mm/.plugin.setting.ui.setting.SettingsUI",
"com.tencent.mm/.ui.chatting.SendImgProxyUI",
"com.tencent.mobileqq/.activity.photo.PhotoPreviewActivity",
"com.tencent.mobileqq/.activity.aio.photo.AIOGalleryActivity",
"com.eg.android.AlipayGphone/com.alipay.mobile.homefeeds.morecards.HomeMoreCardsActivity",
"com.eg.android.AlipayGphone/com.alipay.mobile.nebulacore.ui.H5Activity"
]

TOP_LAUNCH_COUNT_APP = [
"com.android.quicksearchbox/.SearchActivity",
"com.android.settings/.SubSettings",
"com.android.systemui/.recents.RecentsActivity",
"com.android.settings/.MainSettings",
"com.android.camera/.Camera",
"com.android.updater/.MainActivity",
"com.tencent.mm/.plugin.sns.ui.En_424b8e16",
"com.tencent.mm/.ui.LauncherUI",
"com.android.incallui/.InCallActivity",
"com.taobao.taobao/com.taobao.tao.homepage.MainActivity3"
]

MODLE_LIST = ['MI 6','MIX 2','MI 5','Redmi Note 4X']

def parseFile():
    jank_dict = {}
    fileContent = open(FILE_NAME,'r').readlines()
    for line in fileContent:
        infos = line.split('{', 1) #Only split for one time. Split by first '{'
        print '-----------infos:', infos

        imei = infos[0].split('\t')[0]
        init_timestamp = infos[0].split('\t')[1]
        version = formatVersion(infos[0].split('\t')[2])
        model = infos[0].split('\t')[3]

        key = model+':'+version+':'+imei+':'+init_timestamp

        jank_json = byteify(json.loads('{' + infos[1]))
        uptime = jank_json['uptime_sec']
        print '---',imei,init_timestamp, model, version, uptime
        print '---',jank_json
        if key not in jank_dict:
            jank_dict[key] = jank_json
        else:
            if uptime > jank_dict[key]['uptime_sec']:
                jank_dict[key] = jank_json
    print 'jank_dict:', jank_dict
    saveFile(jank_dict)


def saveFile(jank_dict):
    f1 = open('JANK_DICT.txt','wb')
    pickle.dump(jank_dict, f1)
    f1.close()

def readFile():
    f2 = open('JANK_DICT.txt','rb')
    dict_content = pickle.load(f2)
    f2.close()
    return dict_content

def appendLaunchTimeDict(source, destination):
    for pkg,avg_launch_time in source.items():
        if destination.has_key(pkg):
            launch_time_list = (destination[pkg] + avg_launch_time)
            destination[pkg] = launch_time_list
        else:
            destination[pkg] = avg_launch_time


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


def drawByModel(model, launch_time_dict):
    version_list = []
    avg_launch_time_list = []
    avg_launch_tim_count_list = []
    pic = 0

    sorted_version = sorted(launch_time_dict.keys())
#    print '-----sorted_version:', sorted_version

    for app in TOP_LAUNCH_COUNT_APP:
        pic = pic + 1
        for k in sorted_version:
            if k.startswith(model):
                v = launch_time_dict[k]
                if k not in version_list:
                    version_list.append(k)

                #print 'len(v):', len(v)
                if app in v.keys():
#                    print 'ver:', k , ' v.has_key:', app
                    if len(v[app]) > 10:
                        avg_launch_time_list.append(calculateAVGLaunchTime(v[app], app))
                        avg_launch_tim_count_list.append(len(v[app]))
                    else:
                        avg_launch_time_list.append(0)
                        # version_list.remove(k)
                        avg_launch_tim_count_list.append(len(v[app]))
                else:
#                    print 'ver:', k , ' v.not has_key:', app
                    avg_launch_time_list.append(0)
                    # version_list.remove(k)
                    avg_launch_tim_count_list.append(0)

#        print 'version_list:', version_list
#        print 'APP:', app, '  avg_launch_time_list:', avg_launch_time_list

        pyplot.plot(version_list, avg_launch_time_list,
            marker='o', label=app + ' ' + str(avg_launch_tim_count_list))

        pyplot.legend(loc='best', ncol=1)
        version_list = []
        avg_launch_time_list = []
        avg_launch_tim_count_list = []


        if pic%5 == 0 or pic == len(TOP_LAUNCH_COUNT_APP):
            pyplot.subplots_adjust(bottom=0.15)
            pyplot.xlabel('Version')
            pyplot.ylabel('ms')
            pyplot.title('Avg launch time')
            # mng = pyplot.get_current_fig_manager()
            # mng.full_screen_toggle()
            manager = pyplot.get_current_fig_manager()
            manager.resize(*manager.window.maxsize())
            pyplot.show()


def drawByAPP(app, model_list, launch_time_dict):
    sorted_version = sorted(launch_time_dict.keys())

    version_list = []
    avg_launch_time_list = []
    avg_launch_tim_count_list = []
    pic = 0

    for model in model_list:
        pic = pic + 1
        for k in sorted_version:
            if k.startswith(model):
                v = launch_time_dict[k]
                if k not in version_list:
                    version_list.append(k.split(':')[1])

                if app in v.keys():
#                    print 'ver:', k , ' v.has_key:', app
                    if len(v[app]) > 10:
                        avg_launch_time_list.append(calculateAVGLaunchTime(v[app], app))
                        avg_launch_tim_count_list.append(len(v[app]))
                    else:
                        avg_launch_time_list.append(0)
                        # version_list.remove(k)
                        avg_launch_tim_count_list.append(len(v[app]))
                else:
#                    print 'ver:', k , ' v.not has_key:', app
                    avg_launch_time_list.append(0)
                    # version_list.remove(k)
                    avg_launch_tim_count_list.append(0)

        pyplot.plot(version_list, avg_launch_time_list,
            marker='o', label=model + ' ' + str(avg_launch_tim_count_list))

        pyplot.legend(loc='best', ncol=1)
        version_list = []
        avg_launch_time_list = []
        avg_launch_tim_count_list = []

        if pic%5 == 0 or pic == len(TOP_LAUNCH_COUNT_APP):
            pyplot.subplots_adjust(bottom=0.15)
            pyplot.xlabel('Version')
            pyplot.ylabel('ms')
            pyplot.title('Avg launch time of <<< ' + app + ' >>>')
            # mng = pyplot.get_current_fig_manager()
            # mng.full_screen_toggle()
            manager = pyplot.get_current_fig_manager()
            manager.resize(*manager.window.maxsize())
            pyplot.show()



def formatVersion(ver):
    vers = ver.split('.')
    year = vers[0]
    month = vers[1]
    day = vers[2]
    if len(month) < 2:
        month = '0' + month

    if len(day) < 2:
        day = '0' + day
    return (year + '.' + month + '.' + day)

def calculateAVGLaunchTime(launch_time_list, app):
    count = 0
    total = 0
    for item in launch_time_list:
        if item < 5000:
            total = total + item
            count = count + 1
        else:
            print '!!!---', app, ' > 5000, item:', item
    if count == 0:
        return 0
    return (int)(total/count)

def draw():
    jank_dict = readFile()
    print 'len(jank_dict.keys()):', len(jank_dict.keys())
#    print 'jank_dict:', jank_dict

  # for model in MODLE_LIST:
  #   drawByModel(model, LAUNCH_TIME_DICT)

  # for app in TOP_LAUNCH_COUNT_APP:
  #   drawByAPP(app, MODLE_LIST, LAUNCH_TIME_DICT)

def noImei(jank_dict):
    jank_dict


def getTopFrecAPPs():
    LAUNCH_TIME_DICT = readFile()
    top_frec_app = {}
    for k in LAUNCH_TIME_DICT.keys():
        model = k.split(':')[0]
        print '--getTopFrecAPPs model:', model
        if model in MODLE_LIST:
            print '--getTopFrecAPPs in model:', model
            v = LAUNCH_TIME_DICT[k]
            for pkgs in v.keys():
                if pkgs not in top_frec_app.keys():
                    top_frec_app[pkgs] = 1
                else:
                    top_frec_app[pkgs] = top_frec_app[pkgs] + 1
    print 'top_frec_app:', top_frec_app
    print '---Sorted:', sorted(top_frec_app.items(), key=lambda d: d[1], reverse=False)


def main():
    # parseFile()
    draw()
    # getTopFrecAPPs()





if __name__ == '__main__':
    print 'len(sys.argv)', len(sys.argv)
    print '---------- sys.argv', sys.argv
    FILE_NAME = sys.argv[1]
    main()
