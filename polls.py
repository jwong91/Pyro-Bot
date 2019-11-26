import discord as dc 

def parsePoll(ctx, input):
    title = input[0]
    del input[0]

    parsed = {'Title': title, 'Options': input}
    return parsed

def createPoll(ctx, usrInput):
    i = 0
    #!Pass input to parse in list
    parsedInput = parsePoll(ctx, usrInput) #! This is the dict parsed
    print('Poll Title: ' + parsedInput['Title'])
    
    for option in parsedInput['Options']:
        i += 1
        print('Option' + str(i) + ': ' + option)


createPoll('ctx', ['this is a title', 'op1', 'op2', 'op3'])
