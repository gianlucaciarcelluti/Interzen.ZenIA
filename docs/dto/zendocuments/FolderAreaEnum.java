package it.interzen.zencommonlibrary.dto.zendocuments;

public enum FolderAreaEnum {
	ARCHIVE(1, "Archive"),
	INBOUND(2, "Inbound"),
	OUTBOUND(3, "Outbound");

	int id;
	String description;

	FolderAreaEnum(int id, String description) {
		this.id = id;
		this.description = description;
	} 
}
