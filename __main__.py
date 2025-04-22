import re
import json
import math
def formatting(word, urls):
    urls+=1
    if "http" in word or "https" in word or "www" in word:
        urls+=1
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

        urls = 0
        spamicities = []
        for word in massage.split():
            try:
                word = formatting(word, urls)
                if word in spammers_domains:
                    return True
                try:
                    bad_words_chances = bad_words.get(word, 0.001)
                    good_words_chances = good_words.get(word, 0.001)
                    spamicity = math.log(bad_words_chances / (good_words_chances + bad_words_chances))
                    spamicities.append(spamicity)
                except KeyError:
                    continue
                    
            except KeyError as e:
                print(f"KeyError: {e}")
                continue
        prd_spamicity_bad = 1
        prd_spamicity_good = 1
        for spamicity in spamicities:
            if spamicity == 0:
                continue
            if spamicity < 0:
                continue
            prd_spamicity_bad *= spamicity
        for spamicity in spamicities:
            if spamicity == 0:
                continue
            if spamicity > 0:
                continue
            prd_spamicity_good *= (1-spamicity)
        
        score = (prd_spamicity_bad / (prd_spamicity_bad + prd_spamicity_good)) 

        if urls > 0:
            score += 0.5
        else:
            score = 0
        
        return score
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return False
                


if __name__ == "__main__":
    for i in range(1, 7):
        if find_spam(f"msg{i}.txt"):
            print(find_spam(f"msg{i}.txt"))
            print("It is spam")
        else:
            print(find_spam(f"msg{i}.txt"))
            print("It is not spam")
