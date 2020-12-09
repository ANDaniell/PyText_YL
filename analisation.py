import logging

import pymorphy2
import sys
from chardet.universaldetector import UniversalDetector
from SQLite_back import get_color



def analis_morph(text):
    morph = pymorphy2.MorphAnalyzer()
    a = text.lower().split(" ")
    nouns = {}
    adjectives = {}
    comp = {}  # компаратив (лучше, получше, выше)
    verbs = {}
    prichastia = {}
    deeprichastia = {}
    numbers = {}  # числительные
    adverbs = {}  # наречия
    pronouns = {}  # местоимение
    preds = {}  # предактив (некогда)
    preps = {}  # предлог
    conjunctions = {}  # союзы
    particles = {}  # частицы
    interjections = {}  # междометия
    if len(a) > 1:
        for num, i in enumerate(a):
            morph.parse(word=i)
            res = morph.parse(i)[0]

            # print(morph.parse(word=i))
            # print(res.tag.POS)

            part_of_speech = (num, i, res.tag.POS)
            if part_of_speech[2] == "NOUN":
                nouns[part_of_speech[1]] = part_of_speech[0]
                # прилагательные в краткой и полной форме
            elif part_of_speech[2] == "ADJS":
                adjectives[part_of_speech[1]] = part_of_speech[0]
            elif part_of_speech[2] == "ADJF":
                adjectives[part_of_speech[1]] = part_of_speech[0]
                # компаратив
            elif part_of_speech[2] == "COMP":
                comp[part_of_speech[1]] = part_of_speech[0]
                # глагол + инфинитив
            elif part_of_speech[2] == "VERB":
                verbs[part_of_speech[1]] = part_of_speech[0]
            elif part_of_speech[2] == "INFN":
                verbs[part_of_speech[1]] = part_of_speech[0]
                # краткое и полное причастие
            elif part_of_speech[2] == "PRTF":
                prichastia[part_of_speech[1]] = part_of_speech[0]
            elif part_of_speech[2] == "PRTS":
                prichastia[part_of_speech[1]] = part_of_speech[0]
                # деепричатие
            elif part_of_speech[2] == "GRND":
                deeprichastia[part_of_speech[1]] = part_of_speech[0]
                # числительные
            elif part_of_speech[2] == "NUMR":
                numbers[part_of_speech[1]] = part_of_speech[0]
                # наречия
            elif part_of_speech[2] == "ADVB":
                adverbs[part_of_speech[1]] = part_of_speech[0]
                # местоимения
            elif part_of_speech[2] == "NPRO":
                pronouns[part_of_speech[1]] = part_of_speech[0]
                # предактив
            elif part_of_speech[2] == "PRED":
                preds[part_of_speech[1]] = part_of_speech[0]
                # предлог
            elif part_of_speech[2] == "PREP":
                preps[part_of_speech[1]] = part_of_speech[0]
                # союз
            elif part_of_speech[2] == "CONJ":
                conjunctions[part_of_speech[1]] = part_of_speech[0]
                # частица
            elif part_of_speech[2] == "PRCL":
                particles[part_of_speech[1]] = part_of_speech[0]
                # междометия
            elif part_of_speech[2] == "INTJ":
                interjections[part_of_speech[1]] = part_of_speech[0]
        return nouns, adjectives, comp, verbs, prichastia, deeprichastia, numbers, adverbs, pronouns, preds, preps, conjunctions, particles, interjections

    elif len(a) == 1:
        something = "!@#$%^&*()-_+=:?.,<>/~`№{}[]"
        word_red = a[0]
        for i in something:
            # print(i, end=" ")
            word_red = word_red.replace(i, "")

        res = morph.parse(word_red)[0].tag.POS
        # print(word_red, res)
        if res == "NOUN":
            color = "#900e21"  # красный
            # прилагательные в краткой и полной форме
        elif res == "ADJS" or res == "ADJF":
            color = "#1810f7"  # синий
            # компаратив
        elif res == "COMP":
            color = "#07aff7"  # голубой
            # глагол + инфинитив
        elif res == "VERB":
            color = "#035d10"  # тёмно зелёный
        elif res == "INFN":
            color = "#035d10"
            # краткое и полное причастие
        elif res == "PRTF":
            color = "#5d3303"  # коричневый
        elif res == "PRTS":
            color = "#5d3303"
            # деепричатие
        elif res == "GRND":
            color = "#55007f"  # фиолетовый
            # числительные
        elif res == "NUMR":
            color = "#55557f"  # серый какой-то
            # наречия
        elif res == "ADVB":
            color = "#aa557f"  # кораловый
            # местоимения
        elif res == "NPRO":
            color = "#00557f"  # очёнь тёмно бюрюзовый
            # предактив
        elif res == "PRED":
            color = "#e76e36"  # оранжевый
            # предлог
        elif res == "PREP":
            color = "#ff007f"  # розовый
            # союз
        elif res == "CONJ":
            color = "#aaaaff"  # сиреневый
            # частица
        elif res == "PRCL":
            color = "#55ff7f"  # салатовый
            # междометия
        elif res == "INTJ":
            color = "#aaaa7f"  # песочный
        else:
            color = "#000000"
        return color
    else:
        return "#55ff7f"


def analis_encoding(path):
    try:
        detector = UniversalDetector()
        with open(path, 'rb') as fh:
            for line in fh:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
        return detector.result.get("encoding")
    except Exception as exc:
        logging.debug(f"{exc}")
        return None
        pass


def new_analis(text):
    morph = pymorphy2.MorphAnalyzer()
    a = text.lower().split(" ")
    if len(a) == 1:
        something = "!@#$%^&*()-_+=:?.,<>/~`№{}[]"
        word_red = a[0]
        for i in something:
            # print(i, end=" ")
            word_red = word_red.replace(i, "")

        res = morph.parse(word_red)[0].tag.POS
        print(res)
        color = get_color(res)
        return color


if __name__ == '__main__':
    a = analis_morph("Таким")
