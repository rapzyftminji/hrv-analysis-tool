import pandas as pd

INPUT_EXCEL_FILE = 'Ekstraksi Fitur.xlsx' 
OUTPUT_CSV_FILE = 'Ekstraksi_Fitur_Converted.csv'  
HEADER_ROW = 1  

def convert_excel_to_csv():
    print(f"Reading {INPUT_EXCEL_FILE}...")
    
    try:

        df = pd.read_excel(INPUT_EXCEL_FILE, header=HEADER_ROW, engine='openpyxl')
        df.to_csv(OUTPUT_CSV_FILE, index=False)
        
        print(f"Success! Converted to {OUTPUT_CSV_FILE}")
        
    except FileNotFoundError:
        print(f"Error: Could not find '{INPUT_EXCEL_FILE}'. Make sure it's in the same folder.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    convert_excel_to_csv()