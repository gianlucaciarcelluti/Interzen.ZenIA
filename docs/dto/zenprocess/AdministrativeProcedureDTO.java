package it.interzen.zencommonlibrary.dto.zenprocess;

import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.GroupTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.ProtAOOTrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AdministrativeProcedureDTO extends TrackBasicChangesDTO implements HasID<Long> {
	
	private Long id;
	private ProtAOOTrackBasicChangesDTO aooId;
	private GroupTrackBasicChangesDTO groupId;
	private AdministrativeProcedureInitiativeEnum initiative;
	private String name;
	private String referenceLegislation;
	private UtenteTrackBasicChangesDTO procedureOwner;
	private UtenteTrackBasicChangesDTO orderOwner;
	private Integer deadlineDays;
	private String externalLink;
	private String legalAndJurisdictionalProtection;
	private String paymentsMethod;
	private Integer silenceExpiringDays;
	private Integer sciaCheckingDays;
	private String notes;
	private String requiredDocuments;
	
}
