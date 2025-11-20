package it.interzen.zencommonlibrary.dto.zenprotocollo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@NoArgsConstructor
@AllArgsConstructor
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
public class ProtocolRegistrationDetailsDTO extends ProtocolDTO {
	
	KeycloakUserDTO protocolledByDetails;
	
}
