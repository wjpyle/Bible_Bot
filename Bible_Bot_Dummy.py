import praw

def bibleBot():
    # Create the praw object
    bot = praw.Reddit(user_agent = '', client_id = '',
                      client_secret = '',
                      username = '', password = '')

    #Create the subreddit object
    subreddit = bot.subreddit('') #This is my test subreddit

    #Create the comments object
    comments = subreddit.stream.comments()
    
    for comment in comments:
        text = comment.body
        split_text = text.split()
        split_length = len(split_text)
        author = comment.author
        (name,urlname,chapnum) = findName(text,comment)

        if name != "" and ('kingjamesbibleonline' not in text.lower()):
        # If a Bible chapter/verse has been referenced and the comment is not
        # one that this bot has already made

            n = 0
            while (n < split_length) and (split_text[n].lower() != name):
                #Find the chapter name in the comment
                n = n + 1

            if (n + 2) <= split_length:
                #If the name is referenced at the end of the comment, there is
                #no room for a chapter or verse number so the code stops running.
                #If that is not the case, the code focuses in on the string right
                #after the name and names it possnum.
                possnum = split_text[n + 1]

                if possnum[0].isdigit(): #If the string segment right after the
                    #name is a number
                    if name != "psalms": #psalms is the only book with a
                        #three-digit number of chapters, so we make it a special
                        #case.
                        if len(possnum) > 2  and possnum[1].isdigit() and possnum[2].isdigit():
                            #If the length of the possible number is greater than 2 and the second
                            #and third places in the number are digits, then the commenter
                            #must be referencing a chapter that doesn't exist since no book has
                            #a three-digit number of chapters (except for psalms, which we
                            #filtered out earlier).
                            num = 10000
                        elif (len(possnum) == 1) or (len(possnum) >= 2 and not possnum[1].isdigit()):
                            #If the possible number only has one digit or if it is longer but
                            #the second place in the possible number is not a digit (i.e. a colon
                            #or period), then the first digit is considered the full chapter number
                            num = int(possnum[0])
                        elif len(possnum) >= 2 and possnum[1].isdigit():
                            #If the possible number is longer and the second place is a digit, then
                            #the first and second places are considered the full chapter number.
                            num = int(possnum[0]) * 10 + int(possnum[1])
                    elif name == "psalms": #psalms is a special case since it has over 100 chapters
                        if len(possnum) > 3 and possnum[1].isdigit() and possnum[2].isdigit() and possnum[3].isdigit():
                            #If the first four places of possnum are numbers, then the commenter mentioned
                            #a chapter that doesn't exist
                            num = 10000
                        elif (len(possnum) == 1) or (len(possnum)) >= 2 and not possnum[1].isdigit():
                            #If the length of possnum is one or if the length is longer and the second
                            #place is not a digit, then only the first place is considered the chapter
                            #number
                            num = int(possnum[0])
                        elif len(possnum) >= 2 and possnum[1].isdigit() and not possnum[2].isdigit():
                            #If the length of possnum is longer and the first and second places are digits
                            #but not the third, then the first two places are considered the chapter number.
                            num = int(possnum[0] * 10 + int(possnum[1]))
                        elif len(possnum) >= 2 and possnum[1].isdigit() and possnum[2].isdigit():
                            #If the length is longer and the first, second, and third places are digits
                            #then the first three places are considered the chapter number.
                            num = int(possnum[0]) * 100 + int(possnum[1]) * 10 + int(possnum[2])
                                      
                                      
                           
                        """else if len(possnum) > 2 and not possnum[1].isdigit():
                        if len(possnum) > 2 and possnum[1].isdigit() and not (possnum[2].isdigit()):
                            num = int(possnum[0]) * 10 + int(possnum[1])
                        elif len (possnum) not (possnum[1].isdigit()):
                            num = int(possnum[0])
                            
        """ 
                    if num <= chapnum:
                        #If the found number is less than or equal to the number of chapters in the mentioned verse,
                        #the chapter is assumed to exist.
                        #Here, we form the final URL to be posted.
                        message = "Hi! It looks like you included a Bible or Torah chapter in your comment. Here is a link to that chapter as it is written in the King James Bible:   " + ("https://www.kingjamesbibleonline.org/" + urlname +
                        "-chapter-" + str(num)).format(author)

                        #Reply to the comment
                        comment.reply(message)
                        
                        #Print to see when we reply
                        print("success!")

def findName(text,comment):

    #Iterate through all comments

    name = ""
   
    #Create a list of all the words in the comment so we can iterate by word
    #instead of by character
    split_text = text.split()

    split_length = len(split_text)

    #This part is long and tedious but I can't think of any better way to do it.
    #It searches for the name of every Bible verse in the given comment. Perhaps
    #I could create a list of the names and search the comment for elements of
    #the list? But the way I have it here I can specify the number of chapters
    #in each Bible verse, which will be needed later.
    
    if 'genesis' in text.lower():
        name = 'genesis'
        #The "name" variable is used later to pinpoint the area we need to examine
        #in the comment. The "urlname" is the name that will be used to construct
        #the final url. In most cases, they are identical
        urlname = 'genesis'
        chapnum = 50
        
    elif 'exodus' in text.lower():
        name = 'exodus'
        urlname = 'exodus'
        chapnum = 40
        
    elif 'leviticus' in text.lower():
        name = 'leviticus'
        urlname = 'leviticus'
        chapnum = 27
        
    elif 'numbers' in text.lower():
        name = 'numbers'
        urlname = 'numbers'
        chapnum = 36
        
    elif 'deuteronomy' in text.lower():
        name = 'deuteronomy'
        urlname = 'deuteronomy'
        chapnum = 34
        
    elif 'joshua' in text.lower():
        name = 'joshua'
        urlname = 'joshua'
        chapnum = 24
        
    elif 'judges' in text.lower():
        name = 'judges'
        urlname = 'judges'
        chapnum = 21
        
    elif 'ruth' in text.lower():
        name = 'ruth'
        urlname = 'ruth'
        chapnum = 4
        
    elif ' samuel ' in text.lower() and split_text[0].lower() != 'samuel':
        #Here we encounter our first instance of a pair of Bible verses
        #that have the same name and are differentiated by a number. Here,
        #for example, we deal with two verses respectively called 1 Samuel
        #and 2 Samuel.
        #The same method shown here for determining which chapter the commenter
        #is referencing is also used later on in the code for other chapters
        #that are split into multiple numbered sections.
        i = 0
        while split_text[i].lower() != 'samuel':
            i = i + 1
        i = i - 1
        if split_text[i] == "1": # If the comment refers to 1 Samuel
            name = 'samuel'
            urlname = '1-samuel'
            chapnum = 31
        elif split_text[i] == "2": # If the comment refers to 2 Samuel
            name = 'samuel'
            urlname = '2-samuel'
            chapnum = 24

    elif ' kings ' in text.lower() and split_text[0].lower() != 'kings':
        i = 0
        while split_text[i].lower() != 'kings':
            i = i + 1
        i = i - 1
        if split_text[i] == "1":
            name = 'kings'
            urlname = '1-kings'
            chapnum = 22
        elif split_text[i] == "2":
            name = 'kings'
            urlname = '2-kings'
            chapnum = 25

    elif ' chronicles ' in text.lower() and split_text[0].lower() != 'chronicles':
        i = 0
        while split_text[i].lower() != 'chronicles':
            i = i + 1
        i = i - 1
        if split_text[i] == "1":
            name = 'chronicles'
            urlname = '1-chronicles'
            chapnum = 29
        elif split_text[i] == "2":
            name = 'chronicles'
            urlname = '2-chronicles'
            chapnum = 36

    elif 'ezra' in text.lower():
        name = 'ezra'
        urlname = 'ezra'
        chapnum = 10
        
    elif 'nehemiah' in text.lower():
        name = 'nehemiah'
        urlname = 'nehemiah'
        chapnum = 13
        
    elif 'esther' in text.lower():
        name = 'esther'
        urlname = 'esther'
        chapnum = 10
        
    elif 'job' in text.lower():
        name = 'job'
        urlname = 'job'
        chapnum = 42
        
    elif 'psalms' in text.lower():
        name = 'psalms'
        urlname = 'psalms'
        chapnum = 150
        
    elif 'proverbs' in text.lower():
        name = 'proverbs'
        urlname = 'proverbs'
        chapnum = 31
        
    elif 'ecclesiastes' in text.lower():
        name = 'ecclesiastes'
        urlname = 'ecclesiastes'
        chapnum = 12
        
    elif 'solomon' in text.lower():
        name = 'solomon'
        urlname = 'song-of-solomon'
        chapnum = 8
        
    elif 'isaiah' in text.lower():
        name = 'isaiah'
        urlname = 'isaiah'
        chapnum = 66
        
    elif 'jeremiah' in text.lower():
        name = 'jeremiah'
        urlname = 'jeremiah'
        chapnum = 52
        
    elif 'lamentations' in text.lower():
        name = 'lamentations'
        urlname = 'lamentations'
        chapnum = 5
        
    elif 'ezekiel' in text.lower():
        name = 'ezekiel'
        urlname = 'ezekiel'
        chapnum = 48
        
    elif 'daniel' in text.lower():
        name = 'daniel'
        urlname = 'daniel'
        chapnum = 12
        
    elif 'hosea' in text.lower():
        name = 'hosea'
        urlname = 'hosea'
        chapnum = 14
        
    elif 'joel' in text.lower():
        name = 'joel'
        urlname = 'joel'
        chapnum = 3
        
    elif 'amos' in text.lower():
        name = 'amos'
        urlname = 'amos'
        chapnum = 9
        
    elif 'obadiah' in text.lower():
        name = 'obadiah'
        urlname = 'obadiah'
        chapnum = 1
        
    elif 'jonah' in text.lower():
        name = 'jonah'
        urlname = 'jonah'
        chapnum = 4
        
    elif 'micah' in text.lower():
        name = 'micah'
        urlname = 'micah'
        chapnum = 7
        
    elif 'nahum' in text.lower():
        name = 'nahum'
        urlname = 'nahum'
        chapnum = 3
        
    elif 'habakkuk' in text.lower():
        name = 'habakkuk'
        urlname = 'habbakkuk'
        chapnum = 3
        
    elif 'zephaniah' in text.lower():
        name = 'zephaniah'
        urlname = 'zephaniah'
        chapnum = 3
        
    elif 'haggai' in text.lower():
        name = 'haggai'
        urlname = 'haggai'
        chapnum = 2
        
    elif 'zechariah' in text.lower():
        name = 'zechariah'
        urlname = 'zechariah'
        chapnum = 14
        
    elif 'malachi' in text.lower():
        name = 'malachi'
        urlname = 'malachi'
        chapnum = 4
        
    elif 'matthew' in text.lower():
        name = 'matthew'
        urlname = 'matthew'
        chapnum = 28
        
    elif 'mark' in text.lower():
        name = 'mark'
        urlname = 'mark'
        chapnum = 16
        
    elif 'luke' in text.lower():
        name = 'luke'
        urlname = 'luke'
        chapnum = 24
        
        
    elif 'acts' in text.lower():
        name = 'acts'
        urlname = 'acts'
        chapnum = 28
        
    elif 'romans' in text.lower():
        name = 'romans'
        urlname = 'romans'
        chapnum = 16


    elif ' corinthians ' in text.lower() and split_text[0].lower() != 'corinthians':
        i = 0
        while split_text[i].lower() != 'corinthians':
            i = i + 1
        i = i - 1
        if split_text[i] == "1":
            name = 'corinthians'
            urlname = '1-corinthians'
            chapnum = 16
        elif split_text[i] == "2":
            name = 'corinthians'
            urlname = '2-corinthians'
            chapnum = 13

    elif 'galatians' in text.lower():
        name = 'galatians'
        urlname = 'galatians'
        chapnum = 6
        
    elif 'ephesians' in text.lower():
        name = 'ephesians'
        urlname = 'ephesians'
        chapnum = 6
        
    elif 'philippians' in text.lower():
        name = 'philippians'
        urlname = 'philippians'
        chapnum = 4
        
    elif 'colossians' in text.lower():
        name = 'colossians'
        urlname = 'colossians'
        chapnum = 4

    elif ' thessalonians ' in text.lower() and split_text[0].lower() != 'thessalonians':
        i = 0
        while split_text[i].lower() != 'thessalonians':
            i = i + 1
        i = i - 1
        if split_text[i] == "1":
            name = 'thessalonians'
            urlname = '1-thessalonians'
            chapnum = 5
        elif split_text[i] == "2":
            name = 'thessalonians'
            urlname = '2-thessalonians'
            chapnum = 3

    elif ' timothy ' in text.lower() and split_text[0].lower() != 'timothy':
        i = 0
        while split_text[i].lower() != 'timothy':
            i = i + 1
        i = i - 1
        if split_text[i] == "1":
            name = 'timothy'
            urlname = '1-timothy'
            chapnum = 6
        elif split_text[i] == "2":
            name = 'timothy'
            urlname = '2-timothy'
            chapnum = 4

    elif 'titus' in text.lower():
        name = 'titus'
        urlname = 'titus'
        chapnum = 3
        
    elif 'philemon' in text.lower():
        name = 'philemon'
        urlname = 'philemon'
        chapnum = 1
        
    elif 'hebrews' in text.lower():
        name = 'hebrews'
        urlname = 'hebrews'
        chapnum = 13

    elif 'james' in text.lower():
        name = 'james'
        urlname = 'james'
        chapnum = 5

    elif ' peter ' in text.lower() and split_text[0].lower() != 'peter':
        i = 0
        while split_text[i].lower() != 'peter':
            i = i + 1
        i = i - 1
        if split_text[i] == "1":
            name = 'peter'
            urlname = '1-peter'
            chapnum = 5
        elif split_text[i] == "2":
            name = 'peter'
            urlname = '2-peter'
            chapnum = 3

    elif ' john ' in text.lower() and split_text[0].lower() != 'john':
        print "one"
        i = 0
        while split_text[i].lower() != 'john':
            i = i + 1
        i = i - 1
        if split_text[i] == "1":
            name = 'john'
            urlname = '1-john'
            chapnum = 5
        elif split_text[i] == "2":
            print "yes"
            name = 'john'
            urlname = '2-john'
            chapnum = 1
        elif split_text[i] == "3":
            name = 'john'
            urlname = '3-john'
            chapnum = 1
        else:
            name = 'john'
            urlname = 'john'
            chapnum = 21

    elif split_text[0].lower() == 'john':
        name = 'john'
        urlname = 'john'
        chapnum = 21
        

    elif 'jude' in text.lower():
        name = 'jude'
        urlname = 'jude'
        chapnum = 1

    elif 'revelation' in text.lower():
        name = 'revelation'
        urlname = 'revelation'
        chapnum = 22

    return (name,urlname,chapnum)
