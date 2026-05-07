class TuringMachine:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        # Bant kurulumu: Sayılar * ile ayrılır ve sonuna = eklenir. Boşluklar '_' ile temsil edilir.
        self.tape = list(f"{num1}*{num2}=") + ['_'] * 15 
        self.head = 0
        self.state = 'q_baslangic'
        self.step_count = 1
        
        # Çarpma işlemi için iç bellek (Durum kümesinin mantıksal temsili)
        self.multiplicand = ""
        self.multiplier = ""
        self.result_binary = ""
        
    def log_step(self, read_sym, write_sym, move):
        tape_str = "".join(self.tape).replace('_', ' ').strip()
        print(f"Adım {self.step_count}:")
        print(f"  Mevcut Durum   : {self.state}")
        print(f"  Okunan Sembol  : {read_sym}")
        print(f"  Yazılan Sembol : {write_sym}")
        print(f"  Kafa Hareketi  : {move}")
        # Kafanın bulunduğu konumu göstermek için basit bir işaretçi
        head_indicator = " " * self.head + "↓"
        print(f"  Bant İçeriği   :\n  {head_indicator}\n  {tape_str}\n" + "-"*30)
        self.step_count += 1

    def move_head(self, direction):
        if direction == 'R':
            self.head += 1
            # Bant sınırını aşarsa bantı uzat (Sonsuz bant simülasyonu)
            if self.head >= len(self.tape):
                self.tape.append('_')
        elif direction == 'L':
            self.head = max(0, self.head - 1)

    def run(self):
        print("--- Turing Makinesi Simülasyonu Başlıyor ---")
        print(f"Başlangıç Bantı: {''.join(self.tape).replace('_', '').strip()}\n" + "="*40)

        # 1. Aşama: '*' işaretini bul ve solundaki sayıyı (multiplicand) hafızaya al
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
                print(f"[*] Bilgi: '*' bulundu. Operandlar ayrıldı. Birinci Sayı: {self.multiplicand}\n" + "-"*30)
        
        # 2. Aşama: '*' işaretinin sağındaki sayıyı (multiplier) oku ve '=' işaretini bul
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
                print(f"[*] Bilgi: '=' bulundu. İkinci Sayı: {self.multiplier}. Çarpma başlıyor.\n" + "-"*30)

        # 3. Aşama: Shift & Add (Kaydır ve Topla) Mantığı
        self.state = 'q_hesaplama'
        if self.state == 'q_hesaplama':
            # Turing makinesinin karmaşık okuma/yazma döngüsünü mantıksal olarak simüle ediyoruz
            print("[*] Kaydır ve Topla (Shift & Add) İşlemi:")
            result = 0
            multiplicand_val = int(self.multiplicand, 2)
            
            # Sağdan sola doğru bitleri işleme
            for i, bit in enumerate(reversed(self.multiplier)):
                print(f"  -> Sağdan bit {i+1} = {bit}")
                if bit == '1':
                    shifted_val = multiplicand_val << i
                    result += shifted_val
                    print(f"     Bit '1': {self.multiplicand} sola {i} kez kaydırıldı (Değer: {bin(shifted_val)[2:]}) ve eklendi.")
                else:
                    print(f"     Bit '0': Sadece kaydırma yapıldı, toplama yapılmadı.")
            
            self.result_binary = bin(result)[2:]
            self.state = 'q_sonuc_yazma'
            print("-" * 30)

        # 4. Aşama: Sonucu '=' işaretinden sonra banta yazma
        while self.state == 'q_sonuc_yazma':
            for bit in self.result_binary:
                sym = self.tape[self.head]
                self.tape[self.head] = bit
                self.log_step(sym, bit, 'R')
                self.move_head('R')
            
            self.state = 'q_kabul'
            sym = self.tape[self.head]
            self.log_step(sym, sym, 'N') # N = Kafa Sabit (None/Neutral)
            print("--- Simülasyon Tamamlandı (Kabul Durumu) ---")


def validate_binary(binary_str):
    """Girdinin sadece 0 ve 1 içerip içermediğini kontrol eder."""
    for char in binary_str:
        if char not in ['0', '1']:
            return False
    return True

def main():
    print("=== Turing Makinesi ile Binary Çarpma ===")
    
    # 1. Kullanıcıdan girdileri al ve doğrula
    while True:
        num1 = input("Birinci binary sayıyı girin (Örn: 11): ").strip()
        if validate_binary(num1) and len(num1) > 0:
            break
        print("Hata: Sadece 0 ve 1 rakamlarını kullanabilirsiniz.")
        
    while True:
        num2 = input("İkinci binary sayıyı girin (Örn: 10): ").strip()
        if validate_binary(num2) and len(num2) > 0:
            break
        print("Hata: Sadece 0 ve 1 rakamlarını kullanabilirsiniz.")

    # 2. Turing Makinesini Başlat
    tm = TuringMachine(num1, num2)
    tm.run()

    # 3. Sonuçları Göster
    print("\n" + "="*40)
    print("\tBEKLENEN ÇIKTI VE SAĞLAMA")
    print("="*40)
    
    decimal_num1 = int(num1, 2)
    decimal_num2 = int(num2, 2)
    decimal_result = decimal_num1 * decimal_num2
    
    print(f"Birinci Sayı : {num1}₂ = {decimal_num1}₁₀")
    print(f"İkinci Sayı  : {num2}₂ = {decimal_num2}₁₀")
    print(f"İşlem        : {decimal_num1} × {decimal_num2} = {decimal_result}₁₀")
    print(f"Sonuç Bantı  : {''.join(tm.tape).replace('_', '').strip()}")
    print(f"Final Sonuç  : {tm.result_binary}₂")

if __name__ == "__main__":
    main()