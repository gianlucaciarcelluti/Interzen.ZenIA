package it.interzen.zencommonlibrary.dto;

import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class CompanyTrackBasicChangesDTO extends LookupElementDTOLong<HasID<Long>> {

	public CompanyTrackBasicChangesDTO(Long id, String name, String code) {
		this.id = id;
		this.code = code;
		this.description = name;
	}

	public CompanyTrackBasicChangesDTO(Long id) {
		this.id = id;
	}
}
