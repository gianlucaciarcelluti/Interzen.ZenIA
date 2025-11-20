package it.interzen.zencommonlibrary.dto.zenprotocollo;

import jakarta.validation.constraints.NotNull;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProtocolRegistrationManagerDTO {
	
	private Long uorId;
	private Integer uorRev;
	
	private String userId;
	private Integer userRev;

	private String description;
	
	@NotNull
	private ProtocolResponsibilityType responsibilityType;
	
	@NotNull
	private ResponsibilityIdType idType;

}
