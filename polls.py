import discord as dc 

def parsePoll(input):
    title = input[0]
    del input[0]

    parsed = {'Title': title, 'Options': input}
    return parsed

def createPoll(usrInput):
    #!Pass input to parse in list
    parsedInput = parsePoll(usrInput)
    print('Poll Title: ' + parsedInput.title)
    print('')
    
    i = 0
    for option in usrInput.Options:
        i += 1
        print('Option' + i + ': ' + option)


print(createPoll(['title', 'op1', 'op2', 'op3']))