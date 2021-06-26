from db import addItem, doneItem, today

def main():
    command = input('O que deseja fazer? Para saber dos comandos, use help:\n').split()
    if command[0] == 'help':
        print('todo data item\ndone item\n')
        main()
    elif command[0] == 'todo':
        item = ''
        for i in range(2, len(command)):
            item += f"{command[i]} "

        addItem(command[1], item)
    elif command[0] == 'done':
        item = ''
        for i in range(1, len(command)):
            item += f"{command[i]} "

        doneItem(item)
    else:
        yes = ['sim', 'si', 'sisi', 'yes', 'yeah', 'yep', 'aye']
        if input('Não entendi. Quer tentar novamente? Use todo ou done!\n') in yes: main()
        else: exit()
    
main()