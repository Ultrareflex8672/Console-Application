from application.menu_olusturucu import MenuSystem as MS
import os

class UltraConsole(MS):

    def go_main_menu():
        all_config = MS.read_config()                               # Tüm ayarları oku (Şuanda burada bir işlevi yok ancak ileride kullanılabilir)
        modules_path = all_config.get("module_path")                # Modül yolu al (Şuanda burada bir işlevi yok ancak ileride kullanılabilir)
        menu_root_config = MS.read_config("menu_root")              # Menü kökünü al
        MS.check_and_create_config(MS.read_config("menu_file"))     # Menü dosyasını kontrol et ve oluştur
        menu_data = MS.load_json(MS.read_config("menu_file"))       # Menü verilerini yükle
        root = list(menu_data.keys())[int(menu_root_config)]        # İlk menüyü al (menu.cfg Dosyasındaki JSon da 1. Seviyede Birden Fazla Menü varsa İlk Menüyü Alır)                          # Menü başlığını al
        ms = MS(menu_data[root])                                    # Menü sistemini başlat (init fonksiyonu çalışır ancak henüz menü gösterilmez)
        ms.show_menu(root)                                          # Menüyü göster

    def go_custom_menu(menu_root, **kwargs):
        if kwargs.get("menu_data"):
            menu_data_ = kwargs.get("menu_data")
            if isinstance(menu_data_, dict):
                menu_data = menu_data_
                if menu_root != None:
                    if isinstance(menu_root, int):
                        root = list(menu_data.keys())[int(menu_root)]
                    else: 
                        raise  "Menü root verisi INTEGER formatında değil!"
                else:
                    raise "Menü root verisi eksik!"
            else:
                raise  "Menü verisi DICT formatında değil!"
        elif menu_root:
            if isinstance(menu_root, int):
                MS.check_and_create_config(MS.read_config("menu_file"))
                menu_data = MS.load_json(MS.read_config("menu_file"))
                root = list(menu_data.keys())[int(menu_root)]
            else:
                raise  "Menü root verisi INTEGER formatında değil!"
        else:
            raise "Özel menü oluşturma parametrelerinden hiç biri girilmdi - menu_data_ = LIST, menu_root_ = STR"
        
        if kwargs.get("module_name"):
            module_name = kwargs.get("module_name")
        else:
            module_name = None

        if kwargs.get("func_name"):
            func_name = kwargs.get("func_name")
        else:
            func_name = None

        if kwargs.get("module_path") and isinstance(kwargs.get("module_path"), str):
            module_path=kwargs.get("module_path")
        else:
            module_path="modules"

        if kwargs.get("class_name"):
            class_name = kwargs.get("class_name")
        else:
            class_name = None

        if kwargs.get("init_data"):
            init_data = kwargs.get("init_data")
        else:
            init_data = None

        ms = MS(menu_data[root], 1, module_path, module_name, class_name, init_data, func_name, **kwargs)
        ms.show_menu(root)
    
    def selected_key(key, **kwargs):
        if kwargs.get("selected_key") == key:
            return True
        else:
            return False
    
    def from_main_menu(**kwargs):
        if int(kwargs.get("menu_type")) == 0:
            return True
        else:
            return False
        
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear') 

