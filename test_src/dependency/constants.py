# -*- coding:utf-8 -*-

# DEBUG mode
DEBUG = False

# Performance Center Regist URL
REG_URL = "http://3p.taobao.net/3p/device_online"

# Report URL
REPORT_URL = 'http://3p.taobao.net/3p/autotest?file_type=html&file_name=%s&test_id=%s'
REPORT_URL_WITHOUT_TESTID = 'http://3p.taobao.net/3p/autotest?file_type=html&file_name=%s'

# WebSocket server configuration
WS_PORT = "9998"
WS_ROOT = "tools"

# Logger
LOGGER_SERVER_IP                = '127.0.0.1'
LOGGER_SERVER_PORT              = 30100
LOGGER_DIR                      = 'logs'
LOGGER_ONLINE_DIR               = 'tools'
LOGGER_SERVER_NAME              = 'VMS'
LOGGER_CLIENT_MAIN              = 'VMC'
LOGGER_CLIENT_FPS               = 'FPS'
LOGGER_CLIENT_PERF              = 'PERF'
LOGGER_CLIENT_ALIIM_CHAT        = 'IMCH'
LOGGER_CLIENT_DRAG_NOTEPAD      = 'DNP'
LOGGER_CLIENT_DRAG_IE           = 'DIE'
LOGGER_CLIENT_OFFICE_EXCEL      = 'OEXC'
LOGGER_CLIENT_OFFICE_PPT        = 'OPPT'
LOGGER_CLIENT_OFFICE_WORD       = 'OWRD'
LOGGER_CLIENT_SCROLL_NOTEPAD    = 'SNP'
LOGGER_CLIENT_VIDEO_IE          = 'VIE'
LOGGER_CLIENT_VIDEO_IE_SCROLL   = 'VIES'
LOGGER_CLIENT_VIDEO_LOCAL       = 'VLO'
LOGGER_CLIENT_MUAT               = 'MUAT'
LOGGER_FILE                     = 'log_debug.txt'
LOGGER_ONLINE_FILE              = 'log_online_debug.txt'
LOGGER_FILE_MAX_BYTE            = 1048576
LOGGER_FILE_BACKUP_COUNT        = 5
LOGGER_FILE_MEMORY_CACHE        = 1024

# Upgrade
VERSION_FILE            = "version.txt"
UPGRADE_INFO_FILE       = "upgrade.txt"
UPGRADE_INFO_URL        = "http://3p.taobao.net/download/upgrade/upgrade.txt"
UPGRADE_IMAGE_FILE      = "VMAgent.zip"
UPGRADE_IMAGE_URL       = "http://3p.taobao.net/download/upgrade/VMAgent.zip"
UPGRADE_EXTRACT_DIR     = "image_upgrade"
UPGRADE_WS_STATUS_ID    = "9999UpgradeStatus"
UPGRADE_WS_REQUEST_ID   = "9999UpgradeRequest"
UPGRADE_MMAP_TAG_NAME   = "upgrade_mmap_tag"
UPGRADE_CHECK_INTERVAL  = 7200
UPGRADE_POLL_INTERVAL   = 5
UPGRADE_AUTO_EXCLUDE_S  = 9
UPGRADE_AUTO_EXCLUDE_E  = 21

# Path of the Software
PATH_ALIIM  = "C:\\Program Files (x86)\\AliWangWang\\AliIM.exe"
ALICDAGT = "C:\\Windows\\vdi_server\\AliCDAgt.exe"

# Media player
PLAYER_VLC  = "vlc\\vlc-2.1.5\\vlc.exe"

# Internal message ID
ID_ALIWANGWANG_REMOTE = '9999AliIMRemote'

# download debug script
SCRIPT_DOWNLOAD_INTERNET = False

SCRIPT_DOWNLOAD_OFFICIAL_PATH = 'http://3p.taobao.net:80/download'
if not DEBUG:
    SCRIPT_DOWNLOAD_PATH = SCRIPT_DOWNLOAD_OFFICIAL_PATH
else:
    if SCRIPT_DOWNLOAD_INTERNET:
        SCRIPT_DOWNLOAD_PATH = 'http://10.32.168.29'
    else:
        SCRIPT_DOWNLOAD_PATH = 'debug_scripts'

########## MicroPC Test ##########
# Test Account
TEST_USERNAME           = 'ourtest_auto@126.com'
TEST_PASSWD             = 'Autotest1234~'
#timeout
Time_Out                = 10
#浏览器网页响应时间
TIME_OUT                = 35

#MobileIm Account
TEST_WX_USERNAME        = 'countrymars'
TEST_WX_PASSWD          = 'liudongjie126'

#MobileIm Remote Account
TEST_REMOTE_USERNAME    = 'tb3489593'

#Set test running timeout
#run the testgroup by hours. if set 0 ,the test run once.

RUNNING_TIMEOUT          = 36

# Tools
ADB                     = 'adb'
AAPT                    = 'aapt'

# Mouse Type
MouseLeftKey            = 0
MouseRightKey           = 1
MouseWheelUp            = 1
MouseWheelDown          = -1

# NonBlockStreamReader timeout
ADBLOG_READLINE_TIMEOUT = 1

# APP Directory
APKS_DIR                = 'apks'


# Provision FrameLayout
FIRST_START_X                    = 960
FIRST_START_Y                    = 770
# AUTH CODE 70D7 DAA3 6157
AUTH_CODE_EDITBOX_X              = 690
AUTH_CODE_EDITBOX_Y              = 430
AUTH_CODE_16BIT                  = [0xe,0x7,0x20,0xe,0x20,0x1d,0x1d,0xa,0xd,0x8,0xc,0xe]
AUTH_CODE_NEXTSTEP_X             = 1030
AUTH_CODE_NEXTSTEP_Y             = 765

# APP List Test

MUAT_APP_LIST_COUNT              = 10
MUAT_APP_LIST_EMPTY_X            = 1000
MUAT_APP_LIST_EMPTY_Y            = 900
MUAT_APP_LIST_POINT_X            = 1870
MUAT_APP_LIST_POINT_Y            = 1060
MUAT_APP_LIST_RESULT_ITEM        = 'AppList'
MUAT_APP_LIST_RESULT_ITEM_CN     = '应用列表-响应时间'

# APP Launch Time Test
MUAT_APP_LAUNCH_TIME_COUNT       = 5
MUAT_APP_LAUNCH_TIME_LIST        = ['appstore.apk',
                                   'Browser.apk',
                                   'MpcSettings.apk',
                                   ]
MUAT_APP_LAUNCH_TIME_LIST_CN     = {'appstore.apk':'应用商店-启动时间',
                                   'Browser.apk':'浏览器-启动时间',
                                   'MpcSettings.apk':'设置-启动时间',
                                   }

# Status Bar Test
# 1680(40-LANG)1720(40-Net)1760(40-Audio)1800(120-Time)1920
MUAT_STATUS_BAR_COUNT            = 5
MUAT_STATUS_BAR_EMPTY_X          = 960
MUAT_STATUS_BAR_EMPTY_Y          = 30
MUAT_STATUS_BAR_LANG_POINT_X     = 1700
MUAT_STATUS_BAR_LANG_POINT_Y     = 15
MUAT_STATUS_BAR_RESULT_LANG      = 'lang'
MUAT_STATUS_BAR_NET_POINT_X      = 1740
MUAT_STATUS_BAR_NET_POINT_Y      = 15
MUAT_STATUS_BAR_RESULT_NET       = 'net'
MUAT_STATUS_BAR_AUDIO_POINT_X    = 1780
MUAT_STATUS_BAR_AUDIO_POINT_Y    = 15
MUAT_STATUS_BAR_RESULT_AUDIO     = 'audio'
MUAT_STATUS_BAR_CALENDAR_POINT_X = 1860
MUAT_STATUS_BAR_CALENDAR_POINT_Y = 15
MUAT_STATUS_BAR_RESULT_CALENDAR  = 'calendar'
MUAT_STATUS_BAR_RESULT_CN        = {'calendar':'日历-响应时间',
                                   'lang':'语言-响应时间',
                                   'net':'网络-响应时间',
                                   'audio':'音量-响应时间',
                                   }
MUAT_STATUS_BAR_TEST_ITEMS       = [(MUAT_STATUS_BAR_CALENDAR_POINT_X, MUAT_STATUS_BAR_CALENDAR_POINT_Y, MUAT_STATUS_BAR_RESULT_CALENDAR),
                                   (MUAT_STATUS_BAR_NET_POINT_X, MUAT_STATUS_BAR_NET_POINT_Y, MUAT_STATUS_BAR_RESULT_NET),
                                  ]

# Setting Test
MUAT_SETTING_COUNT               = 5
MUAT_SETTING_APK                 = 'MpcSettings.apk'
MUAT_SETTING_X                   = 1920-45
MUAT_SETTING_Y                   = 1080-25
MUAT_SETTING_APK_RESOURCEIDS     = ['exToggleButton8',
                                   'exToggleButton0',
                                   'exToggleButton7',
                                   'exToggleButton1',
                                   'exToggleButton5',
                                   'exToggleButton2',
                                   'exToggleButton4',
                                  ]
MUAT_SETTING_APK_RESOURCEIDS_CN  = {'exToggleButton0':'系统-响应时间',
                                   'exToggleButton1':'网络-响应时间',
                                   'exToggleButton2':'壁纸-响应时间',
                                   'exToggleButton4':'显示-响应时间',
                                   'exToggleButton5':'日期和时间-响应时间',
                                   'exToggleButton7':'版权信息-响应时间',
                                   'exToggleButton8':'设备注册-响应时间',
                                  }
MUAT_SETTING_RESULT_TOTAL        = 'items_avg'

# Window Smoothness Test
MUAT_WINDOW_SMOOTHNESS_LIST      = ['Browser.apk',
                                  ]
MUAT_WINDOW_SMOOTHNESS_LIST_CN   = {'Browser.apk':'拖动浏览器-帧率',
                                  }
MUAT_DRAG_TOP_POINT_X            = 960
MUAT_DRAG_TOP_POINT_Y            = 30
MUAT_DRAG_BOTTOM_POINT_X         = 960
MUAT_DRAG_BOTTOM_POINT_Y         = 1050
MUAT_WINDOW_SMOOTHNESS_SPEED     = ['fast', 'normal', 'slow']
MUAT_WINDOW_SMOOTHNESS_COUNT     = [(0, MUAT_DRAG_TOP_POINT_X, MUAT_DRAG_TOP_POINT_Y),
                                   (1, MUAT_DRAG_BOTTOM_POINT_X, MUAT_DRAG_BOTTOM_POINT_Y),
                                   (2, MUAT_DRAG_TOP_POINT_X, MUAT_DRAG_TOP_POINT_Y),
                                   (3, MUAT_DRAG_BOTTOM_POINT_X, MUAT_DRAG_BOTTOM_POINT_Y),
                                   (4, MUAT_DRAG_TOP_POINT_X, MUAT_DRAG_TOP_POINT_Y),
                                   (5, MUAT_DRAG_BOTTOM_POINT_X, MUAT_DRAG_BOTTOM_POINT_Y),
                                  ]

# Browsing Test
MUAT_BROWSING_LIST               = ['www.taobao.com',
                                  ]
MUAT_BROWSING_LIST_CN            = {'www.taobao.com':'淘宝网-帧率',
                                  }
MUAT_BROWSING_SWIPE_SPEED        = ['fast', 'normal', 'slow']
MUAT_BROWSING_SWIPE_COUNT        = 5
MUAT_BROWSING_SWIPE_DIR_COUNT    = 5
MUAT_SWIPE_START_POINT_X         = 1860
MUAT_SWIPE_START_POINT_Y         = 900
MUAT_SWIPE_END_POINT_X           = 1860
MUAT_SWIPE_END_POINT_Y           = 400

########## MicroPC Test ##########