from query import get_answer_of_query
import time

t1 = time.time()
a = get_answer_of_query("Explain Transformer Architecture")
t2 = time.time()
print(a)
