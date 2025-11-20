package it.interzen.zencommonlibrary.dto.zendocuments;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class FolderDossierGroupOwnerRequestDTO {
    Long classificationSchemaId;
    Long dossierGroupOwnerId;
}