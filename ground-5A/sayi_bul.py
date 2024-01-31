#Kullanıcının 5 adet hakkı olacak. Her yanlış sayı girdiğinde hak 1 azalacak.
#Eğer kullanıcı tahmin ettiği sayı random seçilen sayıdan büyük ise alçal yazılacak, küçük ise yüksel yazılacak
#Eğer kullanıcının tahmin etme hakkı biterse oyun sona erecek
#Eğer kullanıcı sayıyı doğru tahmin ederse tebrikler yazdırın.

print("hosgeldiniz")

import random

r_sayi = random.randint(1,100)

for x in range(1,6):


    k_sayi = int(input("sayi giriniz:"))


    if r_sayi == k_sayi:
        print("Tebrikler doğru tahmin ettiniz.\n Aradığınız sayı:" + str(r_sayi))

        break

    elif x == 5:
        print("Kaybettiniz\n Aradığınız sayı:" + str(r_sayi))
        break

    elif r_sayi < k_sayi:
        print("azalt")

    elif r_sayi > k_sayi:
        print("yükselt")

