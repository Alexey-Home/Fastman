import sqlite3 as sq
import re


def get_object(cur, title, obj):
    """Получает из базы данных координаты врагов, обьектов"""
    cur.execute(f"""SELECT {obj} FROM levels WHERE title = {title}""")
    result = cur.fetchone()[0]
    tmp = []
    req = "([0-9.]+)"
    if result:
        result = result.replace(",", ".").split("\n")
        for i in result:
            coordinate = re.compile(req).findall(i)
            tmp.append(tuple([float(c) for c in coordinate]))
    return tmp


def get_rect(cur, title):
    """Возвращает словарь с обьектами rect"""
    cur.execute(f"""SELECT * FROM rect WHERE level = {title}""")
    result = cur.fetchall()
    l_par = ["level", "width", "height", "color", "position"]
    req = "([0-9.]+)"
    rect_all = {}
    for number, i in enumerate(result):
        tmp = {}
        for num, p in enumerate(l_par):
            tmp[p] = i[num]

        coordinate = ([float(j) for j in re.compile(req).findall(tmp["position"])])
        tmp["position"] = (coordinate[0], coordinate[1])
        rect_all[f"rect{number}"] = tmp
    return rect_all


def get_status_level(cur):
    """Получает номер не пройденных уровней"""
    cur.execute(f"""SELECT title FROM levels WHERE status = "0" """)
    number = cur.fetchone()
    return number[0] if number is not None else 1


def get_level_from_db(title=0):
    """Возвращает данные с параметрами уровня."""
    level = {}
    with sq.connect("db.db") as con:
        cur = con.cursor()

    if title != 1:
        title = get_status_level(cur)
        level["title"] = title
    else:
        level["title"] = 1

    l_object = ["button", "bombs", "hedgehods", "start_player", "door", "gun", "add_sec", "time"]

    for obj in l_object:
        level[obj] = get_object(cur, title, obj)
    level["objects_rect"] = get_rect(cur, title)

    return level


def set_status_done(level):
    """Установить флажок уровень пройден"""
    with sq.connect("db.db") as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE levels SET status = 1 WHERE title = {level.title}""")


def repeat_game(level):
    with sq.connect("db.db") as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE levels SET status = 0 WHERE title = {level.title}""")


def new_game():
    """Обнулить все уровни, и начать заново"""
    with sq.connect("db.db") as con:
        cur = con.cursor()
        cur.execute("""UPDATE levels SET status = 0""")
        cur.execute("""UPDATE levels SET status = 1 WHERE title = 1""")


if __name__ == "__main__":
    get_level_from_db()
