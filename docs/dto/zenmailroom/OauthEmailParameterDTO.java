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
public class OauthEmailParameterDTO extends TrackBasicChangesDTO implements HasID<Long>, LookupEntityGReturnLongPK<OauthEmailParameterDTO> {
	private Long id;
	private String description; 
	private String clientid; 
	private String authtenant;
	private String clientsecret;
    private String tenantid;     
    private String provider = "microsoft";
    
	@Override
	public String getCode() {
		return null;
	}
	
	public void setCode(String code) {
		// necessario altrimenti non si riesce a fare il deserialize 
	}
}
