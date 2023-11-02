import re
import sqlite3
import tkinter as tk
import datetime

def list_dela(selectname):
    selectname = selectname.split(';')[0]
    conn = sqlite3.connect('urist.db')
    cursor = conn.cursor()
    cursor.execute('select * from clients where name = ?', (selectname,))
    client_id = cursor.fetchone()[0]
    cursor.execute('select * from dela where id_client = ?', (client_id,))
    dela_listbox.delete(0, tk.END)
    list_dela = cursor.fetchall()
    for d in list_dela:
        s = ''.join(d[1])
        dela_listbox.insert(tk.END, '№ '+str(s) + '    ' + str(d[3]) + ";    " + str(d[4]))
    conn.close()
def add_client():
    name = entry_name.get()
    phone = entry_phone.get()
    if name and phone:
        conn = sqlite3.connect('urist.db')
        cursor = conn.cursor()
        cursor.execute('insert into clients (name, phone) values (?, ?)', (name, phone))
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        conn.commit()
        conn.close()
        updateclient()
    #entry_name.insert(0, '')
    #entry_phone.insert(0, '')


def updateclient():
    listbox_client.delete(0, tk.END)
    conn = sqlite3.connect('urist.db')
    cursor = conn.cursor()
    cursor.execute('select * from clients')
    clients = cursor.fetchall()
    for client in clients:

        s = ''.join(client[1])+';     '+''.join(client[2])
        listbox_client.insert(tk.END, s)
    conn.close()


def updatedela(client_name):
    #listbox_client.delete(0, tk.END)
    conn = sqlite3.connect('urist.db')
    cursor = conn.cursor()

    cursor.execute('select * from clients where name=?', (client_name,))
    client_id = cursor.fetchone()[0]
    cursor.execute('select * from dela where id_client=?', (client_id,))
    dela_listbox.delete(0, tk.END)
    list_dela = cursor.fetchall()
    for d in list_dela:
        print(d)
        s = ''.join(d[1])
        dela_listbox.insert(tk.END, str(s) + ' - '+str(d[3]) + " - " + str(d[4]))
    conn.close()
def add_delo():
    client = listbox_client.get(listbox_client.curselection())
    selectname = client.split(';')[0]
    number_dela = frame_dela_entry_name.get()


    if client and number_dela:

        conn = sqlite3.connect('urist.db')
        cursor = conn.cursor()
        #print(selectname)
        cursor.execute('select * from clients where name = ?', (selectname,))
        #print(cursor.fetchone()[0])

        client_id = cursor.fetchone()[0]

        date_res = frame_dela_date_1.get() + '.'+frame_dela_date_2.get() + '.' + frame_dela_date_3.get()
        time_res = frame_dela_date_4.get() + ':' + frame_dela_date_5.get()
        cursor.execute('insert into dela (number, id_client, datecreate, timecreate) values (?, ?, ?, ?)', (number_dela, client_id,date_res,time_res,))
        frame_dela_entry_name.delete(0, tk.END)
        frame_dela_date_1.delete(0, tk.END)
        frame_dela_date_2.delete(0, tk.END)
        frame_dela_date_3.delete(0, tk.END)
        frame_dela_date_4.delete(0, tk.END)
        frame_dela_date_5.delete(0, tk.END)
        conn.commit()
        conn.close()
        updatedela(selectname)


conn = sqlite3.connect('urist.db')
cursor = conn.cursor()
cursor.execute('''
create table if not exists clients (
id integer primary key,
name text,
phone text
)
''')
cursor.execute('''
create table if not exists dela (
id integer primary key,
number text,
id_client integer,
datecreate text,
timecreate text,
foreign key (id_client) references clients (id)
)
''')

cursor.execute('''
create table if not exists documents (
id integer primary key,
name text,
id_dela integer,
foreign key (id_dela) references dela (id)
)
''')


root = tk.Tk()
root.title('Программа для юристов')


frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=10, pady=10)
label_name = tk.Label(frame, text='Имя клиента')
label_name.grid(row=0, column=0)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)
label_phone = tk.Label(frame, text='Телефон клиента')
label_phone.grid(row=1, column=0)
entry_phone = tk.Entry(frame)
entry_phone.grid(row=1, column=1)
button_client = tk.Button(frame, text='Добавить клиента', command=add_client)
button_client.grid(row=2, columnspan=2)



frame_clients = tk.Frame(root)
frame_clients.pack(side=tk.LEFT, padx=10, pady=10)
label_client = tk.Label(frame_clients, text='Список клиентов')
label_client.pack()

listbox_client = tk.Listbox(frame_clients, selectmode=tk.SINGLE, width=40)
listbox_client.pack()

listbox_client.bind('<<ListboxSelect>>', lambda e: list_dela(listbox_client.get(listbox_client.curselection())))


frame_dela = tk.Frame(root)
frame_dela.pack(side=tk.LEFT, padx=10, pady=10)
frame_dela_label = tk.Label(frame_dela, text='Судебные дела')
frame_dela_label.pack()
dela_listbox = tk.Listbox(frame_dela, selectmode=tk.SINGLE, width=50)
dela_listbox.pack()

frame_add_dela = tk.Frame(root)
frame_add_dela.pack(side=tk.LEFT, padx=10, pady=10)

frame_dela_name = tk.Label(frame_add_dela, text='№')
frame_dela_name.grid(row=0, columnspan=1)
frame_dela_entry_name = tk.Entry(frame_add_dela, width=4)
frame_dela_entry_name.grid(row=0, columnspan=10)



frame_dela_name_l = tk.Label(frame_add_dela, text='Дата')
frame_dela_name_l.grid(row=1, column=0)
#start date
frame_dela_date_1 = tk.Entry(frame_add_dela, width=2)
frame_dela_date_1.grid(row=1, column=1)
frame_dela_date_2 = tk.Entry(frame_add_dela, width=2)
frame_dela_date_2.grid(row=1, column=2)
frame_dela_date_3 = tk.Entry(frame_add_dela, width=4)
frame_dela_date_3.grid(row=1, column=3)
#end date


frame_dela_name_l1 = tk.Label(frame_add_dela, text='Время')
frame_dela_name_l1.grid(row=2, column=0)
#start time
frame_dela_date_4 = tk.Entry(frame_add_dela, width=2)
frame_dela_date_4.grid(row=2, column=1)
frame_dela_date_5 = tk.Entry(frame_add_dela, width=2)
frame_dela_date_5.grid(row=2, column=2)
#end time


frame_dela_button = tk.Button(frame_add_dela, text='Добавить', command=add_delo)
frame_dela_button.grid(row=3, columnspan=4)

updateclient()
root.mainloop()