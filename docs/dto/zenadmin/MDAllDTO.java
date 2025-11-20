package it.interzen.zencommonlibrary.dto.zenadmin;

import java.util.ArrayList;
import java.util.List;

import com.querydsl.core.annotations.PropertyType;
import com.querydsl.core.annotations.QueryType;
import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnBase;
import it.interzen.zencommonlibrary.dto.LookupElementDTOBase;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTOHasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTOHasLongID;
import jakarta.persistence.Convert;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MDAllDTO extends TrackBasicChangesDTOHasID<String> implements LookupEntityGReturnBase<MDAllDTO, String>{
	protected String id;
	
	protected String name;

	protected String legalStatus;
	
	@QueryType(PropertyType.SIMPLE)
	@Convert(converter = MDTipoAccountListConverter.class)
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
	
	protected String url;
	
	protected LookupElementDTOBase<ProtAOODTO, Long> officeAOOID;
	
	protected LookupElementDTOBase<MDAllDTO, String> accountId;
	
	protected String firstname;
	
	protected String lastname;
	
	/*
	public void setId(MDAllPKey k) {
		if (k == null) {
			id = null;
		}
		else {
			id = k.toString();
		}		
	}
	*/

	@Override
	public LookupElementDTOBase<MDAllDTO, String> getLookupElementDTOBase() {
		return new LookupElementDTOBase<MDAllDTO, String>(getId(), getName(), getIPACode());
	}
}
