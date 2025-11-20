package it.interzen.zencommonlibrary.dto.zendocuments;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class FolderDossierDTO extends FolderBaseDTO implements HasID<Long>, LookupEntityGReturnLongPK<FolderDossierDTO> {
    private String dossierNumber;
    private UtenteTrackBasicChangesDTO dossierOwnerId;
    private Long dossierGroupOwnerId;
    private DossierStatusEnum dossierStatus;
	private DossierTypologyEnum dossierTypology;
    private LocalDateTime dossierStartDate;
    private LocalDateTime dossierCloseDate;
    private LocalDateTime dossierExpiringDate;
    private String physicalLocation;
    private Boolean externalContactAccountAccess = null;
    private String processKey;
    private String processInstanceId;
    private Long technicalProceduresId;

    @Override
    @JsonIgnore
    public String getCode() {
        return "";
    }

    @JsonIgnore
    @Override
    public LookupElementDTOLong<FolderDossierDTO> getLookupElementDTOLong() {
        return new LookupElementDTOLong<>(getId(), getName(), getCode());
    }
}