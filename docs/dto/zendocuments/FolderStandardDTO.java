package it.interzen.zencommonlibrary.dto.zendocuments;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class FolderStandardDTO extends FolderBaseDTO implements HasID<Long>, LookupEntityGReturnLongPK<FolderStandardDTO> {
    private String barCode;

    private String ftpPath;

    @Override
    @JsonIgnore
    public String getCode() {
        return "";
    }

    @JsonIgnore
    @Override
    public LookupElementDTOLong<FolderStandardDTO> getLookupElementDTOLong() {
        return new LookupElementDTOLong<>(getId(), getName(), getCode());
    }
}