class TuringMachine:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        # Bant kurulumu: Sayılar * ile ayrılır ve sonuna = eklenir. '_' boşlukları temsil eder.
        self.tape = list(f"{num1}*{num2}=") + ['_'] * 20 
        self.head = 0
        self.state = 'q_baslangic'
        self.step_count = 1
        
        # İç bellek (Sadece karakter dizisi olarak tutulur)
        self.multiplicand = ""
        self.multiplier = ""
        self.result_binary = "0"
        
    def log_step(self, read_sym, write_sym, move):
        tape_str = "".join(self.tape)
        print(f"Adım {self.step_count:03d} | Durum: {self.state:<17} | Okunan: {read_sym} | Yazılan: {write_sym} | Yön: {move}")
        
        # Ok işaretini tam karakterin üzerine kusursuz hizalamak için:
        head_indicator = " " * self.head + "↓"
        print(f"Bant:\n      {head_indicator}\n      {tape_str}")
        print("-" * 65)
        self.step_count += 1

    def move_head(self, direction):
        if direction == 'R':
            self.head += 1
            if self.head >= len(self.tape):
                self.tape.append('_')
        elif direction == 'L':
            self.head = max(0, self.head - 1)

    def pure_binary_add(self, bin_str1, bin_str2):
        # Saf Lojik Kapı (Carry) mantığıyla ikili toplama işlemi
        max_len = max(len(bin_str1), len(bin_str2))
        v1 = bin_str1.zfill(max_len)
        v2 = bin_str2.zfill(max_len)
        carry = 0
        result_str = ""
        
        for i in range(max_len - 1, -1, -1):
            b1 = 1 if v1[i] == '1' else 0
            b2 = 1 if v2[i] == '1' else 0
            
            total = b1 + b2 + carry
            if total == 0:
                result_str = "0" + result_str; carry = 0
            elif total == 1:
                result_str = "1" + result_str; carry = 0
            elif total == 2:
                result_str = "0" + result_str; carry = 1
            elif total == 3:
                result_str = "1" + result_str; carry = 1
                
        if carry == 1:
            result_str = "1" + result_str
        return result_str

    def run(self):
        print("\n" + "="*65)
        print("TURING MAKİNESİ SİMÜLASYONU BAŞLIYOR")
        print("="*65 + "\n")

        # 1. Aşama: '*' işaretini bulana kadar birinci sayıyı işle
        while self.state == 'q_baslangic':
            sym = self.tape[self.head]
            if sym in ['0', '1']:
                self.multiplicand += sym
                self.log_step(sym, sym, 'R')
                self.move_head('R')
            elif sym == '*':
                self.state = 'q_ayrac_bulundu'
                self.log_step(sym, sym, 'R')
                self.move_head('R')
                print(f"\n[İnfo] '*' ayracı geçildi. 1. Sayı bulundu: {self.multiplicand}\n")
        
        # 2. Aşama: '=' işaretini bulana kadar ikinci sayıyı işle
        while self.state == 'q_ayrac_bulundu':
            sym = self.tape[self.head]
            if sym in ['0', '1']:
                self.multiplier += sym
                self.log_step(sym, sym, 'R')
                self.move_head('R')
            elif sym == '=':
                self.state = 'q_esittir_bulundu'
                self.log_step(sym, sym, 'R')
                self.move_head('R')
                print(f"\n[İnfo] '=' ayracı geçildi. 2. Sayı bulundu: {self.multiplier}\n")

        # 3. Aşama: '=' işaretinden sonraki boşluğa gelince L (Sol) yaparak hesaba başla
        while self.state == 'q_esittir_bulundu':
            sym = self.tape[self.head]
            if sym == '_': 
                self.state = 'q_hesaplama'
                self.log_step(sym, sym, 'L')
                self.move_head('L')

        # 4. Aşama: Shift & Add İşlemi (Fiziksel Kafa Hareketleri ve Adım Adım Gösterim)
        if self.state == 'q_hesaplama':
            print("\n" + "*"*65)
            print("[#] HESAPLAMA (SHIFT & ADD) ALT RUTİNİ BAŞLADI")
            print("*"*65)
            
            if '1' not in self.multiplicand or '1' not in self.multiplier:
                print(" -> Yutan eleman (0) tespit edildi. Sonuç doğrudan 0 yazılacak.\n")
                self.result_binary = "0"
            else:
                current_multiplicand = self.multiplicand
                
                # Kafa '=' üzerinde. Biti okumak için fiziksel olarak sola dönüyor
                self.log_step('=', '=', 'L')
                self.move_head('L')
                
                for i in range(len(self.multiplier)):
                    bit = self.tape[self.head] # Kafa tam okunacak bitin üzerinde!
                    
                    # YENİ DÜZEN: Önce bantın o anki durumunu (kafa hangi bitin üzerindeyse onu) basıyoruz
                    self.log_step(bit, bit, 'L')
                    
                    # Sonra o bit ile ne işlem yapıldığını anlatıyoruz
                    print(f"--- İşlem: Sağdan {i+1}. bit okundu (Banttaki Değer: '{bit}') ---")
                    
                    if bit == '1':
                        self.result_binary = self.pure_binary_add(self.result_binary, current_multiplicand)
                        print(f" -> İşlem       : Çarpılan dizi ('{current_multiplicand}') eklendi.")
                        print(f" -> Güncel Kasa : {self.result_binary}")
                    else:
                        print(f" -> İşlem       : Toplama YAPILMADI (Bit 0).")
                        print(f" -> Güncel Kasa : {self.result_binary}")
                    
                    # Sola kaydırma işleminin şeffaf gösterimi
                    eski_deger = current_multiplicand
                    current_multiplicand += "0" 
                    print(f" -> Sola Kaydır : '{eski_deger}' -> sonuna '0' eklendi -> '{current_multiplicand}'\n")
                    
                    # İşlem bittikten sonra kafayı fiziksel olarak diğer bite (sola) kaydır
                    self.move_head('L')
            
            print("[*] Hesaplama bitti. Yazma işlemine geçmek için kafa boşluğa ('_') ilerliyor...\n")
            # Kafa şu an '*', '1' veya '0' üzerinde olabilir. '='i geçip boşluğu bulana kadar sağa gider.
            while self.tape[self.head] != '_':
                sym = self.tape[self.head]
                self.log_step(sym, sym, 'R')
                self.move_head('R')
                
            self.state = 'q_sonuc_yazma'

        # 5. Aşama: Hesaplanan sonucu banta tek tek yazma
        print("\n" + "="*65)
        print("SONUÇ BANT ÜZERİNE YAZILIYOR")
        print("="*65)
        while self.state == 'q_sonuc_yazma':
            for bit in self.result_binary:
                sym = self.tape[self.head]
                self.tape[self.head] = bit
                self.log_step(sym, bit, 'R')
                self.move_head('R')
            
            self.state = 'q_kabul'
            sym = self.tape[self.head]
            self.log_step(sym, sym, 'N')
            print("\n" + "="*65)
            print("SİMÜLASYON BAŞARIYLA TAMAMLANDI (Kabul Durumu)")
            print("="*65)

def validate_binary(binary_str):
    return all(char in ['0', '1'] for char in binary_str)

def main():
    print("=== Tek Bantlı Turing Makinesi İle İkili (Binary) Çarpma ===")
    
    while True:
        num1 = input("Birinci binary sayıyı girin (Örn: 11): ").strip()
        if validate_binary(num1) and len(num1) > 0:
            break
        print("Hata: Sadece 0 ve 1 kullanınız.")
        
    while True:
        num2 = input("İkinci binary sayıyı girin (Örn: 10): ").strip()
        if validate_binary(num2) and len(num2) > 0:
            break
        print("Hata: Sadece 0 ve 1 kullanınız.")

    tm = TuringMachine(num1, num2)
    tm.run()

    decimal_num1 = int(num1, 2)
    decimal_num2 = int(num2, 2)
    decimal_result = decimal_num1 * decimal_num2

    print("\nSAĞLAMA VE SONUÇ:")
    print(f"İşlem       : {num1}₂ x {num2}₂")
    print(f"Ondalık     : {decimal_num1} x {decimal_num2} = {decimal_result}")
    print(f"Bant Sonucu : {tm.result_binary}₂")

if __name__ == "__main__":
    main()