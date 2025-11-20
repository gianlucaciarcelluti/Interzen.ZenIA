package it.interzen.zencommonlibrary.dto.zenadmin;


public enum MDType {
	Customer("Customer"),
	Supplier("Supplier"),
	Uor("Uor"),
	Other("Other"),
	
	Lead("Lead"),
	Contact("Contact"),
	Private("Private");
	
	public boolean isForAccount() {
		var h = 
			this == Customer || 
			this == Supplier ||
			this == Uor ||
			this == Other;
		
		return h;
	}
	
	public boolean isForContact() {
		var h = isForAccount();
		
		return !h;
		
	}
	
	// Campo aggiuntivo per il testo associato a ogni valore
    private final String testo;

    // Costruttore dell'enum
    MDType(String testo) {
        this.testo = testo;
    }

    // Metodo per ottenere il testo associato al valore
    public String getTesto() {
        return testo;
    }
}
