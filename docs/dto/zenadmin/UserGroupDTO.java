package it.interzen.zencommonlibrary.dto.zenadmin;

import java.time.LocalDateTime;
import java.util.List;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.dto.GroupTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.TableLookupEntityDTOGLongPK;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.zendocuments.LookupDTO;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UserGroupDTO extends TableLookupEntityDTOGLongPK<UserGroupDTO> implements LookupEntityGReturnLongPK<UserGroupDTO> {
	
	private Long id;
	private UtenteTrackBasicChangesDTO userid;
	private Long groupid;
	private GroupTrackBasicChangesDTO groupDetails = null;
	private LocalDateTime insertionDate;
	private Boolean userIsActive = true;
	private List<LookupDTO> jobDescriptions;
	
	public UserGroupDTO() {
		this.insertionDate = LocalDateTime.now();
	}


}
