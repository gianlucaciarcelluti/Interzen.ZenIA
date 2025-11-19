from fillpdf import fillpdfs
import os

# Mostra la directory corrente
print(f"Directory corrente: {os.getcwd()}")

# Specifica il percorso del PDF
pdf_path = "src/pdf_replacer/pdf_form_test.pdf"
output_path = "src/pdf_replacer/pdf_form_test_out.pdf"

# Verifica che il file esista
if not os.path.exists(pdf_path):
    print(f"Errore: Il file '{pdf_path}' non è stato trovato.")
    print("Assicurati che il file PDF sia presente nella directory corrente.")
    exit()

# Elenca i campi presenti nel PDF
print("\nCampi presenti nel PDF:")
try:
    fields = fillpdfs.get_form_fields(pdf_path)
    if fields:
        print("\nTutti i campi modulo:")
        for field_name, field_value in fields.items():
            print(f"- {field_name}: {field_value}")
    else:
        print("Nessun campo modulo trovato")
except Exception as e:
    print(f"Errore nell'accesso ai campi modulo: {e}")

# Chiedi se continuare
risposta = input("\nVuoi continuare con la modifica del PDF? (s/n): ")
if risposta.lower() not in ['s', 'si', 'y', 'yes']:
    print("Operazione annullata.")
    exit()

# Compila i campi modulo
try:
    # Prepara i dati da inserire nei campi
    data_dict = {
        "Casella di testo 1": "test value"
    }
    
    # Se il campo non esiste, prova con il primo campo disponibile
    if fields and "Casella di testo 1" not in fields:
        first_field = list(fields.keys())[0]
        data_dict = {first_field: "test value"}
        print(f"\nCampo 'Casella di testo 1' non trovato, uso '{first_field}'")
    
    print(f"\nCompilazione campi: {data_dict}")
    
    # Compila il PDF
    if os.path.exists(output_path):
        print(f"Il file '{output_path}' esiste già e verrà sovrascritto.")
    
    fillpdfs.write_fillable_pdf(pdf_path, output_path, data_dict)
    
    print("\nCampi modulo aggiornati con successo!")
    
    # Verifica i campi dopo l'aggiornamento
    print("\nVerifica campi nel PDF di output:")
    output_fields = fillpdfs.get_form_fields(output_path)
    if output_fields:
        for field_name, field_value in output_fields.items():
            print(f"- {field_name}: {field_value}")
    
except Exception as e:
    print(f"Errore nell'aggiornamento dei campi: {e}")
    import traceback
    traceback.print_exc()

print("\nPDF salvato con successo!")