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
        sender   = op[0]
        receiver = op[1]
        message  = op[2]
        
        msg = message.text
        receiver.sendMessage("[%s] %s" % (sender.name, msg))

