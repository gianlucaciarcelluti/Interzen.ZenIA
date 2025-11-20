package it.interzen.zencommonlibrary.dto;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.zenadmin.AdminLookupDTO;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UtenteTrackBasicChangesDTO extends LookupElementDTOLong<HasID<Long>> {
	String surname;
	String username;
	String email;
	String userRoleDescription;
	String userRoleCode;

	public UtenteTrackBasicChangesDTO() {
		//
	}
	
	public UtenteTrackBasicChangesDTO(Long id, String userName, String name, String surname, String email) {
		this.id = id;
		this.name = name;
		this.surname = surname;
		this.code = userName;
		this.username = userName;
		this.description = surname + " " + name;
		this.email = email;
	}

	public UtenteTrackBasicChangesDTO(Long id, String userName, String name, String surname, String email, String userRoleCode, String userRoleDescription) {
		this.id = id;
		this.name = name;
		this.surname = surname;
		this.code = userName;
		this.username = userName;
		this.email = email;
		this.description = surname + " " + name;
		this.userRoleCode = userRoleCode;
		this.userRoleDescription = userRoleDescription;
	}
	
	public UtenteTrackBasicChangesDTO(Long id) {
		this.id = id;
	}
}
