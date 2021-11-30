import random
def monte_carlo_pi(prec):
    outer_area = 4
    inside_counter = 0
    for _ in range(prec):
        x = random.uniform(-1,1)
        y = random.uniform(-1,1)
        if x*x+y*y<=1:
            inside_counter+=1
    return (inside_counter/prec)*outer_area

def monte_carlo_quarter_circle(prec):
    outer_area = 1
    inside_counter = 0
    for _ in range(prec):
        x = random.random()
        y = random.random()
        if x*x+y*y<=1:
            inside_counter+=1
    return (inside_counter/prec)*outer_area

print(monte_carlo_quarter_circle(1000000))