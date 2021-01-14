import twitchlive_notify


def main():
    twitchlive_notify.config()
    twitchlive_notify.get_lock()
    twitchlive_notify.main()
