from application.menu_olusturucu import MenuSystem as MS
import os
import json

class SettingsMenu():
  
    def menu_goster(self, **kwargs):
        config = MS.read_config()                                   # Ayarları oku
        menu_data = MS.load_json(config["menu_file"])               # Menü verilerini yükle
        root = list(menu_data.keys())[int(config.get("settings_menu_root"))]
        settings_menu = MS(menu_data[root], 1, "application", "settings", "SettingsMenu", None, "settings", **kwargs)                                    # Menü sistemini başlat (init fonksiyonu çalışır ancak henüz menü gösterilmez)
        settings_menu.show_menu(root)
        
    def settings(self, **kwargs):
        if kwargs.get("selected_key") == 1:
            SettingsMenu.ayarlari_goster(MS.read_config())
        elif kwargs.get("selected_key") == 2:
            SettingsMenu.ayar_degistir(MS.read_config())
        elif kwargs.get("selected_key") == 3:
            SettingsMenu.menu_islem()

    def ayarlari_goster(ayarlar):
        ayar_dokumu = "            ".join(f"{key}: {value}" for key, value in ayarlar.items())
        MS.create_frame("Mevcut Ayarlar", ayar_dokumu)
    
    def ayar_degistir(ayarlar):
        while True:
            ayarlar_listesi = [f"{key}: {value}" for key, value in ayarlar.items()]
            os.system('cls' if os.name == 'nt' else 'clear')  # Konsolu temizle
            secim = MS.create_frame("Ayar Değiştirme Menüsü", ayarlar_listesi + ["Geri Dön"], "menu")
            
            if secim.lower() == "0":
                os.system('cls' if os.name == 'nt' else 'clear')  # Konsolu temizle
                break
            
            if secim.isdigit() and 1 <= int(secim) <= len(ayarlar):
                secim_index = int(secim) - 1
                secilen_anahtar = list(ayarlar.keys())[secim_index]
                yeni_deger = MS.create_frame("Yeni Değer Girişi", f"Uyarı: {secilen_anahtar} için yeni değeri girişi yapılıyor ", "Yeni değer:\n")
                if yeni_deger:
                    eminmisiniz = MS.create_frame("Yeni Değer Girişi", f"Uyarı: {secilen_anahtar} değeri {yeni_deger} olarak değiştirilecektir. Bu değişikliği yapmak istediğinize emin misiniz?", "E/H\n")
                    if eminmisiniz.lower() == "e":
                        ayarlar[secilen_anahtar] = yeni_deger
                        SettingsMenu.ayarlari_kaydet(ayarlar)
            else:
                MS.create_frame("Hata", "Geçersiz seçim yapıldı. Lütfen tekrar deneyin.")

    
    def ayarlari_kaydet(ayarlar):
        MS.save_config(ayarlar)
        MS.create_frame("Ayarlar Kaydedildi", "Ayarlar başarıyla kaydedildi.")

    def menu_islem():
        config = MS.read_config()                                   # Ayarları oku
        menu_data = MS.load_json(config["menu_file"])               # Menü verilerini yükle
        root = list(menu_data.keys())[int(config.get("menu_root"))]

        no_submenu_keys = []

        for key, value in menu_data[root].items():
            if not isinstance(value, dict):  # Eğer değeri bir sözlük değilse (yani alt menüsü yoksa)
                no_submenu_keys = no_submenu_keys+[key]
        

        options_for_selection = ["Ekle", "Sil", "Değiştir", "Geri Dön"]
        os.system('cls' if os.name == 'nt' else 'clear')  # Konsolu temizle
        operation = int(MS.create_frame("İşleminizi Seçin", options_for_selection, "menu"))
        if operation == 2 or operation == 3:
            os.system('cls' if os.name == 'nt' else 'clear')  # Konsolu temizle
            selection  = MS.create_frame("İşlem Yapmak İstediğiniz Modülü Seçiniz", no_submenu_keys+["Geri Dön"], "menu")
            if operation == 2:
                if no_submenu_keys[int(selection)-1] in menu_data[root]:
                    warn = MS.create_frame("SİLME İŞLEMİ ONAYI!", str(no_submenu_keys[int(selection)-1])+" adlı modül menüden silinmek üzrere! İşleme devam etmek istiyormusunuz!", "(E/H)")
                    if warn.lower() == "e":
                        del menu_data[root][no_submenu_keys[int(selection)-1]]
                        SettingsMenu.save_menu(menu_data)
                        MS.create_frame("MODÜL SİLİNDİ!", str([no_submenu_keys[int(selection)-1]])+" adlı modül menüden başarı ile silindi", "info")
                    else:
                        MS.create_frame("Silme İşlemi İptal Edildi", str([no_submenu_keys[int(selection)-1]])+" adlı modül silinmedi!", "info")
                else:
                    MS.create_frame("Modül Bulunamadı", str([no_submenu_keys[int(selection)-1]])+" adlı modül bulunamadı!", "info")
                    
            if operation == 3:
                if no_submenu_keys[int(selection)-1] in menu_data[root]:
                    ckey = no_submenu_keys[int(selection)-1]
                    cvalue = menu_data[root][ckey]
                    os.system('cls' if os.name == 'nt' else 'clear')  # Konsolu temizle
                    opt = MS.create_frame(ckey+" Modülünde Yapılacak Değişikliği Seçin", ["Modül Adı","Fonsiyon Adı","Her İkisi","Geri Dön"], "menu")
                    if int(opt) == 1:
                            while True:
                                new_name = MS.create_frame("Modül Adı Değiştirme", ckey+" adlı modül için yeni ad girin!", "")
                                if new_name not in menu_data[root]:
                                    warn = MS.create_frame("Modül Adı Değiştirme", ckey+" modülünün adını "+new_name+" olarak değiştirmek üzeresiniz! Devam etmek istiyor musunuz?", "(E/H)")
                                    if warn.lower() == "e":
                                        menu_data[root][new_name] = menu_data[root][ckey]
                                        del menu_data[root][ckey]
                                        SettingsMenu.save_menu(menu_data)
                                        MS.create_frame("Modül Adı Değiştirme", ckey+" modülünün adı "+new_name+" olarak başarı ile değiştirildi", "info")
                                        break
                                    else:
                                        MS.create_frame("Modül Adı Değiştirme", ckey+" modülünün adı "+new_name+" olarak değiştirme işlemi iptal edildi!", "info")
                                else:
                                    MS.create_frame("Modül Adı Değiştirme", new_name+" adında bir modüz zaten mevcut!", "info")
                

                    if int(opt) == 2:
                        new_fonk = MS.create_frame("Modül Fonksiyonu Değiştirme", ckey+" adlı modül için yeni fonksiyon adı girin! Not: Modül adı ve fonksiyon adı aynı olamk zorundadır.", "")
                        warn = MS.create_frame("Modül Fonksiyonu Değiştirme", ckey+" modülünün "+cvalue+" fonksiyonunu "+new_fonk +" olarak değiştirmek üzeresiniz! Devam etmek istiyor musunuz?", "(E/H)")
                        if warn.lower() == "e":
                            menu_data[root][ckey] = new_fonk 
                            SettingsMenu.save_menu(menu_data)
                            MS.create_frame("Modül Fonksiyonu Değiştirme", ckey+" modülünün fonksiyonu "+new_fonk+" olarak başarı ile değiştirildi", "info")
                        else:
                            MS.create_frame("Modül Adı Değiştirme", ckey+" modülünün fonksiyonu "+new_fonk+" olarak değiştirme işlemi iptal edildi!", "info")

                    if int(opt) == 3:
                            while True:
                                new_name = MS.create_frame("Modül Adı Değiştirme", ckey+" adlı modül için yeni ad girin!", "")
                                if new_name not in menu_data[root]:
                                    new_fonk = MS.create_frame("Modül Fonksiyonu Değiştirme", ckey+" adlı modül için yeni fonksiyon adı girin! Not: Modül adı ve fonksiyon adı aynı olamk zorundadır.", "")
                                    warn = MS.create_frame("Modül Adı ve Fonksiyon Değiştirme", ckey+" modülünün adını "+new_name+" olarak ve "+cvalue+" fonksiyonunu "+new_fonk +" olarak değiştirmek üzeresiniz! Devam etmek istiyor musunuz?", "(E/H)")
                                    if warn.lower() == "e":
                                        menu_data[root][new_name] = menu_data[root][ckey]
                                        del menu_data[root][ckey]
                                        menu_data[root][new_name] = new_fonk
                                        SettingsMenu.save_menu(menu_data)
                                        MS.create_frame("Modül Adı Değiştirme", ckey+" modülünün adı "+new_name+" olarak başarı ile değiştirildi", "info")
                                        break
                                    else:
                                        MS.create_frame("Modül Adı Değiştirme", ckey+" modülünün adı "+new_name+" olarak değiştirme işlemi iptal edildi!", "info")
                                else:
                                    MS.create_frame("Modül Adı Değiştirme", new_name+" adında bir modüz zaten mevcut!", "info")
                else:
                    MS.create_frame("Modül Bulunamadı", str(ckey)+" adlı modül bulunamadı!", "info")

        elif operation == 1:
            while True:
                new_key  = MS.create_frame("Mevcut Modüller", "|"+"|   |".join(f"{i+1}. {item}" for i, item in enumerate(no_submenu_keys))+"|", "Yeni Menü Adını Giriniz")
                if new_key not in no_submenu_keys:
                    break
                else:
                    MS.create_frame("Bu Menü Mevcut", new_key+" adında bir modül zaten mevcut!", "info")
            new_value = MS.create_frame("Fonksiyon Adı", new_key+" adlı modül seçeneği için fonksiyon adı girin. Not: Modül adı ve fonksiyon adı aynı olamk zorundadır.", "")
            warn = MS.create_frame("Modül Ekleme", new_key+" adlı modülü "+new_value+" fonksiyonu ile eklemek üzeresiniz! Devam etmek istiyor musunuz?", "(E/H)")
            if warn.lower() == "e":
                menu_data[root][new_key] = new_value
                SettingsMenu.save_menu(menu_data)
                MS.create_frame("Modül Ekleme", new_key+" adlı modül "+new_value+" fonksiyonu ile eklendi.", "info")
            else:
                MS.create_frame("Modül Ekleme", new_key+" adlı modül "+new_value+" fonksiyonu ile ekleme işlemi iptal edildi.", "info")

    def save_menu(menu_data):
        config = MS.read_config()
        with open(config["menu_file"], 'w', encoding='utf-8') as file:
            json.dump(menu_data, file, indent=4, ensure_ascii=False)



        
       

