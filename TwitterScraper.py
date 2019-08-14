import csv
import string
# FIRST SEARCH MUST BE ONE WORD SECOND CAN HAVE MULTIPLE BUT ONLY COMMA SEPARATION NO SPACES

wordfreq = {}
count = 0
with open('TweetStreamMed.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # store amount of tweets per hour
    tweetfreq = {}
    for row in reader:
        timestamp = row[2]
        timestamp = timestamp[:-2] + "00"
        if timestamp not in tweetfreq:
            tweetfreq[timestamp] = 0
        tweetfreq[timestamp] += 1
    csvfile.seek(0)
    for row in reader:
        count += 1
        content = row[6]
        time = row[2]
        # take the hour
        time = time[:-2] + "00"
        timestamp = time
        date = row[1]
        # tokenize
        content = content.split()
        # normalize case
        content = [word.lower() for word in content]
        # remove punctuation
        table = str.maketrans('', '', string.punctuation)
        content = [word.translate(table) for word in content]
        # remove stopwords
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('english'))
        content = [w for w in content if not w in stop_words]
        #store wordcount
        grams = [x + ' ' + y + ' ' + z for x, y, z in zip(content[:-2], content[1:-1], content[2:])]
        grams += [x + ' ' + y for x, y in zip(content[:-1], content[1:])]
        grams += content
        for word in grams:
            if word not in wordfreq:
                wordfreq[word] = {}
            if date not in wordfreq[word]:
                wordfreq[word][date] = {}
            if time not in wordfreq[word][date]:
                wordfreq[word][date][time] = 0
            wordfreq[word][date][time] = float((wordfreq[word][date][time] * tweetfreq[timestamp]) + 1) / tweetfreq[timestamp]
        if count == 12001:
            findword = input("What word would you like to search for?")
            while findword not in wordfreq:
                findword = input("Word not found. Try again")
            findword = findword.split(',')
            for word in findword:
                print(wordfreq[word])
            while findword != 'q':
                findword = input("What word would you like to search for?")
                findword = findword.split(',')
                for word in findword:
                    print(wordfreq[word])
