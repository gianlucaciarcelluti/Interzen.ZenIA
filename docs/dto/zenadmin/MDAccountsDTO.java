package it.interzen.zencommonlibrary.dto.zenadmin;

import com.fasterxml.jackson.annotation.JsonIgnore;
import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTOHasLongID;
import lombok.Getter;
import lombok.Setter;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
public class MDAccountsDTO extends TrackBasicChangesDTOHasLongID implements LookupEntityGReturnLongPK<MDAccountsDTO> {
	protected String name;
	
	protected List<MDType> type = new ArrayList<>();
	
	protected MDCategory category;

	protected String IPACode;

	protected String AOOCode;
	
	protected LookupElementDTOLong<CountryDTO> countryId;
	
	protected LookupElementDTOLong<DistrictDTO> districtId;
	
	protected String city;
	
	protected String zipCode;
	
	protected String address;
	
	protected String phone;
	
	protected String fax;
	
	protected String email;
	
	protected String vatNumber;
	
	protected String pec;
	
	protected String fiscalCode;


	@Override
	@JsonIgnore
	public String getDescription() {
		return this.name;
	}

	@Override
	@JsonIgnore
	public String getCode() {
		return this.AOOCode;
	}
}
