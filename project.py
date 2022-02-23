import bs4
import requests
import pandas as pd
import csv

with open ('output.csv',encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)

    count = 0
    link = []
    for row in reader:
        count = count+1

        link.append(row['URL'])

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

imp = []
final_pos_score = []
final_neg_Score= []
final_sub_score =[]
final_avg_sent_len = []
final_pr_cmp_words = []
final_fog_index = []
final_avg_num_of_wrds = []
final_complex_word_count = []
final_word_count = []
final_syl_pr_word = []
final_personal_pro = []
final_avg_word_len = []
for items in link:
    res = requests.get(items, headers=headers)
    soup = bs4.BeautifulSoup(res.content, 'html.parser')
    title = soup.select('title')[0].getText()

    for items in soup.select('p'):
        imp.append(items.text)
    cl = ' '.join(map(str,imp))


    stop_words = set(stopwords.words("english"))

    words = word_tokenize(cl)

    df = pd.read_csv('stop_final.csv')
    slist = open("stop_final.txt","r")
    slist = slist.read().lower()
    slist = slist.split('\n')
    fwords = list(filter(lambda words: words not in slist,words))
    plist = open("Positive_list.txt","r")
    plist = plist.read().lower()
    plist = plist.split('\n')
    #positive score
    pscore = 0
    for items in fwords:
        if items in plist:
            pscore +=1
    nlist = open("Negative_list.txt","r")
    nlist = nlist.read().lower()
    nlist = nlist.split('\n')
    #negative score
    nscore = 0
    for items in fwords:
        if items in nlist:
            nscore -=1
    nscore = nscore*-1
    #POLARITY SCORE
    polscore = (pscore - nscore)/ ((pscore + nscore) + 0.000001)

    #SUBJECTIVITY SCORE
    subscore = (pscore + nscore)/ ((len(fwords)) + 0.000001)

    #Average Sentence Length
    avg_len = len(fwords)/len(sent_tokenize(cl))

    #Percentage of Complex word
    compwords = 0
    for items in fwords:
        vw=0
        if items.endswith(('es','ed')):
            pass
        else:
            for i in fwords:
                if(i=='a' or i=='e' or i=='o' or i=='u'):
                    vw+=1
            if (vw>2):
                compwords +=1


    #Percentage of Complex words
    pr_cmpwords = compwords/len(fwords)
    print("Percentage of Complex words")
    print('%0.2f'%(pr_cmpwords*100),"%")


    #Fog Index
    Fog_Index = 0.4 * (avg_len + pr_cmpwords)

    #Average Number of Words Per Sentence
    Average_Number_of_Words_Per_Sentence  = len(fwords)/len(sent_tokenize(cl))

    #Complex Word Count
    print(compwords)

    #Word Count
    print(len(fwords))

    #Syllable Count Per Word
    compwords = 0
    for items in words:
        vw=0
        if items.endswith(('es','ed')):
            pass
        else:
            for i in words:
                if(i=='a' or i=='e' or i=='o' or i=='u'):
                    vw+=1
            if (vw>2):
                compwords +=1



    #Personal Pronouns
    import re
    regex = r"(\b(i)\b)|(\b(we)\b)|\b(my)\b|(\b(ours)\b)|(\b(us)\b)"
    pp= re.findall(regex,cl)
    len(pp)

    #Average Word Length
    import pandas as pd
    clen = pd.Series(fwords)
    sum = 0
    for i in range(len(clen)):
        sum += clen.str.len()[i]


    avg_word_len = sum /len(fwords)

    final_pos_score = pscore
    final_neg_Score= nscore
    final_sub_score =subscore
    final_avg_sent_len = avg_len
    final_pr_cmp_words = pr_cmpwords
    final_fog_index = Fog_Index
    final_avg_num_of_wrds = Average_Number_of_Words_Per_Sentence
    final_complex_word_count = compwords
    final_word_count = len(fwords)
    final_syl_pr_word = compwords
    final_personal_pro = len(pp)
    final_avg_word_len = avg_word_len


