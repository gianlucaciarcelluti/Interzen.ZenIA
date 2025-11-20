package it.interzen.zencommonlibrary.dto.zendocuments;

public enum LegaArchiveTypeEnum {
	COMPANY(1, "Company"),
	DOCUMENTTYPE(2, "Document type"),
	DATE(3, "Data"),
	STANDARD(4, "Metadata standard"),
	NOT(5, "Not");
		
	int id;
	String description;
	
	LegaArchiveTypeEnum(int id, String description) {
		this.id = id;
		this.description = description;
	} 
}
