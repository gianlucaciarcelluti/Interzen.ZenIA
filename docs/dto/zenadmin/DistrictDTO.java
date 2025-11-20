package it.interzen.zencommonlibrary.dto.zenadmin;

import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TableLookupEntityDTOGLongPK;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class DistrictDTO extends TableLookupEntityDTOGLongPK<DistrictDTO> implements LookupEntityGReturnLongPK<DistrictDTO> {
	protected LookupElementDTOLong<CountryDTO> countryId;

}
