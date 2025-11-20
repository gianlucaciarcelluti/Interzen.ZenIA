package it.interzen.zencommonlibrary.dto.zendocuments;

import java.time.LocalDateTime;
import java.util.List;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import jakarta.persistence.Column;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Identifica il DTO con le proprietà di base per i documenti.
 * Gli altri DTO estendono questa classe
 */
@Data
@EqualsAndHashCode(callSuper=false)
public class DocumentBaseDTO extends TrackBasicChangesDTO implements HasID<Long>  {
	private Long id;
	
    protected String description;

    @NotNull
    protected String fileName;

    protected String note;

    protected DocumentSource source;

    private Boolean isAttachment = false;

    @Enumerated(EnumType.STRING)
    private DocumentAttachmentType attachmentType;

    protected LookupElementDTOLong<FolderDTO> folderId;

    @Enumerated(EnumType.STRING)
    protected DocumentStatus status = DocumentStatus.CURRENT;
    
	@Enumerated(EnumType.STRING)
	protected DocumentStatusLegalArchiveEnum statusLegalArchive;

    @Enumerated(EnumType.STRING)
    private DocumentStatusCreationEnum statusCreation = DocumentStatusCreationEnum.FINAL;

    protected String externalReference;

    protected String barCode;

    protected Boolean inheritPermission = true;

    protected LookupElementDTOLong<ModelDTO> model;

    // Elenca i metadati associati all'oggetto
    protected List<MetadataValueDTO> metadata;

    private UtenteTrackBasicChangesDTO checkedinOwner; // Id dell'utente che ha fatto il checkin sul documento

    private LocalDateTime checkedinDate;   //Data in cui il documento è stato preso in carico
    
    private OperationsDTO operations;

    // Per gli allegati
    private Long parentId;

    private String mimeType;

    private int attachmentNumber = 0;
    
    @Enumerated(EnumType.STRING)
    protected DocumentLastActionEnum lastAction = DocumentLastActionEnum.CREATED;

    @Enumerated(EnumType.STRING)
    private DocumentFlowTypeEnum flowType;

    protected String processKey;
    private String processInstanceId;
    private String processDocumentType;
}
