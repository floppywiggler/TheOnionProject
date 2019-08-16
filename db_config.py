import sqlite3
conn = sqlite3.connect('onion.db')

def create_db():

    c = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE onionsites
                 (URL, Title , Status, Status_code, last_checked)''')
    # Insert a row of data
    c.execute("INSERT INTO onionsites VALUES ('tuu66yxvrnn3of7l.onion','UK Guns and Ammo Store - Buy guns and ammo in the UK for Bitcoin.','OK','200')")
    # Save (commit) the changes
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

