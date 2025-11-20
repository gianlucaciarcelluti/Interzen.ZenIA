package it.interzen.zencommonlibrary.dto.zenadmin;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;

public enum MDCategory {
	ItalianPublicAdministration("IPA"),
	LegalPerson("LP"),
	PhysicalPerson("PP"),
	ForeignPublicAdministration("FPA");
	
	// Campo aggiuntivo per il testo associato a ogni valore
    private final String label;

    // Costruttore dell'enum
    MDCategory(String label) {
        this.label = label;
    }

    @JsonCreator
    public static MDCategory forValue(String value) {
        for (MDCategory category : values()) {
            if (category.name().equals(value)) {
                return category;
            }
        }
        for (MDCategory category : values()) {
            if (category.label.equals(value)) {
                return category;
            }
        }
        throw new IllegalArgumentException("Valore non valido per MDCategory: " + value);
    }
    
    @JsonValue
    public String getLabel() {
    	return label;
    }
}
