package it.interzen.zencommonlibrary.dto;

import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class GroupTrackBasicChangesDTO extends LookupElementDTOLong<HasID<Long>> {
	public GroupTrackBasicChangesDTO() {
		//
	}

	public GroupTrackBasicChangesDTO(Long id, String name, String code, String type) {
		this.id = id;
		this.name = name;
		this.code = code;
		this.description = name;
		this.type = type;
	}

	public GroupTrackBasicChangesDTO(Long id) {
		this.id = id;
	}
}
