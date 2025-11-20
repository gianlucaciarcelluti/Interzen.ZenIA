package it.interzen.zencommonlibrary.dto;

import it.interzen.zencommonlibrary.crud_base.HasID;

/* specializzazione per la primary key Long */
public class LookupElementDTOLong<T extends HasID<Long>> extends LookupElementDTOBase<T, Long>{
	public LookupElementDTOLong() {
		
	}
	
	public LookupElementDTOLong(LookupElementDTOBase<T, Long> d) {
		this.id = d.getId();
		this.description = d.getDescription();
		this.code = d.getCode();
	}
	
	public LookupElementDTOLong(Long id, String descrizione, String codice) {
		this.id = id;
		this.description = descrizione;
		this.code = codice;
	}

	public LookupElementDTOLong(Long id, String descrizione, String codice, String nome) {
		this.id = id;
		this.description = descrizione;
		this.code = codice;
		this.name = nome;
	}

	public LookupElementDTOLong(Long id, String descrizione, String codice, String nome, String type) {
		this.id = id;
		this.description = descrizione;
		this.code = codice;
		this.name = nome;
		this.type = type;
	}
	
	public LookupElementDTOLong(Long id) {
		this.id=id;
	}
	
	public LookupElementDTOLong(String code) {
		this.code = code;
	}
	
}
