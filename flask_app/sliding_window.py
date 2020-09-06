from datetime import datetime, timedelta
import sqlite3
from time import sleep


class Observable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        print(f'Adding observer {observer}')
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observer(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(self, *args, **kwargs)


class Window (Observable):
    """"
    sliding window class
    """

    prev_window = []
    added_data = []
    removed_data = []

    def __init__(self, window_size, db_file, table_name, update_interval):
        super().__init__()
        self.window_size = window_size
        self.update_interval = update_interval
        self.num_of_expiries = 0
        self.content = []
        self.db_file = db_file
        self.table_name = table_name
        self.row_id = 1
        self.slide_interval = 0
        self.time_limit = None
        self.added = []
        self.removed = []

    def connect(self):
        print('Window connecting...')
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.c = self.conn.cursor()
        print('connected!')

    def close(self):
        print('Window closing connection')
        self.conn.close()
        print('closed!')

    def start(self):
        """
        start sliding the window over the database
        """

        global prev_window, added_data, removed_data

        self.connect()

        print(f'sleeping for {self.window_size*60}...')

        sleep(self.window_size*60)

        print('initializing window...')
        self.initialize()

        print('notifying model!')
        self.notify_observer(self.content)

        print(f'sleeping for {self.update_interval * 60}')

        sleep(self.update_interval * 60)

        while self.content != []:

            print('sliding...')

            prev_window = self.content[:]
            self.slide()

            removed_data = self.removed
            added_data = self.added

            print('notifying model!')
            self.notify_observer(removed_data, prev_window, added_data)

            print(f'sleeping for {self.update_interval * 60}')
            sleep(self.update_interval * 60)

        self.close()

    def initialize(self):
        """
        initializes window at the beginning
        """
        row = None

        while not row:
            self.c.execute(
                f'SELECT rowid, * FROM {self.table_name} WHERE rowid == {self.row_id}')
            row = self.c.fetchone()
            if not row:
                print(
                    f'Waiting for {self.update_interval} mins because the DB is empty')
                sleep(self.update_interval * 60)

        time = datetime.strptime(row[1], '%a %b %d %H:%M:%S %z %Y')
        self.time_limit = time + timedelta(minutes=self.window_size)

        while True:
            self.c.execute(
                f'SELECT rowid, * FROM {self.table_name} WHERE rowid == {self.row_id}')
            row = self.c.fetchone()
            self.row_id += 1
            if type(row) is tuple:

                time = datetime.strptime(row[1], '%a %b %d %H:%M:%S %z %Y')

                if time <= self.time_limit:

                    tweet = {}
                    tweet['row_id'], tweet['Time'], tweet['Action_id'], tweet['text'], tweet['Action_Username'], tweet['Causality_id'], tweet[
                        'Causality_Username'], tweet['favourites_count'], tweet['Action_Type'], tweet['verified'], tweet['followers_count'], tweet['coordinates'] = row

                    tweet['Time'] = time
                    self.content.append(tweet)

                else:
                   # Reached time limit
                    break
            else:
                # print(
                #     f'Waiting for {self.update_interval} mins because the DB is empty')
                # sleep(self.update_interval * 60)
                # # Reached end of DB
                # continue
                break

    def slide(self):
        """
        slides the window once
        """

        self.update_time_limit()
        self.remove_expiries()

        while True:
            self.c.execute(
                f'SELECT rowid, * FROM {self.table_name} WHERE rowid == {self.row_id}')
            row = self.c.fetchone()
            self.row_id += 1
            if type(row) is tuple:
                time = datetime.strptime(row[1], '%a %b %d %H:%M:%S %z %Y')

                if time <= self.time_limit:

                    tweet = {}
                    tweet['row_id'], tweet['Time'], tweet['Action_id'], tweet['text'], tweet['Action_Username'], tweet['Causality_id'], tweet[
                        'Causality_Username'], tweet['favourites_count'], tweet['Action_Type'], tweet['verified'], tweet['followers_count'], tweet['coordinates'] = row

                    tweet['Time'] = time
                    self.content.append(tweet)
                    self.added.append(tweet)
                else:
                    # Reached time limit
                    break
            else:
                # Reached end of DB
                break

    def update_time_limit(self):
        """
        updates time limit for the current slide
        """
        self.time_limit += timedelta(minutes=self.update_interval)

    def remove_expiries(self):
        """
        Removes expired data from the window and resets num_of_expiries to 0 for the next window
        """
        self.removed = []
        self.count_expiries()
        for i in range(0, self.num_of_expiries):
            action = self.content.pop(0)
            self.removed.append(action['Action_id'])

        self.num_of_expiries = 0

    def count_expiries(self):
        """
        Counts the number of data that are outside the window's new boundries
        """
        expiry_interval = self.content[0]['Time'] + \
            timedelta(minutes=self.update_interval)
        for tweet in self.content:
            if tweet['Time'] <= expiry_interval:
                self.num_of_expiries += 1
            else:
                break
