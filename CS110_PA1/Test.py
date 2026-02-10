def eval_fitness (run_time,pushups,situps):

    fit = str()
    rate = int()
    rate2 = int()
    rate3 = int()
    
    if run_time>13.5:
        rate = 0
    elif 12.5 < run_time <= 13.5:
        rate = 1
    else:
        rate = 2
    
    if pushups<30:
        rate2 = 0
    elif 50 > pushups  >= 30:
        rate2 = 1
    else:
        rate2 = 2
    
    if situps<39:
        rate3 = 0
    elif 48 > pushups  >= 39:
        rate3 = 1
    else:
        rate3 = 2
    
    if rate==0 or rate2==0 or rate3==0:
        fit = str("Unsatisfactory")
    elif 6>rate+rate2+rate3>5:
        fit = str("Excellent")
    elif 4>rate+rate2+rate3>3:
        fit = str("Satisfactory")
    
    return fit

c_run_time = float(input())
c_pushups = int(input())
c_situps = int(input())

c_fitness_rating = eval_fitness(c_run_time,c_pushups, c_situps)

print(c_fitness_rating)