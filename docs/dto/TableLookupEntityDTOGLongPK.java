package it.interzen.zencommonlibrary.dto;

import it.interzen.zencommonlibrary.crud_base.HasID;

/* tabella specializzata per chiave long */
public class TableLookupEntityDTOGLongPK<T extends HasID<Long>> extends TableLookupEntityDTOGBase<T, Long> /*LongPKTableLookupEntityDTO*/ {
	public TableLookupEntityDTOGLongPK() {
		
	}
	
	public TableLookupEntityDTOGLongPK(long id, String descrizione, String codice) {
		super(id, descrizione, codice);
	}
	
	public TableLookupEntityDTOGLongPK(long id, String descrizione) {
		super(id, descrizione);
	}
	
	/*
	public TableLookupEntityDTOGLongPK(LookupEntityGReturnLongPK<T> d) {
		super(
			d.getBaseLookupEntityDTO().getId(), 
			d.getBaseLookupEntityDTO().getDescription(),
			d.getBaseLookupEntityDTO().getCode()
		);
	}
	*/
}
