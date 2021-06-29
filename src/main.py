from db import addItem, doneItem, showItems, showAll, showDone, resetDefault

# main function
def main():
    yes = ['sim', 'si', 'sisi', 'yes', 'yeah', 'yep', 'aye']
    def anyMore():
        answer = input('\nAlgo mais? \n> ')
        if answer in yes: main()
        else: exit()


    command = input('\nO que deseja fazer? Para saber dos comandos, use help:\n> ').split()
    
    # help command
    if command[0] == 'help':
        print('''
        use "todo" + data da sua atividade + item a fazer!\n
        use "done" + item que você finalizou!\n
        "show" + data para ver TODOs de tal data!\n
        "showall" para ver todos os TODOs!\n
        "showdone" para ver todos os TODOs finalizados!\n
        "reset" para resetar a aplicação!
        ''')
        main()

    # add todo command
    elif command[0] == 'todo':
        item = ''
        for i in range(2, len(command)):
            item += f"{command[i]} "

        addItem(command[1], item)
        anyMore()

    # done todo command
    elif command[0] == 'done':
        item = ''
        for i in range(1, len(command)):
            item += f"{command[i]} "

        doneItem(item)
        anyMore()

    # show todo from specific date command
    elif command[0] == 'show':
        showItems(command[1])
        anyMore()

    # show all todos command
    elif command[0] == 'showall':
        showAll()
        anyMore()

    # show all done todos
    elif command[0] == 'showdone':
        showDone()
        anyMore()

    # reset to default command
    elif command[0] == 'reset':
        st = 'Tem certeza? Digite "sim eu tenho" para excluir as databases: \n> '
        if input(st) == 'sim eu tenho':
            resetDefault()
            print('Aplicação resetada!')
            exit()
        else: 
            print('Ok, não excluirei!\n')
            anyMore()

    # command not recognized
    else:
        if input('Não entendi. Quer tentar novamente?\n> ') in yes: main()
        else: exit()
    
main()