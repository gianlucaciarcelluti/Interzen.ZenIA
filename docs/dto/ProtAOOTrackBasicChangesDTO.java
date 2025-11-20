package it.interzen.zencommonlibrary.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@JsonIgnoreProperties(ignoreUnknown = true)
public class ProtAOOTrackBasicChangesDTO extends LookupElementDTOLong<HasID<Long>> {

	public ProtAOOTrackBasicChangesDTO(Long id, String name, String code) {
		this.id = id;
		this.code = code;
		this.description = name;
	}

	public ProtAOOTrackBasicChangesDTO(Long id) {
		this.id = id;
	}
	
	public ProtAOOTrackBasicChangesDTO() {
	}
}
