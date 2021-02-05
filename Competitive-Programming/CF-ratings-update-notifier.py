# Fails if you've never given a rated contest before.

"""
    Codeforces Ratings Update Notifier.

    Checks your contest count on your contests page every 5 minutes,
    and sends you an email if the count has increased, i.e., ratings
    have been updated.

    Asks for the handle to track, and the email address and password
    of the account with which you would like to send an email. Also
    asks for the email address of the account in which you would like
    to receive the update notification email. Even if both are same,
    you have to enter it once again.

    It shall fail to work if you have no previous contests in your
    contests page. This too is trivial to fix, but I'm feeling lazy
    right now.
    
    Has been working well till now. Let me know if you encounter
    any bugs :)
"""

import requests
import schedule
import smtplib
import time
from bs4 import BeautifulSoup


def getContestCount(url):
    while True:
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            return int(soup.find('div', {"class": "datatable"}).find('td').text.strip())

        except:
            time.sleep(60)
            continue


def getUrl(handle):
    return "https://codeforces.com/contests/with/" + handle


def checkIfUpdated():
    global URL, prev
    updated = getContestCount(URL)
    global flag
    if updated > prev:
        prev = updated
        flag = True


def sendMail(author, passwd, recipient, subject, message):
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()

    mail.login(author, passwd)
    mail.sendmail(author, recipient, "Subject: " + subject + "\n\n" + message)
    mail.quit()


username = str(input("Please enter your handle:\n"))
mailFrom = str(input("Please enter your gmail address:\n"))
p = str(input("Please enter your password:\n"))
mailTo = str(input("Please enter the recipient gmail address:\n"))

URL = getUrl(username)
prev = getContestCount(URL)

sendMail(mailFrom, p, mailTo, "Start Successful",
         "MailerBot has started. Current count: " + str(prev))

flag = False
schedule.every(5).minutes.do(checkIfUpdated)

while True:
    schedule.run_pending()
    if flag:
        sendMail(mailFrom, p, mailTo, "Ratings Updated!",
                 "Hey " + username + ",\n\nYour ratings have been updated!")
        flag = False

    time.sleep(60)
