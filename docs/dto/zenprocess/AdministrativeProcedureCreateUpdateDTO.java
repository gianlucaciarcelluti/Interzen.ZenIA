package it.interzen.zencommonlibrary.dto.zenprocess;


import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AdministrativeProcedureCreateUpdateDTO {

	@NotNull(groups = ValidationGroups.Create.class, message = "field cannot be empty or null")
	private Long aooId;
	
	@NotNull(groups = ValidationGroups.Create.class, message = "field cannot be empty or null")
	private Long groupId;
	
	@NotNull(groups = ValidationGroups.Create.class, message = "field cannot be empty or null")
	private AdministrativeProcedureInitiativeEnum initiative;
	
	@NotEmpty(groups = ValidationGroups.Create.class, message = "field cannot be empty or null")
	private String name;
	
	@NotEmpty(groups = ValidationGroups.Create.class, message = "field cannot be empty or null")
	private String referenceLegislation;
	
	@NotNull(groups = ValidationGroups.Create.class, message = "field cannot be empty or null")
	private Long procedureOwner;
	
	@NotNull(groups = ValidationGroups.Create.class, message = "field cannot be empty or null")
	private Long orderOwner;
	
	private Integer deadlineDays;
	private String externalLink;
	private String legalAndJurisdictionalProtection;
	private String paymentsMethod;
	private Integer silenceExpiringDays;
	private Integer sciaCheckingDays;
	private String notes;
	
}
