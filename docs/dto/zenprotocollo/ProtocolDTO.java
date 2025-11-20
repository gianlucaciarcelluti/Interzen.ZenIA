package it.interzen.zencommonlibrary.dto.zenprotocollo;

import io.swagger.v3.oas.annotations.media.Schema;
import it.interzen.zencommonlibrary.basedb.TrackBasicChanges;
import it.interzen.zencommonlibrary.crud_base.HasID;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTO;
import it.interzen.zencommonlibrary.dto.TrackBasicChangesDTOHasID;
import it.interzen.zencommonlibrary.dto.UtenteTrackBasicChangesDTO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import it.interzen.zencommonlibrary.dto.zendocuments.smistamento.AssignmentDetailsOutDTO;

import java.util.ArrayList;
import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProtocolDTO extends TrackBasicChangesDTO implements HasID<Long> {
	
	@Schema(description="Protocol id")
	private Long id;

	private CorrelatedProtocolDTO correlatedParentProtocol = null;
	private List<CorrelatedProtocolDTO> correlatedChildrenProtocols = new ArrayList<>();
	
	@Schema(description="The id of the associated daily protocol register")
	private Long dailyRegisterId;
	
	@Schema(description="The protocols company id. Retrieved from ZenAdmin")
	private Long companyId;
	
	@Schema(description="The protocols company name. Retrieved from ZenAdmin")
	private String companyName;
	
	@Schema(description="The protocols AOO id. Retrieved from ZenAdmin")
    private Long aooId;
	
	@Schema(description="The protocols AOO name. Retrieved from ZenAdmin")
	private String aooName;
	
	//@Schema(description="The protocols UOR id. Retrieved from ZenAdmin")
    //private Long uorId;
	
	@Schema(description="Protocol type (INBOX, OUTBOX, INTERNAL)")
    private ProtocolRegistrationType protocolRegistrationType;
	
	@Schema(description="Protocol status (OPEN, CLOSED, CANCELED)")
    private ProtocolStatus status;

	@Schema(description="If protocol status is CANCELED then it contains the reason of the cancellation")
	private String cancellationReason;
	
	@Schema(description="The protocol number, must be unique and automatically generated. ", pattern="0000001")
    private String protocolNumber;
	
	@Schema(description="Complete data of the user who closed the protocol")
	private UtenteTrackBasicChangesDTO protocolledBy;
	
	@Schema(description="Protocol year of registration, automatically generated", pattern="YYYY")
    private Integer registrationYear;
	
	@Schema(description="Protocol registration date, automatically generated", pattern="dd-MM-YYYY hh:mm:ss")
    private String registrationDate;
	
	@Schema(description="Protocol cancellation (annullamento) date, automatically generated", pattern="dd-MM-YYYY hh:mm:ss")
    private String cancelingDate;

	@Schema(description="Expire date for the protocol", pattern="dd/MM/YYYY")
	private String expireDate;

	@Schema(description="Hash of the main document, retrieved from ZenDocuments")
	private String mainDocumentHash;

	@Schema(description="The id of the main document, retrieved from ZenDocuments")
	private Long mainDocumentId;
	
	@Schema(description="Token needed to access the document")
	private String docToken;

	private String documentSigner;
	
	private String modifiedByName;
	
	@Schema(description="The description of the last operation made on the protocol. Used for audit logging")
	private String lastLoggedOperation;
    
    
    //---------------------------------- SCHEDA CORRISPONDENTI
	@Schema(description="The list of correspondents associated with the protocol")
  	List<CorrespondentOutDTO> correspondents;
	
	//@Schema(description="The list of UORs correspondents associated with the protocol")
  	//List<GruppoDTO> correspondentsUors;
	
	
	//---------------------------------- SCHEDA DETTAGLI
	@Schema(description="Protocol confidentiality level (PUBLIC, CONFIDENTIAL)")
	private ProtocolConfidentialityLevel protocolConfidentialityLevel;
	private String subject;
	private String documentDate;
	private String physicalLocation;
	private String notes;
	private String senderProtocol;
	private String senderProtocolDate;
	private ProtocolCorrespondenceType protocolCorrespondenceType;
	
	
	//---------------------------------- CLASSIFICAZIONE E FASCICOLAZIONE
	private ClassificationOutDTO classification;
	private Long dossierId;
	
	
	//---------------------------------- RESPONSABILITA
	private List<ProtocolRegistrationManagerDTO> managers;

	private Long uorCompetenceManagerId;
	private Integer uorCompetenceManagerRev;
	private String uorCompetenceManagerDescription;

	private String userCompetenceManagerId;
	private Integer userCompetenceManagerRev;
	private String userCompetenceManagerDescription;

	private boolean doAssignDocument;
	private boolean doNotifySorting;
	
	private boolean assignProtocol = false;
	private String sortingNotes;
	
    //------------------- OPERAZIONI
    private ProtocolListOperationsDTO operations = new ProtocolListOperationsDTO();
    
    
	//--------------------------------- PROTOCOLLO D'EMERGENZA
	private boolean emergencyProtocolFlag;
	private String emergencyRegisterIdNumber;
	private String emergencyRegisterName;
	private String causeOfInterruption;
	private String interruptionStartingDate;
	private String interruptionEndDate;
	private String emergencyRegisterProtocolNumber;
	private String emergencyRegistrationDate;
	
	
	//--------------------------------- SMISTAMENTO
	AssignmentDetailsOutDTO assignmentDetails = null;

	private Boolean imported = false;
	

	public void addChildCorrelatedProtocol(CorrelatedProtocolDTO prot){
		this.correlatedChildrenProtocols.add(prot);
	}
	
	
	public void setViewOperation(boolean val) {
		this.getOperations().setView(val);
	}
	
	public void setDeleteOperation(boolean val) {
		this.getOperations().setDelete(val);
	}
	
	public void setEditOperation(boolean val) {
		this.getOperations().setEdit(val);
	}

}
