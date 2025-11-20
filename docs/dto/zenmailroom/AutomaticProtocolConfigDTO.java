package it.interzen.zencommonlibrary.dto.zenmailroom;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.zenadmin.MDCategory;
import it.interzen.zencommonlibrary.dto.zenprotocollo.AutomaticRegisterActionEnum;
import it.interzen.zencommonlibrary.dto.zenprotocollo.ProtocolRegistrationType;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@EqualsAndHashCode(callSuper = false)
@AllArgsConstructor
@NoArgsConstructor
public class AutomaticProtocolConfigDTO extends TrackBasicChangesDTO implements HasID<Long>, LookupEntityGReturnLongPK<AutomaticProtocolConfigDTO> {
    Long id;
    Long emailParameter;
    Long classificationId;
    ProtocolRegistrationType protocolRegistrationType;
    AutomaticRegisterActionEnum automaticRegisterAction;
    MDCategory newCorrespondantCategory;
    Long uorCompetenceManagerId;
    String userCompetenceManagerId;
    boolean flagAssignment = false;
    Integer expiringDays = 0;
    List<Long> uorCopyManagerIds;
    List<String> userCopyManagerIds;
    boolean active = false;

    Long companyid;
    Long aooid;

    public Long getId() {
        return id;
    }

    public String getDescription() {
        return null;
    }

    public String getCode() {
        return null;
    }
}