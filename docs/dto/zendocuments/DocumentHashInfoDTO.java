package it.interzen.zencommonlibrary.dto.zendocuments;

import java.util.ArrayList;
import java.util.List;

import lombok.Data;

@Data
public class DocumentHashInfoDTO {

	Long documentId;
	Long protocolId;
	String fileName;
	String fileDescription;
	String hashAlgorithm;
	String hashValue;
	DocumentAttachmentType attachmentType = null;
	List<DocumentHashInfoDTO> attachments = new ArrayList<>();

}
