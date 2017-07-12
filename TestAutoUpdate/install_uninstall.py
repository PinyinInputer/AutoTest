import os
import time
from pywinauto import Application
import win32com.shell.shell as shell


def is_admin():
    if os.name == 'nt':
        # WARNING: requires Windows XP SP2 or higher!
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0
    else:
        raise RuntimeError('Unsupported operating system for this module: %s' % os.name)


def run_external(exe_path):
    # WARNING should run python as Administrator and run installer as normal
    if not is_admin():
        raise RuntimeError('Should run python as Administrator')
    shell.ShellExecuteEx(lpVerb='runas', lpFile=exe_path, lpParameters='')


def resolve_confirm_dlg(title_re, cancel=False):
    try:
        confirm_app = Application().connect(title_re=title_re)
    except Exception as e:
        raise RuntimeError('Cannot find confirm dialog, exception: %s' % repr(e))
    confirm_dlg = confirm_app.window_(title_re=title_re)
    print(confirm_dlg.print_control_identifiers())
    l, r, t, b = confirm_dlg.Rectangle().left, confirm_dlg.Rectangle().right, \
                 confirm_dlg.Rectangle().top, confirm_dlg.Rectangle().bottom
    pos = (int(l + (r - l) * 0.87), int(t + (b - t) * 0.87)) if cancel else (int(l + (r - l) * 0.64), int(t + (b - t) * 0.87))

    confirm_dlg.click_input(coords=pos, absolute=True)


def resolve_configure_dlg():
    try:
        configure_app = Application().connect(title_re=u'2345王牌输入法设置向导')
    except Exception as e:
        raise RuntimeError('Cannot find confirm dialog, exception: %s' % repr(e))
    configure_dlg = configure_app.window_(title_re=u'2345王牌输入法设置向导')
    print(configure_dlg.print_control_identifiers())
    l, r, t, b = configure_dlg.Rectangle().left, configure_dlg.Rectangle().right, \
                 configure_dlg.Rectangle().top, configure_dlg.Rectangle().bottom
    pos = (int(l + (r - l) * 0.92), int(t + (b - t) * 0.94))
    while configure_dlg.exists():
        configure_dlg.click_input(coords=pos, absolute=True)


def install(installer_path):
    # 1. start installer and wait for UerAccoutCotrol confirm
    run_external(installer_path)
    time.sleep(2)

    # 2. find the installer dialog
    installer = None
    try:
        installer = Application().connect(title_re=u'2345王牌输入法 v[0-9]+\.[0-9]+ 安装')
    except Exception as e:
        raise RuntimeError('Cannot find installer, exception: %s' % repr(e))

    # 3. get position of the install button and note the installed path
    # can get all handlers by call like this:
    # print(installer.window_(title_re=u'2345王牌输入法 v[0-9]+\.[0-9]+ 安装').print_control_identifiers())
    install_dlg = installer.window_(title_re=u'2345王牌输入法 v[0-9]+\.[0-9]+ 安装')
    print(install_dlg.print_control_identifiers())

    installed_path = None
    for widget in install_dlg.descendants():
        if widget.class_name() == 'Edit':
            installed_path = widget.window_text()

    l, r, t, b = install_dlg.Rectangle().left, install_dlg.Rectangle().right, \
                 install_dlg.Rectangle().top, install_dlg.Rectangle().bottom
    pos = (int((l + r) / 2), int(t + (b - t) * 0.775))
    print('Move mouse to button(%d, %d)' % (pos[0], pos[1]))
    install_dlg.click_input(coords=pos, absolute=True)
    time.sleep(2)

    # 4. wait for finish
    while b != install_dlg.Rectangle().bottom:
        time.sleep(2)
    install_dlg.click_input(coords=pos, absolute=True)

    try:
        time.sleep(2)
        resolve_configure_dlg()
    except:
        print('No configure dlg, ignore')
    return installed_path


def uninstall(uninstaller_path):
    # 1. start uninstaller
    run_external(uninstaller_path)
    time.sleep(2)

    # 2. find the installer dialog
    uninstaller = None
    try:
        uninstaller = Application().connect(title=u'2345王牌输入法 卸载程序')
    except Exception as e:
        raise RuntimeError('Cannot find uninstaller, exception: %s' % repr(e))

    # 3. get position of the install button and note the installed path
    # can get all handlers by call like this:
    # print(installer.window_(title_re=u'2345王牌输入法 v[0-9]+\.[0-9]+ 安装').print_control_identifiers())
    uninstall_dlg = uninstaller.window_(title=u'2345王牌输入法 卸载程序')
    print(uninstall_dlg.print_control_identifiers())

    l, r, t, b = uninstall_dlg.Rectangle().left, uninstall_dlg.Rectangle().right, \
                 uninstall_dlg.Rectangle().top, uninstall_dlg.Rectangle().bottom
    pos = (int(l + (r - l) * 0.713), int(t + (b - t) * 0.923))
    print('Move mouse to button(%d, %d)' % (pos[0], pos[1]))
    uninstall_dlg.click_input(coords=pos, absolute=True)
    resolve_confirm_dlg(title_re=u'2345王牌输入法卸载程序')

    # 4. wait for finish
    confirm_pos = (int(l + (r - l) * 0.9), int(t + (b - t) * 0.9))
    while uninstall_dlg.exists():
        uninstall_dlg.click_input(coords=confirm_pos, absolute=True)
        time.sleep(5)


def main():
    installer = r'C:Users\wo\Desktop\2345pinyin_v4.6.5804.exe'
    install(installer)

    uninstaller = r'C:\Program Files (x86)\2345Soft\2345Pinyin\4.6.1.5804\Uninstall.exe'
    uninstall(uninstaller)


if __name__ == '__main__':
    main()
