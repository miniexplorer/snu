from typing import List
import typer
from syncapicalls import *
from asyncapicalls import *
from rich import print
import json
from rich.console import Console
from rich.table import Table

console = Console()

app = typer.Typer()

def qtys2list(argument: str) -> list:
    d = {}

    for line in argument.split("+"):
        if line.find("*") == -1:
            acc_id = int(line.partition("*")[0])
            qt = 1
        else:
            acc_id = int(line.partition("*")[0])
            qt = int(line.partition("*")[2])
        
        if acc_id in d:
            d[acc_id] = d[acc_id] + qt
        else:
            d[acc_id] = qt
    
    return d

def draw_table(jlist: list):
    table = Table()
    table.add_column("Name", style="green")
    table.add_column("Avail.", style="green")
    table.add_column("Int.", style="green")

    for cur in jlist:
        table.add_row(cur["name"], str(cur["remaining_qty"]), str(cur["intended_qty"]))

    console.print(table)

def validate_qty(jlist: list):
    for cur in jlist:
        if cur["intended_qty"] > cur["remaining_qty"]:
            message = "[yellow]Insuficient quantity! Intended {0}, but only {1} available of: [/yellow]{2}".format(str(cur["intended_qty"]), str(cur["remaining_qty"]), cur["name"])
            print(message)
            raise typer.Abort()

def generate_group_json(group_number: str) -> str:
    return """{"Automatic_Info":"Nao alterar / Dont touch","group_id":"@!GID""" + group_number + """#"}"""

def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

@app.command()
def cout(user: int, group: str, itens: str):
    """
    Checkouts stock itens to a team.
    """
    acc_dic = qtys2list(itens) # Transform argument in dictionary.
    json_item_list = asyncio.run( bulk_get_itens(list(acc_dic.keys()) , "/api/v1/accessories/") ) # Get intended acessories information from Snipe-IT.

    # Append intended quantites to JSON
    for cur in json_item_list:
        cur["intended_qty"] = acc_dic[cur["id"]]

    user_name = get_user_name(user)
    print(f"Checkout the following itens to user: [bold red]{user_name}[/bold red]?")
    
    draw_table(json_item_list)
    validate_qty(json_item_list)

    actuate = typer.confirm("Are you sure?")
    if not actuate:
        raise typer.Abort()
    else:
        for acc2req in json_item_list:
            i = 1
            while i < acc2req["intended_qty"] + 1:
                accessories_id_checkout(acc2req["id"], user, generate_group_json(group))
                i += 1

@app.command()
def cin(group: int, users: List[int]):
    """
    Checkins stock itens from a team.
    """
    acclist1 = []
    for user in users:
        acclist1 += users_id_accessories_get_rows(user)
    acclist2 = []
    for acc in acclist1:
        acclist2.append(acc["id"])

    acclist3 = unique(acclist2)

    checkouts = []
    for acc in acclist3:
        checkouts_subset = accessories_id_checkedout_get_rows(acc)
        checkouts += checkouts_subset

    checkouts2 = []
    group_mark = "@!GID" + str(group) + "#"
    for acc in checkouts:
        if acc["checkout_notes"] != None:
            if group_mark in acc["checkout_notes"]:
                checkouts2.append(acc)

if __name__ == "__main__":
    app()
