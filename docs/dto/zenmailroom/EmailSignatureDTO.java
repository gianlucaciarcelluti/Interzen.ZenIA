package it.interzen.zencommonlibrary.dto.zenmailroom;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class EmailSignatureDTO extends TrackBasicChangesDTO implements HasID<Long>, LookupEntityGReturnLongPK<EmailSignatureDTO> {
	private Long id;
	private String title;
    private String html;
    
	@Override
	public String getDescription() {
		return title;
	}
	
	@Override
	public String getCode() {
		return null;
	}
	
	public void setDescription(String description) {
		title = description;
	}
	
	public void setCode(String code) {
		// altrimenti fallisce il deserialize
	}
}
