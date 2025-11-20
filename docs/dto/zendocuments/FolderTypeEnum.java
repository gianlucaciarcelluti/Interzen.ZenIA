package it.interzen.zencommonlibrary.dto.zendocuments;

public enum FolderTypeEnum {
	FOLDER(1, "Folder"),
	DOSSIER(2, "Dossier"),
	CLASSIFICATIONSCHEMA(3, "Classification Schema"),
	EMAIL(4, "Email");
	
	int id;
	String description;
	
	FolderTypeEnum(int id, String description) {
		this.id = id;
		this.description = description;
	} 
}
