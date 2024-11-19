#Importation bibliothèques
from numpy import *
from matplotlib.pyplot import *
from pylab import *

# définition fonction de tranfert
#PV : fréquence plus parlant (effectivement ce n'est qu'a des facteur pres
ft=3000 # fréquence de mon signal
dureeT = 10/ft   #Observation temporelle sur 10 période


fe=96000 # fréquence ech

######################## A SUPP
#fcnt=wt/we
#wcnt=2*pi*fcnt
##################################


#Signal temporel : 
t = np.linspace(0, dureeT, int(dureeT * fe), endpoint=False)  # Vecteur temps
x = np.sin(2 * np.pi * ft * t)  # Signal sinusoïdal

def H(f):
    return H0 / (1 + 1j * f * 2 * np.pi / wc)


#Test à mofidier...
def filtreNumTemp(data):
    a0 = 0.1153
    a1 = -0.1153
    b1 = 1.8777
    b2 = -0.8809
    filtered_data = np.zeros_like(data) #Creation donnee sortie meme type que data
   

    filtered_data[0] = a0*data[0]
    filtered_data[1] = a0*data[1] + a1 * data[0] + b1* filtered_data[0]
    filtered_data[2] = a0*data[2] + a1 * data[1] + b1* filtered_data[1] + + b2* filtered_data[0]
     
    for i in range(3, len(data)):
        filtered_data[i] =a0*data[i] + a1 * data[i-1] + b1* filtered_data[i-1] + + b2* filtered_data[i-2]
    return filtered_data





y = filtreNumTemp(x)
# Affichage des signaux
plt.figure()
plt.plot(t, x, label='Signal original')
plt.plot(t, y, label='Signal filtré', linestyle='--')
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Filtre Passe-Bas de Premier Ordre')
plt.grid()
plt.show()
###Autre méthode




