import random
from application.ultraconsole import UltraConsole as UC

def taskagitmakas(**kwargs):
    secenekler = ["taş", "kağıt", "makas"]
    
    while True:
        # oyuncu_secimi = input("Taş, Kağıt veya Makas seçin (çıkmak için 'q' tuşuna basın): ").lower()
        oyuncu_secimi = UC.create_frame("Seçimini Yap","-----Taş-----Kağıt-----Makas----- lütfen birini yazın","Çıkmak için 'q' tuşuna basın):")
        oyuncu_secimi = oyuncu_secimi.lower()
        
        if oyuncu_secimi == "q":
            return "Oyun bitti, teşekkürler!"
        
        if oyuncu_secimi not in secenekler:
            # print("Geçersiz seçim! Lütfen taş, kağıt veya makas yazın.")
            UC.create_frame("Geçersiz seçim!","Lütfen taş, kağıt veya makas yazın.")
            continue

        bilgisayar_secimi = random.choice(secenekler)
        # print(f"Bilgisayarın seçimi: {bilgisayar_secimi}")
        UC.create_frame("Benim Seçimim :)",f"Bilgisayarın seçimi: {bilgisayar_secimi}")

        if oyuncu_secimi == bilgisayar_secimi:
            UC.create_frame("Berabere!","Aynı Seçimleri Yaptık :)")
        elif (oyuncu_secimi == "taş" and bilgisayar_secimi == "makas") or \
             (oyuncu_secimi == "kağıt" and bilgisayar_secimi == "taş") or \
             (oyuncu_secimi == "makas" and bilgisayar_secimi == "kağıt"):
            UC.create_frame("TEBRİKLER!!!","Kazandın! Seçiminin "+oyuncu_secimi+" olacağını tahmin etmeliydim :)")
        else:
            UC.create_frame("ÜZGÜNÜM :(","Kaybettiniz! "+oyuncu_secimi+"a karşı "+bilgisayar_secimi+" kazanır.")

