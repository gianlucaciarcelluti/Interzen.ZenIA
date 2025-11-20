package it.interzen.zencommonlibrary.dto.zendocuments;

import lombok.Data;

@Data
public class DocumentSearchDTO extends DocumentDTO {
    DocumentTypeEnum type = DocumentTypeEnum.DOCUMENT;
}
