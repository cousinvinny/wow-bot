import sqlite3
from datetime import datetime, timedelta, time
import time

class Database:

    def check_posts_not_posted(self):
        sqlite_connection = sqlite3.connect('/home/vinh/Desktop/wow_discord_bot/sql.db')
        cursor = sqlite_connection.cursor()
        try:
            cursor.execute("SELECT posted FROM Post WHERE posted = 0 ORDER BY datetime DESC")
            result = cursor.fetchall()
            if len(result) > 0:
                return True
            else:
                return False
        except sqlite3.Error as error:
            print('Error occurred in check_for_posts - ', error)
        # Close DB Connection irrespective of success or failure
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def add_posts(self, titles, dates, links):
        sqlite_connection = sqlite3.connect('/home/vinh/Desktop/wow_discord_bot/sql.db')
        cursor = sqlite_connection.cursor()
        try:
            data = []
            for i in range(len(titles)):
                # check if there exists a row with the link
                cursor.execute("SELECT 1 FROM Post WHERE link = '" + links[i] + "'")
                # if the link does not exist, add the row of data to the Post table
                if not cursor.fetchone():
                    data.append((titles[i], links[i], dates[i]))
            if data:
                cursor.executemany('INSERT INTO Post (title, link, datetime) VALUES (?, ?, ?)', data)
                sqlite_connection.commit()

        # Handle errors
        except sqlite3.Error as error:
            print('Error occurred in add_posts - ', error)

        # Close DB Connection irrespective of success or failure
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def add_items(self, post_link, item_names, item_links):
        sqlite_connection = sqlite3.connect('/home/vinh/Desktop/wow_discord_bot/sql.db')
        cursor = sqlite_connection.cursor()
        try:
            data = []
            for i in range(len(item_names)):
                # check if there exists a row with the link
                cursor.execute("SELECT 1 FROM Item WHERE item_link = '" + item_links[i] + "'")
                # if the link does not exist, add the row of data to the Item table
                if not cursor.fetchone():
                    data.append((post_link, item_names[i], item_links[i]))
            cursor.executemany('INSERT INTO Item VALUES(?, ?, ?)', data)
            sqlite_connection.commit()

            # Close the cursor
            cursor.close()

        # Handle errors
        except sqlite3.Error as error:
            print('Error occurred in add_items - ', error)

        # Close DB Connection irrespective of success or failure
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def get_latest_post(self):
        sqlite_connection = sqlite3.connect('/home/vinh/Desktop/wow_discord_bot/sql.db')
        cursor = sqlite_connection.cursor()
        try:
            # check if there exists a row with the link
            cursor.execute("SELECT title, link, datetime FROM Post ORDER BY datetime DESC LIMIT 1")
            post_data = cursor.fetchone()
            post_link = post_data[1]
            cursor.execute("UPDATE Post SET posted = 'True' WHERE link = '" + post_link + "'")
            sqlite_connection.commit()
            cursor.execute("SELECT item_name, item_link FROM Item WHERE post_link = '" + post_link + "'")
            item_data = cursor.fetchall()

            return post_data, item_data

        # Handle errors
        except sqlite3.Error as error:
            print('Error occurred in get_latest_post - ', error)

        # Close DB Connection irrespective of success or failure
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def get_5_latest_post(self):
        sqlite_connection = sqlite3.connect('/home/vinh/Desktop/wow_discord_bot/sql.db')
        cursor = sqlite_connection.cursor()
        try:
            # check if there exists a row with the link
            cursor.execute("SELECT title, link, datetime FROM Post ORDER BY datetime DESC LIMIT 5")
            post_data = cursor.fetchall()
            for i in range(0, 5):
                cursor.execute("UPDATE Post SET posted = 'True' WHERE title = '" + post_data[i][0] + "'")
                sqlite_connection.commit()
            post_links = []
            item_data = []
            for i in range(0, 5):
                post_links.append(post_data[i][1])
                cursor.execute("SELECT item_name, item_link FROM Item WHERE post_link = '" + post_links[i] + "'")
                item_data.append(cursor.fetchall())

            return post_data, item_data

        # Handle errors
        except sqlite3.Error as error:
            print('Error occurred in get_latest_post - ', error)

        # Close DB Connection irrespective of success or failure
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    def get_posts_not_sent(self):
        sqlite_connection = sqlite3.connect('/home/vinh/Desktop/wow_discord_bot/sql.db')
        cursor = sqlite_connection.cursor()
        try:
            # check if there exists a row with the link
            cursor.execute("SELECT title, link, datetime FROM Post WHERE posted = 0 ORDER BY datetime ASC")
            post_data = cursor.fetchall()
            for i in range(0, len(post_data)):
                post_link = post_data[i][1]
                cursor.execute("UPDATE Post SET posted = 'True' WHERE link = '" + post_link + "'")
                sqlite_connection.commit()
            post_links = []
            item_data = []
            for i in range(0, len(post_data)):
                post_links.append(post_data[i][1])
                cursor.execute("SELECT item_name, item_link FROM Item WHERE post_link = '" + post_links[i] + "'")
                item_data.append(cursor.fetchall())

            return post_data, item_data

        # Handle errors
        except sqlite3.Error as error:
            print('Error occurred in get_latest_post - ', error)

        # Close DB Connection irrespective of success or failure
        finally:
            if sqlite_connection:
                sqlite_connection.close()
