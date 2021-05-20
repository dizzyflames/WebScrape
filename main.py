import requests
import os
import re

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Find nth occurrence of a substring within a string if found
# returns -1 otherwise
# parameters string and substring are both strings
# n is an int
def findOccurrence(string, substring, n):
    val = -1
    for i in range(0, n):
        val = string.find(substring, val + 1)
    return val


# will take a large string and cuts it and returns only the part in between substring 1 and substring 2
# the occurrence parameter is to further specify where the substring is located.
# occurrences are ints all other parameters are strings
def cutString(string, substring1, occurrence1, substring2, occurrence2):
    start = findOccurrence(string, substring1, occurrence1)
    end = findOccurrence(string, substring2, occurrence2)

    return string[start:end]


# Accepts a directory as a string.
# Returns the name of all files contained within as an array.
def getFileNames(dir):
    filenames = []
    for filename in os.listdir(dir):
        filenames.append(filename)

    return filenames


def sortByNum(e):
    return int(e.split(".")[0])

def sortedFolderFiles(dir):
    filenames = getFileNames(dir)
    f = []
    filenames.sort(key=sortByNum)
    for fName in filenames:
        start = findOccurrence(fName, ".", 1)
        end = findOccurrence(fName, ".", 2)
        f.append(fName[start + 1: end])
    return f

# scraping tarot meanings here https://www.tarotcardmeanings.net/waite-tarot-comments/
# will use file names to create urls to scrap from
# accepts nothing and returns nothing
# used for major arcana with different layout
def getMajorArcana():
    f = sortedFolderFiles("cards")

    # all major arcanas
    f = f[:22]
    urlString = []
    for name in f:
        if name.find("The") != -1:
            urlString.append(name.replace("The ", ""))
        else:
            urlString.append(name)
    i = 0
    for a in urlString:

        res = requests.get("https://www.tarotcardmeanings.net/waite-tarot-comments/waite-on-tarot-" + a.lower().replace(" ", "") + ".htm")

        # cuts the string to only have card meaning
        s = cutString(res.text, "</H3>", 3, "<BR>", 10)
        s = s[7:-4]

        # remove the html text
        x = findOccurrence(s, "<", 1)
        y = findOccurrence(s, "/B", 1)

        # writes the text to a text file
        with open("meanings/" + str(i) + "." + f[i] + ".txt", "w") as file:
            file.write(s[:x] + "\n\n" + s[y + 4:])
        i += 1

# 22 - 35 wands
# 36 - 49 pentacles
# 50 - 64 cups
# 65 - 78 swords
# accepts nothing and returns nothing
# scrapes the meaning of the minor arcana cards from a website
def getMinorArcana():
    wands = "https://www.tarotcardmeanings.net/waite-tarot-comments/waite-on-tarot-wands.htm"
    pentacles = "https://www.tarotcardmeanings.net/waite-tarot-comments/waite-on-tarot-pentacles.htm"
    cups = "https://www.tarotcardmeanings.net/waite-tarot-comments/waite-on-tarot-cups.htm"
    swords = "https://www.tarotcardmeanings.net/waite-tarot-comments/waite-on-tarot-swords.htm"
    files = sortedFolderFiles("cards")

    res = requests.get(wands)
    k = 1
    pattern = r'\<.*?\>.*?\<\/.*?\>'
    for i in range(22, 78):
        if i == 36:
            res = requests.get(pentacles)
            k = 1
        elif i == 50:
            res = requests.get(cups)
            k = 1
        elif i == 64:
            res = requests.get(swords)
            k = 1

        with open("meanings/" + str(i) + "." + files[i] + ".txt", "w") as file:
            output = res.text[findOccurrence(res.text, "Divinatory Meanings", k):findOccurrence(res.text,"<A HREF", k + 9)]
            output = output[33:]
            output = re.sub(pattern, '', output)
            output = re.sub('\<.*?\>', '', output)
            output = output.replace("\n\n\n", "\n\n")
            output = output.replace("\n ", "\n")
            output = output.rstrip()
            file.write(output)
            k += 1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    getMajorArcana()
    getMinorArcana()
