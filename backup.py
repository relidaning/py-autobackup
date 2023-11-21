# -*- coding: GBK -*-
import os
import win32file
import win32con
import time

from conf import *

class Achieve3:

  def __init__(self, Conf):
    self.Conf = Conf

  def watch(self):
    ACTIONS = {
      1: "Created",
      2: "Deleted",
      3: "Updated",
      4: "Renamed from something",
      5: "Renamed to something"
    }
    # Thanks to Claudio Grondi for the correct set of numbers
    FILE_LIST_DIRECTORY = 0x0001

    path_to_watch = "."
    hDir = win32file.CreateFile(
      path_to_watch,
      FILE_LIST_DIRECTORY,
      win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
      None,
      win32con.OPEN_EXISTING,
      win32con.FILE_FLAG_BACKUP_SEMANTICS,
      None
    )
    while 1:
      #
      # ReadDirectoryChangesW takes a previously-created
      # handle to a directory, a buffer size for results,
      # a flag to indicate whether to watch subtrees and
      # a filter of what changes to notify.
      #
      # NB Tim Juchcinski reports that he needed to up
      # the buffer size to be sure of picking up all
      # events when a large number of files were
      # deleted at once.
      #
      results = win32file.ReadDirectoryChangesW(
        hDir,
        1024,
        True,
        win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
        win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
        win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
        win32con.FILE_NOTIFY_CHANGE_SIZE |
        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
        win32con.FILE_NOTIFY_CHANGE_SECURITY,
        None,
        None
      )
      for action, file in results:
        full_filename = os.path.join(path_to_watch, file)
        # print(full_filename, ACTIONS.get(action, "Unknown"))
        filename = full_filename.split(os.sep)[1]
        if filename in self.Conf.target and ACTIONS.get(action, "Unknown") == 'Updated':
          now = time.strftime("%Y%m%d%H%M%S", time.localtime())
          print('������Ŀ���ļ��޸�:', filename, '@', now)
          backup_path = "." + os.sep + "backups"
          if not os.path.exists(backup_path):
            os.mkdir(backup_path)
          os.system("copy %s %s" % (full_filename,
                                    backup_path + os.sep + filename.split(".")[0] + "-" + now + "." +
                                    filename.split(".")[1]))
