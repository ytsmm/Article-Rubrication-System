import math


def getKeywords(vocabulary, keywords, labels, n):
    texts = []
    for i in range(n):
        text = []
        for j in range(len(labels)):
            if labels[j] == i:
                text.extend(keywords[j])
        texts.append(text)
    result = []
    terms = []
    for text in texts:
        for word in text:
            if word not in terms:
                terms.append(word)
    for text in texts:
        textRes = []
        for t in terms:
            textRes.append(tfidf(t, text, texts))
        result.append(textRes)
    maxes = []
    weights = []
    for i in result:
        t = terms.copy()
        line = i.copy()
        kw, weight = top(t, line, vocabulary)
        maxes.append(kw)
        weights.append(weight)
    while True:
        words = []
        for m in maxes:
            for word in m:
                words.append(word)  # все ключевые слова
        dup = [x for i, x in enumerate(words) if i != words.index(x)]
        dup = list(set(dup))
        y = 0
        for d in dup:
            y = 1
            ind = terms.index(d.lower())
            for k in range(len(result)):
                result[k].pop(ind)
            terms.remove(d.lower())
        if y == 1:
            maxes = []
            weights = []
            for i in result:
                line = i.copy()
                w = terms.copy()
                kw, weight = top(w, line, vocabulary)
                maxes.append(kw)
                weights.append(weight)
        else:
            break
    return maxes, weights


def top(words, line, vocabulary):
    maxTerms = []
    weights = []
    while len(maxTerms) < 10:
        maxValue = max(line)
        term = words[line.index(maxValue)]
        if term not in maxTerms:
            maxTerms.append(vocabulary[term])
            weights.append(maxValue)
        line.remove(maxValue)
        words.remove(term)
    return maxTerms, weights


def tfidf(word, sentence, docs):
    tf = sentence.count(word) / len(sentence)
    idf = math.log1p(len(docs) / sum([1 for doc in docs if word in doc]))
    return tf * idf
