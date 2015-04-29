import time
while True:
    try:
        x=raw_input()
        print x
    except Exception:
        break

for i in xrange(10):
    print 'hello',i
    time.sleep(1)

