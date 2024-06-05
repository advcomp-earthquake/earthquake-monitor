import zenoh
if __name__ == "__main__":
    session = zenoh.open()
    replies = session.get('demo/kitchen/temp', 
zenoh.ListCollector())
    for reply in replies():
        try:
            print("Received ('{}': '{}')"
                .format(reply.ok.key_expr, 
reply.ok.payload.decode("utf-8")))
        except:
            print("Received (ERROR: '{}')"
                .format(reply.err.payload.decode("utf-8")))
session.close()