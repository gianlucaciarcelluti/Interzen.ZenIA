package it.interzen.zencommonlibrary.dto.zendocuments;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.zenmailroom.EmailParameterTypeEnum;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class FolderEmailDTO extends FolderBaseDTO implements HasID<Long>, LookupEntityGReturnLongPK<FolderEmailDTO> {
    private Long emailParameterId;
    
    @Enumerated(EnumType.STRING)
    private EmailParameterTypeEnum emailParameterType = EmailParameterTypeEnum.EMAIL;

    @Override
    @JsonIgnore
    public String getCode() {
        return "";
    }

    @JsonIgnore
    @Override
    public LookupElementDTOLong<FolderEmailDTO> getLookupElementDTOLong() {
        return new LookupElementDTOLong<>(getId(), getName(), getCode());
    }
}