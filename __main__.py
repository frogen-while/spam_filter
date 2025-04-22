
import re
import json
def formatting(word):
    if "http" in word or "https" in word or "www" in word:
        return word.replace("http://", "").replace("https://", "").replace("www.", "").split('/')[0]
    word = word.lower()
    word = word.strip('\'"')
    word = re.sub(r'[()\?\!\:\.\>\<\-\'\\d]', '', word)
    return word

def find_spam(massage):
    try:
        with open('bad.json') as f:
            bad_words = json.loads(f.read())
        with open('good.json') as f:
            good_words = json.loads(f.read())
        with open(massage, 'r') as f:
            massage = f.read()
        with open('spammers_domains.json', 'r') as f:
            spammers_domains = json.loads(f.read())

        spam_chances = []
        for word in massage.split():
            word = formatting(word)
            if word in spammers_domains:
                return True
            try:
                spamicity = bad_words.get(word) / (bad_words.get(word) + good_words.get(word))
                spam_chances.append(spamicity)
            except:
                continue
        from math import log, exp

        log_spam_prd = 0
        log_spam_prd2 = 0
        for item in spam_chances:
            log_spam_prd += log(item)
            log_spam_prd2 += log(1 - item)
        score = exp(log_spam_prd) / (exp(log_spam_prd) + exp(log_spam_prd2))
        print(
            f"spam score: {score}")
        if score > 0.8:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return


for i in range(1, 7):
    if find_spam(f"msg{i}.txt"):
        print("It is spam")
    else:
        print("It is not spam")
