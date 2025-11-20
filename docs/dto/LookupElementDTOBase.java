package it.interzen.zencommonlibrary.dto;

import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
/* classe per i DTO delle lookup. HA solo 3 campi: ID, DESCRIZIONE e CODICE */
public class LookupElementDTOBase<T, PK> implements HasID<PK> {
	protected PK id;
	protected String description;
	protected String name;
	protected String code;
	protected String type;
	
	public LookupElementDTOBase() {
		
	}
	
	public LookupElementDTOBase(PK id, String description, String code) {
		this.id = id;
		this.description = description;
		this.code = code;
	}

	public LookupElementDTOBase(PK id, String description, String code, String name) {
		this.id = id;
		this.description = description;
		this.code = code;
		this.name = name;
	}

	public LookupElementDTOBase(PK id, String description, String code, String name, String type) {
		this.id = id;
		this.description = description;
		this.code = code;
		this.name = name;
		this.type = type;
	}
	
	public LookupElementDTOBase(PK id, String description) {
		this.id = id;
		this.description = description;
	}
	
	public LookupElementDTOBase(PK id) {
		this.id=id;
	}
}
