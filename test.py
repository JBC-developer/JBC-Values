import numpy as np
import quickstart1

def main(images : dict):
    values1 : dict
    values1 = np.load('ValueList.npy', allow_pickle=True).item()
    k = list(values1.keys())
    v = list(values1.values())
    values2 = {}

    values2 = quickstart1.main(values2,"Textures!C9:K200")
    values2 = quickstart1.main(values2,'Hyperchromes!C10:K200')
    values2 = quickstart1.main(values2,"Colors!C9:K200")
    values2 = quickstart1.main(values2,"Rims!C9:K200")
    values2 = quickstart1.main(values2,"Spoilers!C9:K200")
    values2 = quickstart1.main(values2,"Tires & Horns!C9:M200")
    values2 = quickstart1.main(values2,"Furniture!C9:K200")
    values2 = quickstart1.main(values2,"Vehicles!C9:K200")

    

    
    k = list(values2.keys())
    v = list(values2.values())
    values2 = {}
    values2 = {k: v for k, v in zip(k,v)}

    #print(images)

    for ka in k:
        if ka.lower() in list(images.keys()):
            values2[ka][0] = images[ka.lower()]
        if ka in list(images.keys()):
            values2[ka][0] = images[ka]
    
    for key, value in values2.items() :
        print (("'"+ key +"'").strip(), ':', value, end=',\n')

    np.save('ValueList.npy', values2)
    
