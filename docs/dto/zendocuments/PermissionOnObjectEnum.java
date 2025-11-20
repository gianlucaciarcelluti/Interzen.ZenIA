package it.interzen.zencommonlibrary.dto.zendocuments;

public enum PermissionOnObjectEnum {
	DOCUMENT(1, "Documento"),
	FOLDER(2, "Folder"),
	MODEL(3, "Model");
	
	int id;
	String descrizione;
	
	PermissionOnObjectEnum(int id, String description) {
		this.id = id;
		this.descrizione = description;
	}
}
