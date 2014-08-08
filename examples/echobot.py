from line import LineClient, LineGroup, LineContact

try:
    client = LineClient("ID", "PASSWORD")
    #client = LineClient(authToken="AUTHTOKEN")
except:
    print "Login Failed"

while True:
    op_list = []

    for op in client.longPoll():
        op_list.append(op)

    for op in op_list:
        message = op[1]
        sender  = op[0]
        
        msg = message.text
        sender.sendMessage(msg)

