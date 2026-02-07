import sqlite3

import developer_mode

DEVELOPER_MODE = developer_mode.state()


def add_data(ki,val):
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        cur.execute(f"INSERT INTO mappings VALUES (?,?)", (ki,val),)
        con.commit()
        return "Operation Completed Sucessfully", 2000
    except sqlite3.IntegrityError:
        return "Duplicate shareableKey -- Try again", 3001
    except Exception as E:
        if not DEVELOPER_MODE:
            return "Unknown Error", 3002
        else:
            return f"Unknown Error -- {E}", 3002
    finally:
        cur.close()
        con.close()

def remove_data(ki):
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        cur.execute(f"DELETE FROM mappings WHERE shareablekey = ?", (ki,))
        con.commit()
        return "Operation Completed Sucessfully", 2000
    except Exception as E:
        if not DEVELOPER_MODE:
            return "Unknown Error", 3003
        else:
            return f"Unknown Error -- {E}", 3003
    finally:
        cur.close()
        con.close()

def get_val(ki):
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        res = cur.execute("SELECT HashedOTP FROM mappings WHERE shareableKey = ?", (ki,))
        val = res.fetchone()
        if val == None:
            return "Invalid/Missing shareableKey", 3011
        val = val[0]
        return val, 2000
    except Exception as E:
        if not DEVELOPER_MODE:
            return "Unknown Error", 3004
        else:
            return f"Unknown Error -- {E}", 3004
    finally:
        cur.close()
        con.close()

def list_data():
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        res = cur.execute("SELECT * FROM mappings")
        list = res.fetchall()
        return list, 2000
    except Exception as E:
        if not DEVELOPER_MODE:
            return "Unknown Error", 3005
        else:
            return f"Unknown Error -- {E}", 3005
    finally:
        cur.close()
        con.close()

def add_blocklist(kix,tries):
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        cur.execute("INSERT INTO blocklist VALUES (?,?)", (kix,tries))
        con.commit()
        return "Operation Completed Sucessfully", 2000
    except Exception as e:
        if not DEVELOPER_MODE:
            return "Unknown Error", 3006
        return f"Unknown Error - {e}", 3006
    finally:
        cur.close()
        con.close()
    
def modify_blocklist(kix):
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        resp = cur.execute("SELECT tries FROM blocklist WHERE shareableKey = ?", (kix,))
        tries = resp.fetchone()[0]
        tries = tries + 1
        cur.execute("UPDATE blocklist SET tries = ? WHERE shareableKey = ?", (tries,kix,))
        con.commit()
        return "Operation Completed Sucessfully", 2000
    except Exception as e:
        if not DEVELOPER_MODE:
            return "Unknown Error", 3007
        return f"Unknown Error - {e}", 3007
    
    finally:
        cur.close()
        con.close()
    

def should_be_blocked(kix):
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        resp = cur.execute("SELECT tries FROM blocklist WHERE shareableKey = ?", (kix,))
        tries = resp.fetchone()[0]
        if tries > 3:
            return True
        else:
            return False
    except Exception as e:
        return "err"
    
    finally:
        cur.close()
        con.close()
    
def remove_blocklist(kix):
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        cur.execute("DELETE FROM blocklist WHERE shareableKey = ?", (kix,))
        con.commit()
        return "Operation Completed Sucessfully", 2000
    except Exception as e:
        if not DEVELOPER_MODE:
            return "Unknown Error", 3008
        return f"Unknown Error - {e}", 3008
    
    finally:
        cur.close()
        con.close()


def register_secretKey(secretKey,smtp_host,smtp_port,smtp_mail,smtp_password):
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        cur.execute("INSERT INTO auth VALUES (?,?,?,?,?)", (secretKey,smtp_host,smtp_port,smtp_mail,smtp_password,))
        con.commit()
        return "Operation Completed Sucessfully", 2000
    except sqlite3.IntegrityError:
        return "secretKey already exists", 3009
    except Exception as e:
        if not DEVELOPER_MODE:
            return "Unknown Error", 3010
        else:
            return f"Unknown Error - {e}", 3010
    finally:
        cur.close()
        con.close()
    
def getfrom_secretKey(secretKey):
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        resp = cur.execute("SELECT * FROM auth WHERE secretKey = ?", (secretKey,))
        resp = resp.fetchone()
        return resp, 2000
    except Exception as e:
        if not DEVELOPER_MODE:
            return "Unknown error", 3022
        else:
            return f"Unknown error - {e}", 3022
    finally:
        cur.close()
        con.close()
        
def remove_secretKey(secretKey):
    try:
        con = sqlite3.connect("map.db")
        cur = con.cursor()
        cur.execute("DELETE FROM auth WHERE secretKey = ?", (secretKey,))
        con.commit()
        return "Operation Completed Sucessfully", 2000
    except Exception as e:
        if not DEVELOPER_MODE:
            return "Unknown Error", 3023
        else:
            return f"Unknown Error - {e}", 3023
    finally:
        cur.close()
        con.close()
        
