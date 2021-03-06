#!/usr/bin/env python
"""This module performs simple password tasks

Keyword arguments:
A -- apple
"""
# Copyright 2015 Austin Fox
# Program is distributed under the terms of the
# GNU General Public License see ./License for more information.

import sys
import time
import bcrypt


# Password Stuff
def getDigest(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())


def isPassword(password, digest):
    return bcrypt.hashpw(password, digest) == digest


def Addusr(name, pass1, pass2, advisor, email):
    test = passtest(pass1, pass2)
    if test is True:
        if advisor == "":
            return "Please provide Advisor."
        hashed = getDigest(pass1)
        tim = time.strftime("%y-%m-%d-%H:%M")  # lastlogin
        with open("data/Pass.txt", "r") as data_file:
            for row in data_file:
                data = row.split("\t")
                if name == data[0]:
                    return "User Name Exists. <br> Please select another."
        with open("data/Pass.txt", "a") as out_file:
            out_file.write("%s\t%s\t%s\tindex\t%s\t%s\t\n" %
                           (name, hashed, advisor, tim, email))
            return "Success!<br>%s Added as new user!!" % name
    else:
        return test


def userup(userdata):
    with open("data/Pass.txt", "a") as out_file:
            userdata = '\t'.join(userdata)
            out_file.write(userdata)
            return "Success!"


def changepass(name, oldpass, pass1, pass2):  # this is not right yet
    check = checkpass(name, oldpass)
    if check is True or check[0:2] == "No":
        test = passtest(pass1, pass2)
        if test is True:
            hashed = getDigest(pass1)
            userdata = getuserdata(name)
            userdata[1] = hashed
            userup(userdata)
            return "Success!<br>%s password changed!" % name
        else:
            return test
    else:
        return check


def getallusers():
    allusers = []
    with open("data/Pass.txt") as data_file:
        for row in data_file:
            userdat = row.split("\t")
            allusers.append(userdat[0])
    allusers.sort()
    # print allusers
    return allusers


def getuserdata(name, remove=True):
    # print "name:", name
    with open("data/Pass.txt", "r") as f:
        data_file = f.readlines()
        userdata = []
    with open("data/Pass.txt", "w") as out_file:
        for row in data_file:
            data = row.split("\t")
            if name == data[0]:
                userdata = data
                # print userdata
                if not remove:
                    out_file.write(row)
            else:
                out_file.write(row)
    return userdata


def passtest(pass1, pass2):
    if pass1 == pass2:
        if len(pass1) >= 6:
            return True
        else:
            return "Password must be atlest 6 characters long."
    else:
        return "Passwords are not equal!"


def checkpass(name, pass1):  # Check Password
    with open("data/Pass.txt") as data_file:
        for row in data_file:
            data = row.split("\t")
            if name == data[0]:
                userdata = data
                # print userdat[1]
                if userdata[1] == "":
                    return "No Password is set.<br>Please change password"\
                           " leaving old password BLANK.<br>"\
                           "-> Menu -> Change Password"
                if isPassword(pass1, userdata[1]):
                    # print "You Got It!!"
                    return True
                else:
                    return "Password is incorrect.<br>Please try again.<br>"\
                            "If you cannot remember your password please "\
                            "contact the administrator."
        else:
            return "No such user"

if __name__ == "__main__":
    print Addusr("Admin", "Password", "Password", "Glob", "email")
    print Addusr("Joe", "123456", "123456", "Glob", "email")
    while True:
        name = raw_input('User Name:')
        pass1 = raw_input('Password:')
        print checkpass(name, pass1)
        if name == 'quit':
            break
    print checkpass("Joe", "123456")
