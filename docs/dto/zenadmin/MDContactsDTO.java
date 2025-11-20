package it.interzen.zencommonlibrary.dto.zenadmin;

import com.fasterxml.jackson.annotation.JsonIgnore;
import it.interzen.zencommonlibrary.basedb.LookupEntityGReturnLongPK;
import it.interzen.zencommonlibrary.basedb.Searchable;
import it.interzen.zencommonlibrary.dto.LookupElementDTOLong;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTOHasLongID;
import lombok.Getter;
import lombok.Setter;
import org.apache.commons.lang3.StringUtils;

import java.util.ArrayList;
import java.util.List;

@Getter
@Setter
public class MDContactsDTO extends TrackBasicChangesDTOHasLongID implements LookupEntityGReturnLongPK<MDAccountsDTO> , Searchable {
	protected String name;
	protected String surname;
	protected List<MDType> type = new ArrayList<>();
	protected MDCategory category;
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
	protected LookupElementDTOLong<MDAccountsDTO> accountId;

	@Override
	@JsonIgnore
	public String getDescription() {
		return name + " " + surname;
	}
	
	@Override
	@JsonIgnore
	public String getCode() {
		return null;
	}

	@Override
	public String createSearchString() {
		return StringUtils.defaultString(name) + " " +
				StringUtils.defaultString(surname) + " " +
				StringUtils.defaultString(name) + " " +
				StringUtils.defaultString(vatNumber) + " " +
				StringUtils.defaultString(fiscalCode) + " " +
				StringUtils.defaultString(pec) + " " +
				StringUtils.defaultString(email) + " " +
				StringUtils.defaultString(phone) + " " +
				StringUtils.defaultString(address) + " " +
				StringUtils.defaultString(city) + " " +
				StringUtils.defaultString(zipCode);
	}
}
