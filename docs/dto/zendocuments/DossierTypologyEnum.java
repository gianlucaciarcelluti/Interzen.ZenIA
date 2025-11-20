package it.interzen.zencommonlibrary.dto.zendocuments;

public enum DossierTypologyEnum {
	AFFARE(1, "affare"), 
	ATTIVITA(2, "attivita"),
	PERSONA_FISICA(3, "persona fisica"),
	PERSONA_GIURIDICA(4, "persona giuridica"),
	PROCEDIMENTO_AMMINISTRATIVO(5, "procedimento amministrativo");
	
	int id;
    String description;

    DossierTypologyEnum(int id, String description) {
        this.id = id;
        this.description = description;
    }
}


