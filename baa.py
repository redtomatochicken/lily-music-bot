alpha_list = "abcdefghijklmnopqrstuvwxyz"

def convert(word:str):
    out = ""
    for c in word:
        temp = "ba"
        #print(f"letter {c}")
        if c in alpha_list:
            for i in range(alpha_list.index(c)):
                temp+="a"
            
            out+=" " +temp
        else:
            out+=c

    #while (out.find("aaaaa") != -1):
    out = out.replace("aaaaa","​ba")
    #    print(out)
    
    return " "+out

def convert2(word:str):
    out = word.replace("​ba","aaaaa")
    #print(out)
    
    i = out.count("a")
    #print(i)
    if i == 0:
        return " "
    
    out2 = alpha_list[i-1]
    return " " +out2

def convertSentence(sentence:str,dir=False):
    words = sentence.lower().strip().split(" ")
    out = ""
    for word in words:
        if not dir:
            out += convert(word)
        else:
            out += convert2(word)
    return out.strip()