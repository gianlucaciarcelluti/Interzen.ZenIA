package it.interzen.zencommonlibrary.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
/* tabella base per i DTO delle lookup */
public class TableLookupEntityDTOGBase<T /*extends HasID<PK>*/, PK> extends TrackBasicChangesDTOHasID<PK> {	//extends TableLookupEntityDTOBase<PK> {
	protected String code;
	
	protected String description;
	
	public TableLookupEntityDTOGBase() {
		
	}
	
	public TableLookupEntityDTOGBase(PK id, String description, String codice) {
		this.id = id;
		this.description = description;
		this.code = codice;
	}
	
	public TableLookupEntityDTOGBase(PK id, String description) {
		this.id = id;
		this.description = description;
	}

}
