import threading
from eg2 import func
y = dict()
print(id(y))

z = threading.Thread(target=func, args=(y, ))
z.start()
z.join()