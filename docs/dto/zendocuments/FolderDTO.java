package it.interzen.zencommonlibrary.dto.zendocuments;


import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.zenmailroom.EmailParameterTypeEnum;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class FolderDTO extends FolderBaseDTO implements HasID<Long>, LookupEntityGReturnLongPK<FolderDTO> {
    // Classification Schema properties
    private ClassificationStatusEnum classificationSchemaStatus;
    
    // Dossier properties
    private String dossierNumber;
    private UtenteTrackBasicChangesDTO dossierOwnerId;
    private DossierStatusEnum dossierStatus;
	private DossierTypologyEnum dossierTypology;
    private LocalDateTime dossierStartDate;
    private LocalDateTime dossierCloseDate;
    private Long dossierGroupOwnerId;
    private LocalDateTime dossierExpiringDate;
    private String physicalLocation;
    private Boolean externalContactAccountAccess = null;
    private String processKey;
    private String processInstanceId;
    private Long technicalProceduresId;
    
    // Email properties
    private Long emailParameterId;
    @Enumerated(EnumType.STRING)
    private EmailParameterTypeEnum emailParameterType;


    // Standard properties
    private String barCode;
    private String ftpPath;

    @Override
    @JsonIgnore
    public String getCode() {
        return "";
    }

    @JsonIgnore
    @Override
    public LookupElementDTOLong<FolderDTO> getLookupElementDTOLong() {
        return new LookupElementDTOLong<>(getId(), getName(), getCode());
    }
}