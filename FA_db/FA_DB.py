import sqlite3

def ins_usr(DB, user):
    try:
        DB.execute(f'''INSERT INTO USERS
            (NAME,FOLDERS,GALLERY,SCRAPS,FAVORITES,EXTRAS)
            VALUES ("{user}", "", "", "", "", "")''')
        DB.commit()
    except sqlite3.IntegrityError:
        pass
    except:
        raise

def ins_sub(DB, infos):
    try:
        DB.execute(f'''INSERT INTO SUBMISSIONS
            (ID,AUTHOR,AUTHORURL,TITLE,UDATE,TAGS,FILELINK,FILENAME,LOCATION)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', infos)
        DB.commit()
    except sqlite3.IntegrityError:
        pass
    except:
        raise

def usr_up(DB, user, to_add, column):
    col = DB.execute(f"SELECT {column} FROM users WHERE name = '{user}'")
    col = col.fetchall()[0]
    col = "".join(col).split(',')
    if to_add in col: return 1
    if col[0] == '':
        col = [to_add]
    else:
        col.append(to_add)
    col.sort(key=str.lower)
    col = ",".join(col)
    DB.execute(f"UPDATE users SET {column} = '{col}' WHERE name = '{user}'")
    DB.commit()

def usr_rep(DB, user, find, replace, column):
    col = DB.execute(f"SELECT {column} FROM users WHERE name = '{user}'")
    col = col.fetchall()[0]
    col = "".join(col).split(',')
    if replace in col:
        return 1
    elif col[0] == '':
        col = [replace]
    elif find not in col:
        col.append(replace)
    else:
        col = [e.replace(find, replace) for e in col]
    col.sort(key=str.lower)
    col = ",".join(col)
    DB.execute(f"UPDATE users SET {column} = '{col}' WHERE name = '{user}'")
    DB.commit()

def usr_src(DB, user, find, column):
    col = DB.execute(f"SELECT {column} FROM users WHERE name = '{user}'")
    col = col.fetchall()[0]
    col = "".join(col).split(',')
    if find in col: return True
    else: return False

def sub_read(DB, ID, column):
    col = DB.execute(f"SELECT {column} FROM submissions WHERE id = '{ID}'")
    col = col.fetchall()[0]
    return col[0]

def sub_search(DB, terms):
    return DB.execute('''SELECT author, udate, title FROM submissions
        WHERE id LIKE ? AND
        authorurl LIKE ? AND
        title LIKE ? AND
        tags REGEXP ?
        ORDER BY authorurl ASC, id ASC''', terms)

def sub_exists(DB, ID):
    exists = DB.execute(f'SELECT EXISTS(SELECT id FROM submissions WHERE id = "{ID}" LIMIT 1);')
    return exists.fetchall()[0][0]

def mktable(DB, table):
    if table == 'submissions':
        DB.execute('''CREATE TABLE IF NOT EXISTS SUBMISSIONS
            (ID INT UNIQUE PRIMARY KEY NOT NULL,
            AUTHOR TEXT NOT NULL,
            AUTHORURL TEXT NOT NULL,
            TITLE TEXT,
            UDATE CHAR(10) NOT NULL,
            TAGS TEXT,
            FILELINK TEXT,
            FILENAME TEXT,
            LOCATION TEXT NOT NULL);''')
    elif table == 'users':
        DB.execute('''CREATE TABLE IF NOT EXISTS USERS
            (NAME TEXT UNIQUE PRIMARY KEY NOT NULL,
            FOLDERS CHAR(4) NOT NULL,
            GALLERY TEXT,
            SCRAPS TEXT,
            FAVORITES TEXT,
            EXTRAS TEXT);''')
