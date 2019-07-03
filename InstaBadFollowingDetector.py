from InstagramAPI import InstagramAPI

import getpass

from InstagramAPI import InstagramAPI
import time


def Diff(li1, li2):
    return (list(set(li1) - set(li2)))


def getUsernames(flwList):
    res = []
    for flw in flwList:
        res.append(flw['username'])
    return res


def getPKs(flwList):
    res = []

    for flw in flwList:
        res.append(flw['pk'])
    return res


def createFollowingDict(api):
    api.getTotalSelfFollowings()
    flwList = api.LastJson['users']

    res = {}
    for flw in flwList:
        res[flw['pk']] = flw['username']
    return res


def createFollowerDict(api):
    api.getTotalSelfFollowers()
    flwList = api.LastJson['users']

    res = {}
    for flw in flwList:
        res[flw['pk']] = flw['username']
    return res


def getFollowshipUserIdList(flwrList, flwingList, pk=True):
    if pk:
        totalFlwr = getPKs(flwrList)
        totalFlwing = getPKs(flwingList)
        difference = Diff(totalFlwing, totalFlwr)
        return difference
    else:

        totalFlwr = getUsernames(flwrList)
        totalFlwing = getUsernames(flwingList)
        difference = Diff(totalFlwing, totalFlwr)
        return difference


def notFollowBackedFollowers(api, pk=True):
    api.getTotalSelfFollowings()
    followings = api.LastJson['users']
    api.getTotalSelfFollowers()
    followers = api.LastJson['users']
    return getFollowshipUserIdList(followers, followings, pk=pk)


def notFollowBackedFollowings(api, pk=True):
    followings = api.getTotalSelfFollowings()
    followings = api.LastJson['users']
    followers = api.getTotalSelfFollowers()
    followers = api.LastJson['users']
    return getFollowshipUserIdList(followings, followers, pk=pk)


"""

"""

def unfollowList(api, flwList, dict, ask=True):
    i = 0
    for flw in flwList:
        promt = True
        i += 1

        if ask:
            while promt:
                answer = input(f"{i}. are you sure to unfollow {dict[flw]} [y/n]: ")
                if answer == "y" or answer == "\r" or answer == "":
                    promt = False
                    api.unfollow(flw)
                elif answer == "n":
                    promt = False
        else:
            print(f"{i}. 2unfollowing {dict[flw]}...")
            api.unfollow(flw)
            time.sleep(1)


def followList(api, flwList, dict, ask=True):
    for flw in flwList:
        promt = True
        if ask:
            while promt:
                answer = input(f"are you sure to follow {dict[flw]} [y/n]: ")
                if answer == "y":
                    promt = False
                    api.follow(flw)
                elif answer == "n":
                    promt = False
        else:
            print(f"following {dict[flw]}...")
            api.follow(flw)

def UnfollowNotFollowBackedFollowings(api, ask):
    difff1 = notFollowBackedFollowers(api, pk=True)
    d1 = createFollowingDict(api)
    unfollowList(api, difff1, d1, ask=ask)


def CLIRender(api):
    print("choose a command to run")
    print("1. unfollow all of your not follow-backed followings \n"
          "2. show your not follow-backed followings usernames")
    i = input("command number: ")

    if i == "1":
        command = input("Enter 1 to ask before unfollow \nor Enter 2 to unfollow all \n1 or 2: ")
        if command == "1":
            ask = True
        elif command == "2":
            ask = False
        UnfollowNotFollowBackedFollowings(api, ask)
    elif i == "2":
        difff1 = notFollowBackedFollowers(api, pk=True)
        d1 = createFollowingDict(api)
        print(f"accounts to unfollow number is: {len(difff1)} and they are listed below")
        for usr in difff1:
            print (d1[usr])


def main():
    username = input("Enter Username: ")
    # password = input("Enter Password: ")
    password = getpass.getpass(prompt="Enter Password: ")
    api = InstagramAPI(username, password)
    run = api.login()
    print()
    if(run):
        CLIRender(api)
    else:
        print("your input data is in correct")

if __name__ == '__main__':
    main()
