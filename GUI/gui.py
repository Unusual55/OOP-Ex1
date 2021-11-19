from tkinter import *
import tkinter
from Building import Building
from Elevator import Elevator
from Call import Call
from Controller import Controller
import json

Buildings = [
    "B1",
    "B2",
    "B3",
    "B4",
    "B5"
]
Cases = [
    "a",
    "b",
    "c",
    "d"
]
# def create_building():
#     floors = building.number_of_floors
#     elevs = building.number_of_elevators
#     for i in range(floors):
#         for j in range(elevs):
#             mat = Entry(window, width = 720/elevs, fg='white', font=('Arial', '16', 'bold'))
#             mat.grid(row=i, column=j)
#     return mat

def set_building(bu):
    b.set(bu)
    print(b.get())
    build = "B".join(bu)
    # bselect.destroy()

def set_case(ca):
    c.set(ca)
    print(c.get())
    case = ca
    # cselect.destroy()




#### main:
window = Tk()
window.title("Elevator simulation")
window.configure(background="black")
window.geometry('700x500')
b = StringVar(window)
b.set("Select the building you want")
c = StringVar(window)
c.set("Select the case you want")
build = None
case = None
bselect = OptionMenu(window,b, "1", "2", "3", "4", "5", command=set_building)
bselect.pack()
cselect = OptionMenu(window, c, "a", "b", "c", "d", command=set_case)
cselect.pack()

path = ['./data/Ex1_input/Ex1_Buildings/']
# filename = "log_"+(build)+("_")+(case)+(".csv")
# build.join(".json")
# json_path = './data/Ex1_input/Ex1_Buildings/'+(build)
# building = Building(Building.parse_from_json(json_path))
# mat = create_building()
#### run
window.mainloop()