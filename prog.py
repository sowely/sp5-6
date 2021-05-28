from threading import Thread, Semaphore
import threading
from multiprocessing import Pipe
from random import randint
import os
import signal
from time import sleep, time

def f(conn):
    global iters, blockChange
    teamName = threading.current_thread().getName()
    fighters = 5
    print(os.getpid())
    mutexTime = time()
    while fighters > 0:
       sleep(0.01)
       with blockChange:
           print("time when iters changes:", time() - mutexTime)
           iters += 1
           sleep(1)
       print(teamName,"has", fighters,"fighters")
       inc = randint(0, 9)
       fighters += inc
       print(teamName, "+", inc, "=", fighters)
       dec = randint(0, 9)
       conn.send(dec)
       print(teamName,"SEND dec", dec)
       sleep(1) #sleep
       dec = conn.recv()
       print(teamName,"RECV dec", dec)
       fighters -= dec
       if fighters < 0:
          fighters = 0
       print(fighters, "fighters in the", teamName,"--------")
       sleep(1)
       if fighters == 0:
          print("LOOSER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", teamName) #, threading.get_ident())
          print(iters // 2,"iterations")
          os.kill(os.getpid(), signal.SIGTERM) # or signal.SIGKILL

conn1, conn2 = Pipe()
p1 = Thread(target=f, args=(conn1,), name="TEAM1", daemon=True)
p2 = Thread(target=f, args=(conn2,), name="TEAM2", daemon=True)
blockChange = Semaphore(value=1)
iters = 0
p1.start()
p2.start()
p1.join()
p2.join()
