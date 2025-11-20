package it.interzen.zencommonlibrary.dto;

/* specializzazione per la primary key String */
public class LookupElementDTOString<T> extends LookupElementDTOBase<T, String>{
	public LookupElementDTOString() {
		
	}
	
	public LookupElementDTOString(LookupElementDTOBase<T, String> d) {
		this.id = d.getId();
		this.description = d.getDescription();
		this.code = d.getCode();
	}
	
	public LookupElementDTOString(String id) {
		this.id = id;
	}
	
	public LookupElementDTOString(String id, String description) {
		this.id = id;
		this.description = description;
	}
	
	public LookupElementDTOString(String id, String descrizione, String codice) {
		this.id = id;
		this.description = descrizione;
		this.code = codice;
	}

	public LookupElementDTOString(String id, String descrizione, String codice, String nome) {
		this.id = id;
		this.description = descrizione;
		this.code = codice;
		this.name = nome;
	}

	public LookupElementDTOString(String id, String descrizione, String codice, String nome, String type) {
		this.id = id;
		this.description = descrizione;
		this.code = codice;
		this.name = nome;
		this.type = type;
	}
}
