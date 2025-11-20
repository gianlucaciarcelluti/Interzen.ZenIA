package it.interzen.zencommonlibrary.dto.zenadmin;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TableLookupEntityDTOGLongPK;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class GroupDTO  extends TableLookupEntityDTOGLongPK<GroupDTO> implements LookupEntityGReturnLongPK<GroupDTO> {
    private Long id;

    private String externalid;

    private String name;

    private GroupType type;

    private String officeCode;

    private LookupElementDTOLong<?> officeAOOID;

    private String officePhone;

    private String officeFax;

    private UtenteTrackBasicChangesDTO officeManager;

    private LookupElementDTOLong<?> parentOffice;


    private Boolean active;

    public GroupDTO() {
        this.active =true;
    }
}
