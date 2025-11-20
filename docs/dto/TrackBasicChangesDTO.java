package it.interzen.zencommonlibrary.dto;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Date;

import it.interzen.zencommonlibrary.basedb.GetUserDTOFromMSAAdmin;
import it.interzen.zencommonlibrary.basedb.TrackBasicChanges;
import it.interzen.zencommonlibrary.basedb.TrackBasicChangesI;
import it.interzen.zencommonlibrary.dto.zenadmin.AdminLookupDTO;
import it.interzen.zencommonlibrary.dto.zenadmin.RequireActions;
import it.interzen.zencommonlibrary.dto.zenadmin.UserDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class TrackBasicChangesDTO {
	protected LocalDateTime creationDate;

	protected UtenteTrackBasicChangesDTO createdBy;

	protected LocalDateTime modificationDate;

	protected UtenteTrackBasicChangesDTO modifiedBy;
	
	protected String searchData;
	
	public void setTrackingBasicChangesValueFromDB(TrackBasicChangesI dbObject, GetUserDTOFromMSAAdmin msAdmin) {
		if (dbObject == null) {
			return ;
		}		
		
		this.createdBy = msAdmin.get(dbObject.getCreatedBy());
		this.creationDate = dbObject.getCreationDate();
		
		this.modifiedBy = msAdmin.get(dbObject.getModifiedBy());
		this.modificationDate = dbObject.getModificationDate();
		
		this.searchData = dbObject.getSearchData();
	}
}
