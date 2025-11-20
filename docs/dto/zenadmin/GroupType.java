package it.interzen.zencommonlibrary.dto.zenadmin;

public enum GroupType {
    Generico("Generico"),
    Ufficio("Ufficio"),
    CRM("CRM");
    // Campo aggiuntivo per il testo associato a ogni valore
    private final String txt;

    // Costruttore dell'enum
    GroupType(String txt) {
        this.txt = txt;
    }

    // Metodo per ottenere il testo associato al valore
    public String getTxt() {
        return txt;
    }
}
