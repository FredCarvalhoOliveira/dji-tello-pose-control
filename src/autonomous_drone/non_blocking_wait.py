import time


class NonBlockingWait:
    def __init__(self):
        self.__timestamp: int = 0
        self.__wait_time: int = 0

    def wait_millis(self, wait_time: int):
        self.__wait_time = wait_time
        self.__timestamp = time.time()

    def has_time_passed(self) -> bool:
        if int(round((time.time() - self.__timestamp) * 1000)) >= self.__wait_time:
            self.reset()
            return True
        return False

    def reset(self):
        self.__timestamp: int = 0
        self.__wait_time: int = 0


if __name__ == '__main__':
    wait = NonBlockingWait()
    wait.wait_millis(5000)  # wait for 5 seconds
    while not wait.has_time_passed():
        print('waiting...')
    print('done')
