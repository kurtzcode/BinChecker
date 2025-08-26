# MODULES
import requests
import os  

"""main checker"""
class main(object):

    """Verifica se o BIN foi informado"""
    @classmethod
    def check(cls, bins):
        if bins.strip() == '':
            print('[!] INVALID BIN')
        else:
            cls.main(bins.strip())

    """Faz a requisição para a Binlist.net"""
    @classmethod
    def main(cls, x):
        url = f"https://lookup.binlist.net/{x}"  
        headers = {"Accept-Version": "3"}       

        try:
            req = requests.get(url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"[!] Erro de conexão: {e}")
            return

        try:
            data = req.json()
        except ValueError:
            print("[!] Resposta não é JSON ou inválida.")
            print("Status:", req.status_code, "| Conteúdo:", req.text[:200], "...")
            return

        if req.status_code != 200 or not data:
            print("[!] Erro na consulta BIN ou BIN não encontrado.")
            return

        
        r = {
            'bin': x,
            'vendor': data.get('scheme', ''),   # Bandeira
            'type': data.get('type', ''),       # Tipo (Credit/Debit)
            'level': data.get('brand', ''),     # Marca do cartão (às vezes vazio)
            'bank': data.get('bank', {}).get('name', ''),
            'country': data.get('country', {}).get('name', '')
        }

        cls.main_check(r, {
            'author': 'Kurtz',
            'version': '1.0'
        })

    """Exibe os dados"""
    @classmethod
    def main_check(cls, r, xx):
        print(f"""
 [+] Author: {xx['author']}
 [+] Version: {xx['version']}""")

        print(f"""
 [+] Bin: {r['bin']}
 [+] Vendor: {r['vendor']}
 [+] Type: {r['type']}
 [+] Level: {r['level']}
 [+] Bank: {r['bank']}
 [+] Country: {r['country']}""")


if __name__ == '__main__':
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        
        full_number = input('[+] BIN: ').strip()

        if not full_number.isdigit() or len(full_number) < 6:
            print('[!] BIN inválido! Digite apenas números e pelo menos 6 dígitos.')
            continue

        
        BIN_NUMBER = full_number[:6]

        main.check(BIN_NUMBER)
        print("\n" + "-"*50 + "\n")
