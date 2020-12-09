import sqlite3

db = sqlite3.connect("server02.db")
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS settings(
        id INT,
        hints INT,
        last_path TEXT,
        opens INT
    )""")
db.commit()


def change(setting="", params=0):
    sql.execute(f"SELECT id FROM settings WHERE id = '{0}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO settings VALUES (?,?,?,?)", (0, 0, 0, ""))
        db.commit()
    else:
        pass
    if setting == "hints":
        sql.execute(f"UPDATE settings SET hints = {params} WHERE id = '{0}'")
        db.commit()
        pass
    elif setting == "last_path":
        sql.execute(f"UPDATE settings SET last_path = '{params}' WHERE id = '{0}'")
        db.commit()
        pass
    elif setting == "opens":
        sql.execute(f"UPDATE settings SET opens = {params} WHERE id = '{0}'")
        db.commit()
        pass


def get_values():
    return sql.execute(f"SELECT hints FROM settings WHERE id = '{0}'").fetchone()


def get_setting():
    return sql.execute(f"SELECT opens FROM settings WHERE id = '{0}'").fetchone()


def get_path():
    return sql.execute(f"SELECT last_path FROM settings WHERE id = '{0}'").fetchone()


sql.execute("""CREATE TABLE IF NOT EXISTS color(
        id INT,
        RGB TEXT,
        part_of_speech TEXT
    )""")
db.commit()


def start():
    parts = {
        "NOUN": "#900e21", "ADJS": "#1810f7", "ADJF": "#1810f7", "COMP": '#07aff7', "VERB": '#035d10',
        "INFN": '#035d10', "PRTF": '#5d3303', "PRTS": '#5d3303',
        "GRND": '#55007f', "NUMR": '#55557f', "ADVB": '#aa557f', "NPRO": '#00557f', "PRED": '#e76e36',
        "PREP": '#ff007f', "CONJ": '#aaaaff', "PRCL": '#55ff7f', "INTJ": '#aaaa7f'}
    for i, char in enumerate(parts.keys()):
        sql.execute(f"INSERT INTO color VALUES (?,?,?,?)", (i, parts[char], char, 0))
        db.commit()
    for res in parts.keys():
        sql.execute(f"UPDATE color SET RGB = '{parts[res]}' WHERE part_of_speech = '{res}'")
        # print(res, parts[res])
        db.commit()


def set_color(part_of_speech, rgb):
    sql.execute(f"SELECT id FROM color WHERE id = '{0}'")
    if sql.fetchone() is None:
        start()
    try:
        sql.execute(f"UPDATE color SET RGB = '{rgb}' WHERE part_of_speech = '{part_of_speech}'")
        db.commit()

    except BaseException:
        pass


def get_color(part_of_speech):
    try:
        print(part_of_speech)
        return sql.execute(f"SELECT RGB FROM color WHERE part_of_speech = '{part_of_speech}'").fetchone()[0]

    except TypeError:
        start()


if __name__ == '__main__':
    start()
    print(sql.execute(f"SELECT RGB FROM color WHERE part_of_speech = '{'NOUN'}'").fetchone()[0])
