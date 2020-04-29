import time
import pyperclip
import threading


class ClipboardWatcher(threading.Thread):
    def __init__(self, callback, pause=5.):
        super(ClipboardWatcher, self).__init__()
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self):
        recent_value = ""
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                self._callback(tmp_value)
                recent_value = pyperclip.paste()
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True


def copy_to_stdout(text):
    text = text.replace('\n', ' ')
    text = text.replace('\r', '')
    pyperclip.copy(text)
    print(text)


if __name__ == "__main__":
    watcher = ClipboardWatcher(copy_to_stdout, 1.)
    watcher.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            watcher.stop()
            break
