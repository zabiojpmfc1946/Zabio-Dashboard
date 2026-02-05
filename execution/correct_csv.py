import csv
import os

# Configuration
INPUT_FILE = "export-address-token-0x90eF96BCFB3e798C6565CBBA6a587F14b58003D3 (3)(Sheet1).csv"
TEMP_FILE = "export-address-token-corrected.csv"
ZABIO_ADDRESS = "0x90ef96bcfb3e798c6565cbba6a587f14b58003d3".lower()

# USER PROVIDED MAPPING (Extended with discovered wallets)
WALLET_TO_COMPANY = {
    "0x90ef96bcfb3e798c6565cbba6a587f14b58003d3": "Zabio",
    "0xd86a5afe3dcc8d76f8d61db8dcbb48b2a29eea27": "Keto Group",
    "0xd86a5619b4a49319d2b7957037cab8aff367ea27": "Keto Group", # Secondary wallet from user list
    "0x13d4c51985a287c25754944576c50911fb407dad": "Carlos Daniel OTC",
    "0xf74c31a102045184fe7d3821b5a61a92e40f4b19": "Activos Digitales",
    "0x71133c094ae933a779652a1201b5be923818d51d": "MiTec",
    "0x3eb296527614f3c7be16d5f8684df164d23d90f6": "Cripto manantial",
    "0x1f35b83b6ea222abbd2b0f7ffe6dbec58797e1d0": "Soluciones de abastecimiento Integral",
    "0x2370a1530701333ce394303dfe78a6c7f6605c05": "Digital Cash",
    "0xf0f7d6e94598be070f24d2f23085f7dff1f82682": "Carlos Cassiani",
    "0xdef32069f1544a29098d241bea179df52f936a00": "Cripto Xpress",
    "0xd1f3bb79e36813be4f21576cdda5d50f26083629": "Robotica innovacion sas",
    "0x52c5982d5a919717093021fb2cb8a672f8ce54b3": "SOLUCIONES DIGITALES NFT SAS",
    "0xa2764222ecf035c17533791ecb4281aafe622144": "Vivian Johanna Piedrahita Correa",
    "0x65d79c2c0bdb7d47400a21b50902d47c8a67bed8": "GMBank Casa De Las Monedas",
    "0xd518414d370464d78557ee63d49db794ae91edc3": "Wesley Smith",
    "0xcb5c5d6e1e23e664cff8c321079ef1bfb5fe7c30": "Crypto Go SAS",
    "0xe6c3500fc00585ce70d4c84941d0cf3f865446b5": "Jascalla",
    "0x5de536645a0b9434401cdd1a591c4a7bbac4b3ce": "FYNORA SAS",
    "0xa1f680b0b21bbab38dc6a30e449a93a08536d056": "Nicolás Calle Marín",
    "0xadc307f7b889187b066cd41cfee7fa9bf06f2969": "Profitnanzas JH",
    "0x5e0df580a309fd887939cb746e53bfea1b8d558a": "Good Venture SAS",
    "0x405733b90642cc71fd8a4e0e2650ec5b1313fd78": "PS613 SAS",
    "0xca843bdc40cbe25656af91cfb17c080a59f26733": "Miguel Tobon",
    "0xd80e209f8add77d873c44b3521853c1181fe3c85": "Salomé Gaviria",
    "0xd760fdfc2513077b104a53ca7cbbf7fa382b6580": "Salomé Gaviria", # Discovered secondary wallet
    "0xea1c3d1cdf4c0cfb987dba6f2e0996feb340904d": "SureFX",
    "0xcb5212ba34e9a51141c6842a8fc5654dabb68e7c": "CC Pay",
    "0xf13146c59922b34326bf1dfea77966866b045ed5": "Hugo Alejandro Castano",
    "0xe0f00cd1084189ce53472a423f1fa8ab166d76bb": "Yanet Giraldo",
    "0xfe70d9fb663ad57259c2c030ef064019c4a9c69c": "Santa Rosa Agroindustrial SAS",
    "0x272fc655c121237d8b67642eed5c4734a8c137c3": "Precooperativa Mercantil de Colombia",
    "0xaeb10598876351722e19657e89666e659bd009f1": "COLOCA GROUP",
    "0x95e267687da3f302ae3716d22b24610cab7960aa": "INVERSIONES R CASTRO S.A.S."
}

def correct_csv():
    # Use UTF-8 for reading since we previously saved it as UTF-8
    rows_corrected = 0
    with open(INPUT_FILE, mode='r', encoding='utf-8') as f_in, \
         open(TEMP_FILE, mode='w', encoding='utf-8', newline='') as f_out:
        
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            if len(row) < 10:
                writer.writerow(row)
                continue
            
            from_addr = row[3].lower()
            to_addr = row[5].lower()
            client_addr = from_addr if to_addr == ZABIO_ADDRESS else to_addr
            
            corrected_name = WALLET_TO_COMPANY.get(client_addr)
            if corrected_name:
                if row[4] != corrected_name:
                    row[4] = corrected_name
                    rows_corrected += 1
            
            writer.writerow(row)
            
    os.replace(TEMP_FILE, INPUT_FILE)
    print(f"Standardized Source CSV: {rows_corrected} corrections made using extended mapping.")

if __name__ == "__main__":
    correct_csv()
