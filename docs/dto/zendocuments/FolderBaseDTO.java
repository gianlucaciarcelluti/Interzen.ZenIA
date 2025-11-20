package it.interzen.zencommonlibrary.dto.zendocuments;


import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class FolderBaseDTO extends TrackBasicChangesDTO implements HasID<Long> {
    private Long id;
    private String name;
    private String description;
    private FolderTypeEnum type = FolderTypeEnum.FOLDER;
    private Boolean inheritPermission = true;
    private LookupElementDTOLong<? extends FolderBaseDTO> parentId;
    
    @Enumerated(EnumType.STRING)
    private FolderAreaEnum area = FolderAreaEnum.ARCHIVE;

    // Modello associato al folder
    private LookupElementDTOLong<? extends ModelDTO> model;

    // Elenca i metadati associati al folder
    private List<MetadataValueDTO> metadata;
    
    private OperationsDTO operations;
    private Long documentCurrentCount = 0L;
    private Long documentDepositCount = 0L;
    private Long documentHistoricalCount = 0L;
    
    private Long companyid;
	private Long aooid;

    private boolean statusCurrent = false;
    private boolean statusDeposit = false;
    private boolean statusHistorical = false;

    private Long numbering;
    private Long externalReferalId;
}