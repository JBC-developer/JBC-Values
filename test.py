
import numpy as np
import quickstart1
import values

def main(images : dict):
    values1 : dict
    values1 = np.load('ValueList.npy', allow_pickle=True).item()
    k = list(values1.keys())
    v = list(values1.values())
    values2 = {}

    #values2 = quickstart1.main(values2,"Textures!C9:K200")
    values2 = quickstart1.main(values2,'Hyperchromes!C10:K200')
   # values2 = quickstart1.main(values2,"Colors!C9:K200")
   # values2 = quickstart1.main(values2,"Rims!C9:K200")
   # values2 = quickstart1.main(values2,"Spoilers!C9:K200")
   # values2 = quickstart1.main(values2,"Tires & Horns!C9:M200")
   # values2 = quickstart1.main(values2,"Furniture!C9:K200")
    values2 = quickstart1.main(values2,"Vehicles!C61:K200")
    values2 = values.main(values2, 'Value List!C20:F400')
    values2 = values.main(values2, 'Hyperchromes!C22:E63')

    

    
    k = list(values2.keys())
    v = list(values2.values())
    values2 = {}
    values2 = {k: v for k, v in zip(k,v)}

    #print(images)
    values1 = {}
    for key in values2.keys():
        values1[key.strip().lower()] = values2[key]
    for ka in k:
        if ka.lower() in list(images.keys()):
            values1[ka.lower()][0] = images[ka.lower()]
        if ka in list(images.keys()):
            values1[ka.lower()][0] = images[ka]
    
    for key, value in values1.items() :
        if value[0] == '':
            print (("'"+ key +"'").strip(), ':', value, end=',\n')
    values1['torpedo'][0] = 'https://static.wikia.nocookie.net/rblx-jailbreak/images/4/40/Torpedo.png/revision/latest/scale-to-width-down/1000?cb=20220219030137.png'
    values1['m12'][0] = 'https://static.wikia.nocookie.net/rblx-jailbreak/images/3/37/MoltenHD.png/revision/latest?cb=20220211222718.png'

    np.save('ValueList.npy', values1)
