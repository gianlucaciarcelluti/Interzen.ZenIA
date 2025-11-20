package it.interzen.zencommonlibrary.dto.zendocuments;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Data
public class BreadcrumbItem {
	Long folderId;
	String folderName;

	public BreadcrumbItem() {
	}

	public BreadcrumbItem(Long folderId, String folderName) {
		this.folderId = folderId;
		this.folderName = folderName;
	}
}
