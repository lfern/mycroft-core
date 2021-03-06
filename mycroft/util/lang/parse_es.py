# -*- coding: utf-8 -*-
#
# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
    Parse functions for spanish (es)
    TODO: numbers greater than 999999
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
from mycroft.util.lang.parse_common import is_numeric, look_for_fractions

# Undefined articles ["un", "una", "unos", "unas"] can not be supressed,
# in Spanish, "un caballo" means "a horse" or "one horse".
es_articles = ["el", "la", "los", "las"]

es_numbers = {
    "cero": 0,
    "un": 1,
    "uno": 1,
    "una": 1,
    "primero": 1,
    "primera": 1,
    "primer": 1,
    "dos": 2,
    "segundo": 2,
    "tres": 3,
    "tercero": 3,
    "tercer": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "once": 11,
    "doce": 12,
    "trece": 13,
    "catorce": 14,
    "quince": 15,
    u"dieciséis": 16,
    "diecisiete": 17,
    "dieciocho": 18,
    "diecinueve": 19,
    "veinte": 20,
    "veintiuno": 21,
    "veintidos": 22,
    "veintitres": 23,
    "veinticuatro": 24,
    "veinticinco": 25,
    "veintiseis": 26,
    "veintisiete": 27,
    "veintiocho": 28,
    "veintinueve": 29,
    "treinta": 30,
    "cuarenta": 40,
    "cincuenta": 50,
    "sesenta": 60,
    "setenta": 70,
    "ochenta": 80,
    "noventa": 90,
    "cien": 100,
    "ciento": 100,
    "doscientos": 200,
    "doscientas": 200,
    "trescientos": 300,
    "trescientas": 300,
    "cuatrocientos": 400,
    "cuatrocientas": 400,
    "quinientos": 500,
    "quinientas": 500,
    "seiscientos": 600,
    "seiscientas": 600,
    "setecientos": 700,
    "setecientas": 700,
    "ochocientos": 800,
    "ochocientas": 800,
    "novecientos": 900,
    "novecientas": 900,
    # "mil": 1000,
    u"millón": 1000000}


def isFractional_es(input_str):
    """
    This function takes the given text and checks if it is a fraction.

    Args:
        text (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction

    """
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str) - 1]  # e.g. "fifths"

    # We need to put in order from 1/2 to whichever fraction - here we'd 
    # specified up to 12th
    aFrac = [("medio", "media", "mitad"), ("tercio", "tercera"), ("cuarto", "cuarta"),
             ("quinto", "quinta"), ("sexto", "sexta"), (u"séptimo", u"séptima"),
             ("octavo", "octava"), ("noveno", "novena"), (u"décimo", u"décima"),
             ("onceavo", "onceava", u"undécimo", u"undécima"), ("doceavo", 
              "doceava", u"duodécimo", u"duodécima")]
    # We'll search for the term input_str on all the terms of the array and
    # it will return its index and we'll sum 2 to obtain its real value
    for item in aFrac:
        if input_str in item:
            divisor = aFrac.index(item) + 2
            return 1.0 / divisor
    
    aFracTens = [(u"vigésimo", u"vigésima", "veinteavo", "veinteava"), 
                (u"trigésimo", u"trigésima", "treintavo", "treintava"), 
                (u"cuadragésimo", u"cuadragésima", "cuarentavo", "cuarentava"),
                (u"quincuagésimo", u"quincuagésima", "cincuentavo", "cincuentava"),
                (u"sextagésimo", u"sextagésima", "sesentavo", "sesentava"),
                (u"septagésimo", u"quiseptagésima", "setentavo", "setentava"),
                (u"octagésimo", u"octagésima", "ochentavo", "ochentava"),
                (u"nonagésimo", u"nonagésima", "noventavo", "noventava"),
                ]
    
    for item in aFracTens:
        if input_str in item:
            divisor = aFracTens.index(item) + 2 * 10
            return 1.0 / divisor
    if (input_str == u"centésimo" or input_str == u"centésima"):
        return 1.0 / 100
    if (input_str == u"milésimo" or input_str == u"milésima"):
        return 1.0 / 1000
    return False

def extractnumber_long_es(word):
    """
    Questa funzione converte un numero testuale lungo es.
    ventisette -> 27
    quarantuno -> 41
    nell'equivalente valore intero
     args:
         text (str): la stringa da normalizzare
    Ritorna:
         (int) : il valore del numero estratto usando tutta la parola
         Falso : se la parola non è un numero es."qualcuno"
    """
    result = False
    value = False

    for number in es_numbers.keys():  # ciclo unità
        if word.endswith(number):
            result = True
            value = es_numbers[number]
            word = word[0: len(word) - len(number)]
            break

    if result:  # tolte le unità, dovrebbe rimanere una stringa nota
        if word in es_numbers:
            value += es_numbers[word]
        else:
            value = False  # non è un numero es. qualcuno

    return value


def extractnumber_es(text):
    """
    Questa funzione prepara il testo dato per l'analisi rendendo
    numeri testuali come interi o frazioni.
    In italiano non è un modo abituale ma può essere interessante
    per Mycroft
    E' la versione portoghese riadattata in italiano
     args:
         text (str): la stringa da normalizzare
    Ritorna:
         (int) o (float): il valore del numero estratto

    """
    aWords = text.split()
    count = 0
    result = None
    while count < len(aWords):
        val = 0
        word = aWords[count]
        next_next_word = None
        if count + 1 < len(aWords):
            next_word = aWords[count + 1]
            if count + 2 < len(aWords):
                next_next_word = aWords[count + 2]
        else:
            next_word = None

        # is current word a number?
        if word in es_numbers:
            if word == "mil":
                val = es_numbers[word]
                val = result * val
                result = 0
            else:
                val = es_numbers[word]

        elif word.isdigit():  # doesn't work with decimals
            val = int(word)
        elif is_numeric(word):
            val = float(word)
        elif isFractional_es(word):
            if not result:
                result = 1
            result = result * isFractional_es(word)
            count += 1
            continue

        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            # if (len(aPieces) == 2 and is_numeric(aPieces[0])
            #   and is_numeric(aPieces[1])):
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])

        if not val:
            # cerca numero composto come ventuno ventitre centoventi"
            val = extractnumber_long_es(word)

        if val:
            if result is None:
                result = 0
            # handle fractions
            # if next_word != "avos":
            result += val
            # else:
            #    result = float(result) / float(val)

        if next_word is None:
            break

        # number word and fraction
        ands = ["y"]
        if next_word in ands:
            zeros = 0
            if result is None:
                count += 1
                continue
            newWords = aWords[count + 2:]
            newText = ""
            for word in newWords:
                newText += word + " "

            afterAndVal = extractnumber_es(newText[:-1])
            if afterAndVal:
                if result < afterAndVal or result < 20:
                    while afterAndVal > 1:
                        afterAndVal = afterAndVal / 10.0
                    for word in newWords:
                        if word == "cero" or word == "0":
                            zeros += 1
                        else:
                            break
                for _ in range(0, zeros):
                    afterAndVal = afterAndVal / 10.0
                result += afterAndVal
                break
        elif next_next_word is not None:
            if next_next_word in ands:
                newWords = aWords[count + 3:]
                newText = ""
                for word in newWords:
                    newText += word + " "
                afterAndVal = extractnumber_es(newText[:-1])
                if afterAndVal:
                    if result is None:
                        result = 0
                    result += afterAndVal
                    break

        decimals = ["punto", "coma", ".", ","]
        if next_word in decimals:
            zeros = 0
            newWords = aWords[count + 2:]
            newText = ""
            for word in newWords:
                newText += word + " "
            for word in newWords:
                if word == "cero" or word == "0":
                    zeros += 1
                else:
                    break
            afterDotVal = str(extractnumber_es(newText[:-1]))
            afterDotVal = zeros * "0" + afterDotVal
            result = float(str(result) + "." + afterDotVal)
            break
        count += 1

    if result is None:
        return False

    # Return the $str with the number related words removed
    # (now empty strings, so strlen == 0)
    # aWords = [word for word in aWords if len(word) > 0]
    # text = ' '.join(aWords)
    if "." in str(result):
        integer, dec = str(result).split(".")
        # cast float to int
        if dec == "0":
            result = int(integer)

    return result

def es_number_parse(words, i):
    def es_cte(i, s):
        if i < len(words) and s == words[i]:
            return s, i + 1
        return None

    def es_number_word(i, mi, ma):
        if i < len(words):
            v = es_numbers.get(words[i])
            if v and v >= mi and v <= ma:
                return v, i + 1
        return None

    def es_number_1_99(i):
        r1 = es_number_word(i, 1, 29)
        if r1:
            return r1

        r1 = es_number_word(i, 30, 90)
        if r1:
            v1, i1 = r1
            r2 = es_cte(i1, "y")
            if r2:
                i2 = r2[1]
                r3 = es_number_word(i2, 1, 9)
                if r3:
                    v3, i3 = r3
                    return v1 + v3, i3
            return r1
        return None

    def es_number_1_999(i):
        # [2-9]cientos [1-99]?
        r1 = es_number_word(i, 100, 900)
        if r1:
            v1, i1 = r1
            r2 = es_number_1_99(i1)
            if r2:
                v2, i2 = r2
                return v1 + v2, i2
            else:
                return r1

        # [1-99]
        r1 = es_number_1_99(i)
        if r1:
            return r1

        return None

    def es_number(i):
        # check for cero
        r1 = es_number_word(i, 0, 0)
        if r1:
            return r1

        # check for [1-999] (mil [0-999])?
        r1 = es_number_1_999(i)
        if r1:
            v1, i1 = r1
            r2 = es_cte(i1, "mil")
            if r2:
                i2 = r2[1]
                r3 = es_number_1_999(i2)
                if r3:
                    v3, i3 = r3
                    return v1 * 1000 + v3, i3
                else:
                    return v1 * 1000, i2
            else:
                return r1
        return None

    return es_number(i)

def normalize_es(text, remove_articles):
    """ Spanish string normalization """

    words = text.split()  # this also removed extra spaces

    normalized = ""
    i = 0
    while i < len(words):
        word = words[i]

        if remove_articles and word in es_articles:
            i += 1
            continue

        # Convert numbers into digits
        r = es_number_parse(words, i)
        if r:
            v, i = r
            normalized += " " + str(v)
            continue

        normalized += " " + word
        i += 1

    return normalized[1:]  # strip the initial space

# def extract_datetime_it(string, currentDate=None):
#     def clean_string(s):
#         """
#             cleans the input string of unneeded punctuation and capitalization
#             among other things.
#             Normalize italian plurals
#         """
#         symbols = [".", ",", ";", "?", "!", u"º", u"ª", u"°"]

#         for word in symbols:
#             s = s.replace(word, "")

#         s = s.lower().replace(
#             u"á",
#             "a").replace(
#             u"é",
#             "e'").replace(
#             u"í",
#             "i").replace(
#             u"ó",
#             "o").replace(
#             u"ú",
#             "u").replace(
#             "-",
#             " ").replace(
#             "_",
#             "")

#         noise_words = ["entre", "la", "del", "al", "el", "de",
#                        "le", "per", "alle", "alla", "dai", "delle",
#                        "a", "e'", "era", "questa", "questo", "e"]

#         # normalizza plurali per semplificare analisi
#         s = s.replace(
#             "secondi",
#             "secondo").replace(
#             "minuti",
#             "minuto").replace(
#             "ore",
#             "ora").replace(
#             "giorni",
#             "giorno").replace(
#             "settimane",
#             "settimana").replace(
#             "mesi",
#             "mese").replace(
#             "anni",
#             "anno").replace(
#             "mattino",
#             "mattina").replace(
#             "prossima",
#             "prossimo").replace(
#             "questa",
#             "questo").replace(
#             "quarti",
#             "quarto")

#         wordList = s.split()
#         # print(wordList)  # debug only

#         return wordList

#     def date_found():
#         return found or \
#             (
#                 datestr != "" or timeStr != "" or
#                 yearOffset != 0 or monthOffset != 0 or
#                 dayOffset is True or hrOffset != 0 or
#                 hrAbs != 0 or minOffset != 0 or
#                 minAbs != 0 or secOffset != 0
#             )

#     if string == "":
#         return None
#     if currentDate is None:
#         currentDate = datetime.now()

#     found = False
#     daySpecified = False
#     dayOffset = False
#     monthOffset = 0
#     yearOffset = 0
#     dateNow = currentDate
#     today = dateNow.strftime("%w")
#     currentYear = dateNow.strftime("%Y")
#     fromFlag = False
#     datestr = ""
#     hasYear = False
#     timeQualifier = ""

#     timeQualifiersList = ['mattina', 'pomeriggio', 'sera']
#     markers = ['alle', 'in', 'questo',  'per', 'di']
#     days = ['lunedi', 'martedi', 'mercoledi',
#             'giovedi', 'venerdi', 'sabato', 'domenica']
#     months = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
#               'luglio', 'agosto', 'settembre', 'ottobre', 'novembre',
#               'dicembre']
#     monthsShort = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago',
#                    'set', 'ott', 'nov', 'dic']

#     words = clean_string(string)

#     for idx, word in enumerate(words):
#         if word == "":
#             continue
#         wordPrevPrev = words[idx - 2] if idx > 1 else ""
#         wordPrev = words[idx - 1] if idx > 0 else ""
#         wordNext = words[idx + 1] if idx + 1 < len(words) else ""
#         wordNextNext = words[idx + 2] if idx + 2 < len(words) else ""
#         # wordNextNextNext = words[idx + 3] if idx + 3 < len(words) else ""
#         # possono esistere casi dove servano tre parole di profondità ?
#         start = idx
#         used = 0
#         # save timequalifier for later
#         if word in timeQualifiersList:
#             timeQualifier = word
#             # parse today, tomorrow, day after tomorrow
#         elif word == "oggi" and not fromFlag:
#             dayOffset = 0
#             used += 1
#         elif word == "domani" and not fromFlag:
#             dayOffset = 1
#             used += 1
#         elif word == "ieri" and not fromFlag:
#             dayOffset -= 1
#             used += 1
#         elif word == "dopodomani" and not fromFlag:  # after tomorrow
#             dayOffset += 2
#             used += 1
#         elif word == "dopo" and wordNext == "domani" and \
#                 not fromFlag:
#             dayOffset += 1
#             used += 2
#         elif word == "giorno":
#             if wordPrev[0].isdigit():
#                 dayOffset += int(wordPrev)
#                 start -= 1
#                 used = 2
#                 if wordNext == "dopo" and wordNextNext == "domani":
#                     dayOffset += 1
#                     used += 2
#         elif word == "settimana" and not fromFlag:
#             if wordPrev[0].isdigit():
#                 dayOffset += int(wordPrev) * 7
#                 start -= 1
#                 used = 2
#             elif wordPrev == "prossimo":
#                 dayOffset = 7
#                 start -= 1
#                 used = 2
#             elif wordPrev == "passato":
#                 dayOffset = -7
#                 start -= 1
#                 used = 2
#                 # parse 10 months, next month, last month
#         elif word == "mese" and not fromFlag:
#             if wordPrev[0].isdigit():
#                 monthOffset = int(wordPrev)
#                 start -= 1
#                 used = 2
#             elif wordPrev == "prossimo":
#                 monthOffset = 1
#                 start -= 1
#                 used = 2
#             elif wordPrev == "passato":
#                 monthOffset = -1
#                 start -= 1
#                 used = 2
#                 # parse 5 years, next year, last year
#         elif word == "anno" and not fromFlag:
#             if wordPrev[0].isdigit():
#                 yearOffset = int(wordPrev)
#                 start -= 1
#                 used = 2
#             elif wordPrev == "prossimo":
#                 yearOffset = 1
#                 start -= 1
#                 used = 2
#             elif wordPrev == "passato":
#                 yearOffset = -1
#                 start -= 1
#                 used = 2
#                 # parse Monday, Tuesday, etc., and next Monday,
#                 # last Tuesday, etc.
#         elif word in days and not fromFlag:
#             d = days.index(word)
#             dayOffset = (d + 1) - int(today)
#             used = 1
#             if dayOffset < 0:
#                 dayOffset += 7
#             if wordPrev == "prossimo":
#                 dayOffset += 7
#                 used += 1
#                 start -= 1
#             elif wordPrev == "passato":
#                 dayOffset -= 7
#                 used += 1
#                 start -= 1
#             if wordNext == "prossimo":
#                 # dayOffset += 7
#                 used += 1
#             elif wordNext == "passato":
#                 # dayOffset -= 7
#                 used += 1
#                 # parse 15 of July, June 20th, Feb 18, 19 of February
#         elif word in months or word in monthsShort and not fromFlag:
#             try:
#                 m = months.index(word)
#             except ValueError:
#                 m = monthsShort.index(word)
#             used += 1
#             datestr = months[m]
#             if wordPrev and (wordPrev[0].isdigit()):
#                 datestr += " " + wordPrev
#                 start -= 1
#                 used += 1
#                 if wordNext and wordNext[0].isdigit():
#                     datestr += " " + wordNext
#                     used += 1
#                     hasYear = True
#                 else:
#                     hasYear = False

#             elif wordNext and wordNext[0].isdigit():
#                 datestr += " " + wordNext
#                 used += 1
#                 if wordNextNext and wordNextNext[0].isdigit():
#                     datestr += " " + wordNextNext
#                     used += 1
#                     hasYear = True
#                 else:
#                     hasYear = False
#         # parse 5 days from tomorrow, 10 weeks from next thursday,
#         # 2 months from July
#         validFollowups = days + months + monthsShort
#         validFollowups.append("oggi")
#         validFollowups.append("domani")
#         validFollowups.append("prossimo")
#         validFollowups.append("passato")
#         validFollowups.append("ora")
#         if (word == "da" or word == "dopo") and wordNext in validFollowups:
#             used = 2
#             fromFlag = True
#             if wordNext == "domani":
#                 dayOffset += 1
#             elif wordNext in days:
#                 d = days.index(wordNext)
#                 tmpOffset = (d + 1) - int(today)
#                 used = 2
#                 if tmpOffset < 0:
#                     tmpOffset += 7
#                 dayOffset += tmpOffset
#             elif wordNextNext and wordNextNext in days:
#                 d = days.index(wordNextNext)
#                 tmpOffset = (d + 1) - int(today)
#                 used = 3
#                 if wordNext == "prossimo":
#                     tmpOffset += 7
#                     used += 2  # era 1
#                     start -= 1
#                 elif wordNext == "passato":
#                     tmpOffset -= 7
#                     used += 1
#                     start -= 1
#                 dayOffset += tmpOffset
#         if used > 0:
#             if start - 1 > 0 and words[start - 1] == "questo":
#                 start -= 1
#                 used += 1

#             for i in range(0, used):
#                 words[i + start] = ""

#             if start - 1 >= 0 and words[start - 1] in markers:
#                 words[start - 1] = ""
#             found = True
#             daySpecified = True

#     # parse time
#     timeStr = ""
#     hrOffset = 0
#     minOffset = 0
#     secOffset = 0
#     hrAbs = 0
#     minAbs = 0

#     for idx, word in enumerate(words):
#         if word == "":
#             continue

#         wordPrevPrev = words[idx - 2] if idx > 1 else ""
#         wordPrev = words[idx - 1] if idx > 0 else ""
#         wordNext = words[idx + 1] if idx + 1 < len(words) else ""
#         wordNextNext = words[idx + 2] if idx + 2 < len(words) else ""
#         # wordNextNextNext = words[idx + 3] if idx + 3 < len(words) else ""
#         # TODO verfica se esistono casi dove serva profindita 3 x analisi
#         # parse noon, midnight, morning, afternoon, evening
#         used = 0
#         if word == "mezzogiorno":
#             hrAbs = 12
#             used += 1
#         elif word == "mezzanotte":
#             hrAbs = 24
#             used += 1
#         if word == "mezzo" and wordNext == "giorno":  # if stt splits the word
#             hrAbs = 12
#             used += 2
#         elif word == "mezza"and wordNext == "notte":  # if stt splits the word
#             hrAbs = 24
#             used += 2
#         elif word == "mattina":
#             if hrAbs == 0:
#                 hrAbs = 8
#             used += 1
#             if wordNext and wordNext[0].isdigit():  # mattina alle 5
#                 hrAbs = int(wordNext)
#                 used += 1
#         elif word == "pomeriggio":
#             if hrAbs == 0:
#                 hrAbs = 15
#             used += 1
#             if wordNext and wordNext[0].isdigit():  # pomeriggio alle 5
#                 hrAbs = int(wordNext)
#                 used += 1
#                 if hrAbs < 12:
#                     hrAbs += 12
#         elif word == "sera":
#             if hrAbs == 0:
#                 hrAbs = 19
#             used += 1
#             if wordNext and wordNext[0].isdigit():  # sera alle 8
#                 hrAbs = int(wordNext)
#                 used += 1
#                 if hrAbs < 12:
#                     hrAbs += 12

#         # parse 5:00 am, 12:00 p.m., etc
#         elif word[0].isdigit():
#             isTime = True
#             strHH = ""
#             strMM = ""
#             remainder = ""
#             if ':' in word:
#                 # parse colons
#                 # "3:00 in the morning"
#                 stage = 0
#                 length = len(word)
#                 for i in range(length):
#                     if stage == 0:
#                         if word[i].isdigit():
#                             strHH += word[i]

#                         elif word[i] == ":":
#                             stage = 1
#                         else:
#                             stage = 2
#                             i -= 1
#                     elif stage == 1:
#                         if word[i].isdigit():
#                             strMM += word[i]
#                         else:
#                             stage = 2
#                             i -= 1
#                     elif stage == 2:
#                         remainder = word[i:].replace(".", "")
#                         break

#                 if remainder == "":
#                     nextWord = wordNext.replace(".", "")
#                     if nextWord == "am" or nextWord == "pm":
#                         remainder = nextWord
#                         used += 1
#                     elif nextWord == "sera":
#                         remainder = "pm"
#                         used += 1
#                     elif wordNext == "mattina":
#                         remainder = "am"
#                         used += 1
#                     elif wordNext == "pomeriggio":
#                         remainder = "pm"
#                         used += 1
#                     elif wordNext == "notte":
#                         remainder = "pm"
#                         used += 1
#                     elif wordNext == "di" and wordNextNext == "notte":
#                         if strHH > 5:
#                             remainder = "pm"
#                         else:
#                             remainder = "am"
#                         used += 2
#                     else:
#                         if timeQualifier != "":
#                             if strHH <= 12 and \
#                                     (timeQualifier == "sera" or
#                                      timeQualifier == "pomeriggio"):
#                                 strHH += 12

#             else:
#                 # try to parse # s without colons
#                 # 5 hours, 10 minutes etc.
#                 length = len(word)
#                 strNum = ""
#                 remainder = ""
#                 for i in range(length):
#                     if word[i].isdigit():
#                         strNum += word[i]
#                     else:
#                         remainder += word[i]

#                 if remainder == "":
#                     remainder = wordNext.replace(".", "").lstrip().rstrip()

#                 if (
#                         remainder == "pm" or
#                         wordNext == "pm" or
#                         remainder == "p.m." or
#                         wordNext == "p.m."):
#                     strHH = strNum
#                     remainder = "pm"
#                     used = 1
#                 elif (
#                         remainder == "am" or
#                         wordNext == "am" or
#                         remainder == "a.m." or
#                         wordNext == "a.m."):
#                     strHH = strNum
#                     remainder = "am"
#                     used = 1
#                 else:
#                     if wordNext == "pm" or wordNext == "p.m.":
#                         strHH = strNum
#                         remainder = "pm"
#                         used = 1
#                     elif wordNext == "am" or wordNext == "a.m.":
#                         strHH = strNum
#                         remainder = "am"
#                         used = 1
#                     elif (
#                             int(word) > 100 and
#                             (
#                                 wordPrev == "o" or
#                                 wordPrev == "oh"
#                             )):
#                         # 0800 hours (pronounced oh-eight-hundred)
#                         strHH = int(word) / 100
#                         strMM = int(word) - strHH * 100
#                         if wordNext == "ora":
#                             used += 1

#                     elif (
#                             wordNext == "ora" and
#                             word[0] != '0' and
#                             (
#                                 int(word) < 100 and
#                                 int(word) > 2400
#                             )):
#                         # ignores military time
#                         # "in 3 hours"
#                         hrOffset = int(word)
#                         used = 2
#                         isTime = False
#                         hrAbs = -1
#                         minAbs = -1
#                     elif wordNext == "mattina":
#                         # " 11 del mattina"  -> del viene rimosso
#                         hh = int(word)
#                         used = 2
#                         isTime = False
#                         hrAbs = hh
#                         minAbs = 00
#                     elif wordNext == "pomeriggio":
#                         # " 2 del pomeriggio"  -> del viene rimosso
#                         hh = int(word)
#                         if hh < 12:
#                             hh += 12
#                         used = 2
#                         isTime = False
#                         hrAbs = hh
#                         minAbs = 00
#                     elif wordNext == "sera":
#                         # "alle 8 di sera"  -> alle viene rimosso
#                         hh = int(word)
#                         if hh < 12:
#                             hh += 12
#                         used = 2
#                         isTime = False
#                         hrAbs = hh
#                         minAbs = 00
#                     # parse half an hour : undici e mezza
#                     elif wordNext and wordNext == "mezza":
#                         hrAbs = int(word)
#                         minAbs = 30
#                         used = 2
#                         isTime = False
#                     # parse 1 quarter hour 3 quarters : dieci e tre quarti
#                     elif word and wordNext and \
#                             wordNext == "quarto" and word[0].isdigit():
#                         minAbs = 15 * int(word)
#                         used = 2
#                         if minAbs > 45:  # elimina eventuali errori
#                             minAbs = 0
#                             used -= 2
#                         isTime = False
#                     elif wordNext == "minuto":
#                         # "in 10 minutes"
#                         minOffset = int(word)
#                         used = 2
#                         isTime = False
#                         hrAbs = -1
#                         minAbs = -1
#                     elif wordNext == "secondo":
#                         # in 5 seconds
#                         secOffset = int(word)
#                         used = 2
#                         isTime = False
#                         hrAbs = -1
#                         minAbs = -1
#                     elif int(word) > 100:
#                         strHH = int(word) / 100
#                         strMM = int(word) - strHH * 100
#                         if wordNext == "ora":
#                             used += 1
#                     elif wordNext and wordNext[0].isdigit():
#                         strHH = word
#                         strMM = wordNext
#                         used += 1
#                         if wordNextNext == "ora":
#                             used += 1
#                     elif wordNext == "in" and wordNextNext == "punto":
#                         strHH = word
#                         strMM = 00
#                         used += 2

#                     else:
#                         isTime = False

#             strHH = int(strHH) if strHH else 0
#             strMM = int(strMM) if strMM else 0
#             strHH = strHH + 12 if remainder == "pm" and strHH < 12 else strHH
#             strHH = strHH - 12 if remainder == "am" and strHH >= 12 else strHH
#             if strHH > 24 or strMM > 59:
#                 isTime = False
#                 used = 0
#             if isTime:
#                 hrAbs = strHH * 1
#                 minAbs = strMM * 1
#                 used += 1

#             if hrAbs <= 12 and (timeQualifier == "sera" or
#                                 timeQualifier == "pomeriggio"):
#                 hrAbs += 12

#         if used > 0:
#             # removed parsed words from the sentence
#             for i in range(used):
#                 words[idx + i] = ""

#             if wordPrev == "o" or wordPrev == "oh":
#                 words[words.index(wordPrev)] = ""

#             if wordPrev == "presto":
#                 hrOffset = -1
#                 words[idx - 1] = ""
#                 idx -= 1
#             elif wordPrev == "tardi":
#                 hrOffset = 1
#                 words[idx - 1] = ""
#                 idx -= 1
#             if idx > 0 and wordPrev in markers:
#                 words[idx - 1] = ""
#             if idx > 1 and wordPrevPrev in markers:
#                 words[idx - 2] = ""

#             idx += used - 1
#             found = True

#     # check that we found a date
#     if not date_found:
#         return None

#     if dayOffset is False:
#         dayOffset = 0

#     # perform date manipulation

#     extractedDate = dateNow
#     extractedDate = extractedDate.replace(microsecond=0,
#                                           second=0,
#                                           minute=0,
#                                           hour=0)

#     if datestr != "":
#         en_months = ['january', 'february', 'march', 'april', 'may', 'june',
#                      'july', 'august', 'september', 'october', 'november',
#                      'december']
#         en_monthsShort = ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'july',
#                           'aug',
#                           'sept', 'oct', 'nov', 'dec']
#         for idx, en_month in enumerate(en_months):
#             datestr = datestr.replace(months[idx], en_month)
#         for idx, en_month in enumerate(en_monthsShort):
#             datestr = datestr.replace(monthsShort[idx], en_month)

#         temp = datetime.strptime(datestr, "%B %d")
#         if not hasYear:
#             temp = temp.replace(year=extractedDate.year)
#             if extractedDate < temp:
#                 extractedDate = extractedDate.replace(year=int(currentYear),
#                                                       month=int(
#                                                           temp.strftime(
#                                                               "%m")),
#                                                       day=int(temp.strftime(
#                                                           "%d")))
#             else:
#                 extractedDate = extractedDate.replace(
#                     year=int(currentYear) + 1,
#                     month=int(temp.strftime("%m")),
#                     day=int(temp.strftime("%d")))
#         else:
#             extractedDate = extractedDate.replace(
#                 year=int(temp.strftime("%Y")),
#                 month=int(temp.strftime("%m")),
#                 day=int(temp.strftime("%d")))

#     if timeStr != "":
#         temp = datetime(timeStr)
#         extractedDate = extractedDate.replace(hour=temp.strftime("%H"),
#                                               minute=temp.strftime("%M"),
#                                               second=temp.strftime("%S"))

#     if yearOffset != 0:
#         extractedDate = extractedDate + relativedelta(years=yearOffset)
#     if monthOffset != 0:
#         extractedDate = extractedDate + relativedelta(months=monthOffset)
#     if dayOffset != 0:
#         extractedDate = extractedDate + relativedelta(days=dayOffset)
#     if hrAbs != -1 and minAbs != -1:

#         extractedDate = extractedDate + relativedelta(hours=hrAbs,
#                                                       minutes=minAbs)
#         if (hrAbs != 0 or minAbs != 0) and datestr == "":
#             if not daySpecified and dateNow > extractedDate:
#                 extractedDate = extractedDate + relativedelta(days=1)
#     if hrOffset != 0:
#         extractedDate = extractedDate + relativedelta(hours=hrOffset)
#     if minOffset != 0:
#         extractedDate = extractedDate + relativedelta(minutes=minOffset)
#     if secOffset != 0:
#         extractedDate = extractedDate + relativedelta(seconds=secOffset)
#     for idx, word in enumerate(words):
#         if words[idx] == "e" and words[idx - 1] == "" and words[
#                 idx + 1] == "":
#             words[idx] = ""

#     resultStr = " ".join(words)
#     resultStr = ' '.join(resultStr.split())
#     return [extractedD

def extract_datetime_es(input_str, currentDate=None):
    def clean_string(s):
        # cleans the input string of unneeded punctuation and capitalization
        # among other things
        symbols = [".", ",", ";", "?", "!", u"º", u"ª", u"°"]
        noise_words = ["entre", "la", "del", "al", "el", "de",
                       "por", "para", "una", "cualquier", "a",
                       "esta", "este"]

        for word in symbols:
            s = s.replace(word, "")
        for word in noise_words:
            s = s.replace(" " + word + " ", " ")
        s = s.lower().replace(
            # u"á",
            # "a").replace(
            # u"é",
            # "e").replace(
            #  u"í",
            # "i").replace(
            # u"ó",
            # "o").replace(
            #  u"ú",
            # "u").replace(
            "-",
            " ").replace(
            "_",
            "")
        # handle synonims and equivalents, "tomorrow early = tomorrow morning
        synonims = {u"mañana": ["amanecer", "temprano", "muy temprano"],
                    "tarde": ["media tarde", "atardecer"],
                    "noche": ["anochecer", "tarde"]}
        for syn in synonims:
            for word in synonims[syn]:
                s = s.replace(" " + word + " ", " " + syn + " ")
        # relevant plurals, cant just extract all s in pt
        wordlist = [u"mañanas", "tardes", "noches", u"días", "semanas", u"años",
                    "minutos", "segundos", "las", "los", "siguientes",
                    u"próximas", u"próximos", "horas"]
        for _, word in enumerate(wordlist):
            s = s.replace(word, word.rstrip('s'))
        s = s.replace("meses", "mes").replace("anteriores", "anterior")
        return s

    def date_found():
        return found or \
            (
                datestr != "" or timeStr != "" or
                yearOffset != 0 or monthOffset != 0 or
                dayOffset is True or hrOffset != 0 or
                hrAbs != 0 or minOffset != 0 or
                minAbs != 0 or secOffset != 0
            )

    if input_str == "":
        return None
    if currentDate is None:
        currentDate = datetime.now()

    found = False
    daySpecified = False
    dayOffset = False
    monthOffset = 0
    yearOffset = 0
    dateNow = currentDate
    today = dateNow.strftime("%w")
    currentYear = dateNow.strftime("%Y")
    fromFlag = False
    datestr = ""
    hasYear = False
    timeQualifier = ""

    words = clean_string(input_str).split(" ")
    timeQualifiersList = [u'la mañana', 'tarde', 'noche', u"mediodía"]
    time_indicators = ["en", "la", "al", "por", "pasados",
                       "pasadas", u"día", "hora"]
    days = ['lunes', 'martes', u'miércoles',
            'jueves', 'viernes', u'sábado', 'domingo']
    months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
              'julio', 'agosto', 'septiembre', 'octubre', 'noviembre',
              'diciembre']
    monthsShort = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago',
                   'sep', 'oct', 'nov', 'dic']
    nexts = ["siguiente", u"próximo", u"próxima"]
    suffix_nexts = ["siguientes", "subsecuentes"]
    lasts = [u"último", u"última"]
    suffix_lasts = ["pasada", "pasado", "anterior", "antes"]
    nxts = [u"después", "siguiente", u"próximo", u"próxima"]
    prevs = ["antes", "previa", "previo", "anterior"]
    froms = ["desde", "en", "para", u"después de", "por", u"próximo",
             u"próxima", "de", "partir"]
    thises = ["este", "esta"]
    froms += thises
    lists = nxts + prevs + froms + time_indicators
    for idx, word in enumerate(words):
        if word == "":
            continue
        wordPrevPrev = words[idx - 2] if idx > 1 else ""
        wordPrev = words[idx - 1] if idx > 0 else ""
        wordNext = words[idx + 1] if idx + 1 < len(words) else ""
        wordNextNext = words[idx + 2] if idx + 2 < len(words) else ""
        wordNextNextNext = words[idx + 3] if idx + 3 < len(words) else ""

        start = idx
        used = 0
        # save timequalifier for later
        if word in timeQualifiersList:
            timeQualifier = word

        # parse today, tomorrow, yesterday
        elif word == "hoy" and not fromFlag:
            dayOffset = 0
            used += 1
        elif word == "popopo" and not fromFlag:
            dayOffset = 1
            used += 1
        elif word == "ayer" and not fromFlag:
            dayOffset -= 1
            used += 1
        # "before yesterday" and "before before yesterday"
        elif (word == "anteayer" or
              (word == "ante" and wordNext == "ayer")) and not fromFlag:
            dayOffset -= 2
            used += 1
            if wordNext == "ayer":
                used += 1
        elif word == "ante" and wordNext == "ante" and wordNextNext == \
                "ayer" and not fromFlag:
            dayOffset -= 3
            used += 3
        elif word == "ante anteayer" and not fromFlag:
            dayOffset -= 3
            used += 1
        # day after tomorrow
        elif word == "pasado" and wordNext == u"mañana" and not fromFlag:
            dayOffset += 2
            used = 2
        # day before yesterday
        elif word == "ante" and wordNext == "ayer" and not fromFlag:
            dayOffset -= 2
            used = 2
        # parse 5 days, 10 weeks, last week, next week, week after
        elif word == u"día":
            if wordNext == "pasado" or wordNext == "ante":
                used += 1
                if wordPrev and wordPrev[0].isdigit():
                    dayOffset += int(wordPrev)
                    start -= 1
                    used += 1
            elif (wordPrev and wordPrev[0].isdigit() and
                    wordNext not in months and
                    wordNext not in monthsShort):
                dayOffset += int(wordPrev)
                start -= 1
                used += 2
            elif wordNext and wordNext[0].isdigit() and wordNextNext not in \
                    months and wordNextNext not in monthsShort:
                dayOffset += int(wordNext)
                start -= 1
                used += 2

        elif word == "semana" and not fromFlag:
            if wordPrev[0].isdigit():
                dayOffset += int(wordPrev) * 7
                start -= 1
                used = 2
            for w in nexts:
                if wordPrev == w:
                    dayOffset = 7
                    start -= 1
                    used = 2
            for w in lasts:
                if wordPrev == w:
                    dayOffset = -7
                    start -= 1
                    used = 2
            for w in suffix_nexts:
                if wordNext == w:
                    dayOffset = 7
                    start -= 1
                    used = 2
            for w in suffix_lasts:
                if wordNext == w:
                    dayOffset = -7
                    start -= 1
                    used = 2
        # parse 10 months, next month, last month
        elif word == "mes" and not fromFlag:
            if wordPrev[0].isdigit():
                monthOffset = int(wordPrev)
                start -= 1
                used = 2
            for w in nexts:
                if wordPrev == w:
                    monthOffset = 7
                    start -= 1
                    used = 2
            for w in lasts:
                if wordPrev == w:
                    monthOffset = -7
                    start -= 1
                    used = 2
            for w in suffix_nexts:
                if wordNext == w:
                    monthOffset = 7
                    start -= 1
                    used = 2
            for w in suffix_lasts:
                if wordNext == w:
                    monthOffset = -7
                    start -= 1
                    used = 2
        # parse 5 years, next year, last year
        elif word == u"año" and not fromFlag:
            if wordPrev[0].isdigit():
                yearOffset = int(wordPrev)
                start -= 1
                used = 2
            for w in nexts:
                if wordPrev == w:
                    yearOffset = 7
                    start -= 1
                    used = 2
            for w in lasts:
                if wordPrev == w:
                    yearOffset = -7
                    start -= 1
                    used = 2
            for w in suffix_nexts:
                if wordNext == w:
                    yearOffset = 7
                    start -= 1
                    used = 2
            for w in suffix_lasts:
                if wordNext == w:
                    yearOffset = -7
                    start -= 1
                    used = 2
        # parse Monday, Tuesday, etc., and next Monday,
        # last Tuesday, etc.
        elif word in days and not fromFlag:
            d = days.index(word)
            dayOffset = (d + 1) - int(today)
            used = 1
            if dayOffset < 0:
                dayOffset += 7
            if wordPrev == "siguiente":
                dayOffset += 7
                used += 1
                start -= 1
            elif wordPrev == "pasado":
                dayOffset -= 7
                used += 1
                start -= 1
            if wordNext == "siguiente":
                # dayOffset += 7
                used += 1
            elif wordNext == "pasado":
                # dayOffset -= 7
                used += 1
        # parse 15 of July, June 20th, Feb 18, 19 of February
        elif word in months or word in monthsShort:
            try:
                m = months.index(word)
            except ValueError:
                m = monthsShort.index(word)
            used += 1
            datestr = months[m]
            if wordPrev and wordPrev[0].isdigit():
                # 13 mayo
                datestr += " " + wordPrev
                start -= 1
                used += 1
                if wordNext and wordNext[0].isdigit():
                    datestr += " " + wordNext
                    used += 1
                    hasYear = True
                else:
                    hasYear = False

            elif wordNext and wordNext[0].isdigit():
                # mayo 13
                datestr += " " + wordNext
                used += 1
                if wordNextNext and wordNextNext[0].isdigit():
                    datestr += " " + wordNextNext
                    used += 1
                    hasYear = True
                else:
                    hasYear = False

            elif wordPrevPrev and wordPrevPrev[0].isdigit():
                # 13 dia mayo
                datestr += " " + wordPrevPrev

                start -= 2
                used += 2
                if wordNext and word[0].isdigit():
                    datestr += " " + wordNext
                    used += 1
                    hasYear = True
                else:
                    hasYear = False

            elif wordNextNext and wordNextNext[0].isdigit():
                # mayo dia 13
                datestr += " " + wordNextNext
                used += 2
                if wordNextNextNext and wordNextNextNext[0].isdigit():
                    datestr += " " + wordNextNextNext
                    used += 1
                    hasYear = True
                else:
                    hasYear = False

            if datestr in months:
                datestr = ""

        # parse 5 days from tomorrow, 10 weeks from next thursday,
        # 2 months from July
        validFollowups = days + months + monthsShort
        validFollowups.append("hoy")
        validFollowups.append(u"mañana")
        validFollowups.append("ayer")
        validFollowups.append("anteayer")
        validFollowups.append("ahora")
        validFollowups.append("ya")
        validFollowups.append("ante")

        # TODO debug word "depois" that one is failing for some reason
        if word in froms and wordNext in validFollowups:

            if not (wordNext == u"mañana" and wordNext == "ayer") and not (
                    word == "pasado" or word == "antes"):
                used = 2
                fromFlag = True
            if wordNext == u"mañana" and word != "pasado":
                dayOffset += 1
            elif wordNext == "ayer":
                dayOffset -= 1
            elif wordNext == "anteayer":
                dayOffset -= 2
            elif wordNext == "ante" and wordNextNext == "ayer":
                dayOffset -= 2
            elif (wordNext == "ante" and wordNext == "ante" and
                  wordNextNextNext == "ayer"):
                dayOffset -= 3
            elif wordNext in days:
                d = days.index(wordNext)
                tmpOffset = (d + 1) - int(today)
                used = 2
                # if wordNextNext == "feira":
                #     used += 1
                if tmpOffset < 0:
                    tmpOffset += 7
                if wordNextNext:
                    if wordNextNext in nxts:
                        tmpOffset += 7
                        used += 1
                    elif wordNextNext in prevs:
                        tmpOffset -= 7
                        used += 1
                dayOffset += tmpOffset
            elif wordNextNext and wordNextNext in days:
                d = days.index(wordNextNext)
                tmpOffset = (d + 1) - int(today)
                used = 3
                if wordNextNextNext:
                    if wordNextNextNext in nxts:
                        tmpOffset += 7
                        used += 1
                    elif wordNextNextNext in prevs:
                        tmpOffset -= 7
                        used += 1
                dayOffset += tmpOffset
                # if wordNextNextNext == "feira":
                #     used += 1
        if wordNext in months:
            used -= 1
        if used > 0:

            if start - 1 > 0 and words[start - 1] in lists:
                start -= 1
                used += 1

            for i in range(0, used):
                words[i + start] = ""

            if start - 1 >= 0 and words[start - 1] in lists:
                words[start - 1] = ""
            found = True
            daySpecified = True

    # parse time
    timeStr = ""
    hrOffset = 0
    minOffset = 0
    secOffset = 0
    hrAbs = 0
    minAbs = 0
    # military = False # This has no use in Spanish.

    for idx, word in enumerate(words):
        if word == "":
            continue

        wordPrevPrev = words[idx - 2] if idx > 1 else ""
        wordPrev = words[idx - 1] if idx > 0 else ""
        wordNext = words[idx + 1] if idx + 1 < len(words) else ""
        wordNextNext = words[idx + 2] if idx + 2 < len(words) else ""
        wordNextNextNext = words[idx + 3] if idx + 3 < len(words) else ""
        # parse noon, midnight, morning, afternoon, evening
        used = 0
        if word == "medio" and wordNext == u"día":
            hrAbs = 12
            used += 2
        elif word == "media" and wordNext == "noche":
            hrAbs = 0
            used += 2
        elif word == u"mañana":
            if hrAbs == 0:
                hrAbs = 8
            used += 1
        elif word == "tarde":
            if hrAbs == 0:
                hrAbs = 15
            used += 1
        elif word == "media" and wordNext == "tarde":
            if hrAbs == 0:
                hrAbs = 17
            used += 2
        elif word == "tarde" and wordNext == "noche":
            if hrAbs == 0:
                hrAbs = 20
            used += 2
        elif word == "media" and wordNext == u"mañana":
            if hrAbs == 0:
                hrAbs = 10
            used += 2
        # elif word == "fim" and wordNext == "tarde":
        #     if hrAbs == 0:
        #         hrAbs = 19
        #     used += 2
        # elif word == "fim" and wordNext == "manha":
        #     if hrAbs == 0:
        #         hrAbs = 11
        #     used += 2
        elif word == "madrugada":
            if hrAbs == 0:
                hrAbs = 1
            used += 2
        elif word == "noche":
            if hrAbs == 0:
                hrAbs = 21
            used += 1
        # parse half an hour, quarter hour
        elif word == "hora" and \
                (wordPrev in time_indicators or wordPrevPrev in
                    time_indicators):
            if wordPrev == "media":
                minOffset = 30
            elif wordPrev == "cuarto":
                minOffset = 15
            elif wordPrevPrev == "cuarto":
                minOffset = 15
                if idx > 2 and words[idx - 3] in time_indicators:
                    words[idx - 3] = ""
                words[idx - 2] = ""
            else:
                hrOffset = 1
            if wordPrevPrev in time_indicators:
                words[idx - 2] = ""
            words[idx - 1] = ""
            used += 1
            hrAbs = -1
            minAbs = -1
        # parse 5:00 am, 12:00 p.m., etc
        elif word[0].isdigit():
            isTime = True
            strHH = ""
            strMM = ""
            remainder = ""
            if ':' in word:
                # parse colons
                # "3:00 in the morning"
                stage = 0
                length = len(word)
                for i in range(length):
                    if stage == 0:
                        if word[i].isdigit():
                            strHH += word[i]
                        elif word[i] == ":":
                            stage = 1
                        else:
                            stage = 2
                            i -= 1
                    elif stage == 1:
                        if word[i].isdigit():
                            strMM += word[i]
                        else:
                            stage = 2
                            i -= 1
                    elif stage == 2:
                        remainder = word[i:].replace(".", "")
                        break
                if remainder == "":
                    nextWord = wordNext.replace(".", "")
                    if nextWord == "am" or nextWord == "pm":
                        remainder = nextWord
                        used += 1
                    elif wordNext == u"mañana" or wordNext == "madrugada":
                        remainder = "am"
                        used += 1
                    elif wordNext == "tarde":
                        remainder = "pm"
                        used += 1
                    elif wordNext == "noche":
                        if 0 < int(word[0]) < 6:
                            remainder = "am"
                        else:
                            remainder = "pm"
                        used += 1
                    elif wordNext in thises and wordNextNext == u"mañana":
                        remainder = "am"
                        used = 2
                    elif wordNext in thises and wordNextNext == "tarde":
                        remainder = "pm"
                        used = 2
                    elif wordNext in thises and wordNextNext == "noche":
                        remainder = "pm"
                        used = 2
                    else:
                        if timeQualifier != "":
                            # military = True
                            if strHH <= 12 and \
                                    (timeQualifier == u"la mañana" or
                                     timeQualifier == "tarde"):
                                strHH += 12

            else:
                # try to parse # s without colons
                # 5 hours, 10 minutes etc.
                length = len(word)
                strNum = ""
                remainder = ""
                for i in range(length):
                    if word[i].isdigit():
                        strNum += word[i]
                    else:
                        remainder += word[i]

                if remainder == "":
                    remainder = wordNext.replace(".", "").lstrip().rstrip()

                if (
                        remainder == "pm" or
                        wordNext == "pm" or
                        remainder == "p.m." or
                        wordNext == "p.m."):
                    strHH = strNum
                    remainder = "pm"
                    used = 1
                elif (
                        remainder == "am" or
                        wordNext == "am" or
                        remainder == "a.m." or
                        wordNext == "a.m."):
                    strHH = strNum
                    remainder = "am"
                    used = 1
                else:
                    if (wordNext == "pm" or
                            wordNext == "p.m." or
                            wordNext == "tarde"):
                        strHH = strNum
                        remainder = "pm"
                        used = 1
                    elif (wordNext == "am" or
                          wordNext == "a.m." or
                          wordNext == u"mañana"):
                        strHH = strNum
                        remainder = "am"
                        used = 1
                    elif (int(word) > 100 and
                            (
                                # wordPrev == "o" or
                                # wordPrev == "oh" or
                                wordPrev == "cero"
                            )):
                        # 0800 hours (pronounced oh-eight-hundred)
                        strHH = int(word) / 100
                        strMM = int(word) - strHH * 100
                        # military = True
                        if wordNext == "hora":
                            used += 1
                    elif (
                            wordNext == "hora" and
                            word[0] != '0' and
                            (
                                int(word) < 100 and
                                int(word) > 2400
                            )):
                        # ignores military time
                        # "in 3 hours"
                        hrOffset = int(word)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1

                    elif wordNext == "minuto":
                        # "in 10 minutes"
                        minOffset = int(word)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1
                    elif wordNext == "segundo":
                        # in 5 seconds
                        secOffset = int(word)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1
                    elif int(word) > 100:
                        strHH = int(word) / 100
                        strMM = int(word) - strHH * 100
                        # military = True
                        if wordNext == "hora":
                            used += 1

                    elif wordNext == "" or (
                            wordNext == "en" and wordNextNext == "punto"):
                        strHH = word
                        strMM = 00
                        if wordNext == "en" and wordNextNext == "punto":
                            used += 2
                            if wordNextNextNext == "tarde":
                                remainder = "pm"
                                used += 1
                            elif wordNextNextNext == u"mañana":
                                remainder = "am"
                                used += 1
                            elif wordNextNextNext == "noche":
                                if 0 > strHH > 6:
                                    remainder = "am"
                                else:
                                    remainder = "pm"
                                used += 1

                    elif wordNext[0].isdigit():
                        strHH = word
                        strMM = wordNext
                        # military = True
                        used += 1
                        if wordNextNext == "hora":
                            used += 1
                    else:
                        isTime = False

            strHH = int(strHH) if strHH else 0
            strMM = int(strMM) if strMM else 0
            strHH = strHH + 12 if (remainder == "pm" and
                                   0 < strHH < 12) else strHH
            strHH = strHH - 12 if (remainder == "am" and
                                   0 < strHH >= 12) else strHH
            if strHH > 24 or strMM > 59:
                isTime = False
                used = 0
            if isTime:
                hrAbs = strHH * 1
                minAbs = strMM * 1
                used += 1

        if used > 0:
            # removed parsed words from the sentence
            for i in range(used):
                words[idx + i] = ""

            if wordPrev == "en" or wordPrev == "punto":
                words[words.index(wordPrev)] = ""

            if idx > 0 and wordPrev in time_indicators:
                words[idx - 1] = ""
            if idx > 1 and wordPrevPrev in time_indicators:
                words[idx - 2] = ""

            idx += used - 1
            found = True

    # check that we found a date
    if not date_found:
        return None

    if dayOffset is False:
        dayOffset = 0

    # perform date manipulation

    extractedDate = dateNow
    extractedDate = extractedDate.replace(microsecond=0,
                                          second=0,
                                          minute=0,
                                          hour=0)
    if datestr != "":
        en_months = ['january', 'february', 'march', 'april', 'may', 'june',
                     'july', 'august', 'september', 'october', 'november',
                     'december']
        en_monthsShort = ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'july',
                          'aug',
                          'sept', 'oct', 'nov', 'dec']
        for idx, en_month in enumerate(en_months):
            datestr = datestr.replace(months[idx], en_month)
        for idx, en_month in enumerate(en_monthsShort):
            datestr = datestr.replace(monthsShort[idx], en_month)

        temp = datetime.strptime(datestr, "%B %d")
        if not hasYear:
            temp = temp.replace(year=extractedDate.year)
            if extractedDate < temp:
                extractedDate = extractedDate.replace(year=int(currentYear),
                                                      month=int(
                                                          temp.strftime(
                                                              "%m")),
                                                      day=int(temp.strftime(
                                                          "%d")))
            else:
                extractedDate = extractedDate.replace(
                    year=int(currentYear) + 1,
                    month=int(temp.strftime("%m")),
                    day=int(temp.strftime("%d")))
        else:
            extractedDate = extractedDate.replace(
                year=int(temp.strftime("%Y")),
                month=int(temp.strftime("%m")),
                day=int(temp.strftime("%d")))

    if timeStr != "":
        temp = datetime(timeStr)
        extractedDate = extractedDate.replace(hour=temp.strftime("%H"),
                                              minute=temp.strftime("%M"),
                                              second=temp.strftime("%S"))

    if yearOffset != 0:
        extractedDate = extractedDate + relativedelta(years=yearOffset)
    if monthOffset != 0:
        extractedDate = extractedDate + relativedelta(months=monthOffset)
    if dayOffset != 0:
        extractedDate = extractedDate + relativedelta(days=dayOffset)
    if hrAbs != -1 and minAbs != -1:

        extractedDate = extractedDate + relativedelta(hours=hrAbs,
                                                      minutes=minAbs)
        if (hrAbs != 0 or minAbs != 0) and datestr == "":
            if not daySpecified and dateNow > extractedDate:
                extractedDate = extractedDate + relativedelta(days=1)
    if hrOffset != 0:
        extractedDate = extractedDate + relativedelta(hours=hrOffset)
    if minOffset != 0:
        extractedDate = extractedDate + relativedelta(minutes=minOffset)
    if secOffset != 0:
        extractedDate = extractedDate + relativedelta(seconds=secOffset)

    resultStr = " ".join(words)
    resultStr = ' '.join(resultStr.split())
    # resultStr = pt_pruning(resultStr)
    return [extractedDate, resultStr]


def get_gender_es(word, raw_string=""):
    # Next rules are imprecise and incompleted, but is a good starting point.
    # For more detailed explanation, see
    # http://www.wikilengua.org/index.php/Género_gramatical
    word = word.rstrip("s")
    gender = False
    words = raw_string.split(" ")
    for idx, w in enumerate(words):
        if w == word and idx != 0:
            previous = words[idx - 1]
            gender = get_gender_es(previous)
            break
    if not gender:
        if word[-1] == "a":
            gender = "f"
        if word[-1] == "o" or word[-1] == "e":
            gender = "m"
    return gender
