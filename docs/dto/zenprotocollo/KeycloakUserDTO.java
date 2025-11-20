package it.interzen.zencommonlibrary.dto.zenprotocollo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class KeycloakUserDTO {
	private String usernName;
	private String partnerCode;
	private String email;
	private String operatorId;
	private String iss;				// issuer
	private String externalId;		// id di keycloack
	private String tokenId;
}
