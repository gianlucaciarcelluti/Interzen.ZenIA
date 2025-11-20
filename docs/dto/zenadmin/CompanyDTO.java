package it.interzen.zencommonlibrary.dto.zenadmin;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TableLookupEntityDTOGLongPK;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;


@Data
@Accessors(chain = true)
public class CompanyDTO extends TableLookupEntityDTOGLongPK<CompanyDTO> implements LookupEntityGReturnLongPK<CompanyDTO> {
	protected String address;
	
	protected LookupElementDTOLong<CountryDTO> countryId;
	
	protected LookupElementDTOLong<DistrictDTO> districtId;
	
	protected String city;
	
	protected String zipCode;
	
	protected String vatNumber;
	
	protected String fiscalCode;
	
	protected String legalarchivecompanycode;
}
