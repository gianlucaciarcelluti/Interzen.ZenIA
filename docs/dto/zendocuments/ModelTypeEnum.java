package it.interzen.zencommonlibrary.dto.zendocuments;

public enum ModelTypeEnum {
	DOCUMENT(1, "Document"),
	FOLDER(2, "Folder"),
	DOSSIER(3, "Dossier");
		
	int id;
	String description;
	
	ModelTypeEnum(int id, String description) {
		this.id = id;
		this.description = description;
	} 
}
