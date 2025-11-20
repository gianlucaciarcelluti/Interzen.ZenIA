package it.interzen.zencommonlibrary.dto.zenprotocollo;

import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import it.interzen.zencommonlibrary.crud_base.HasID;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.apache.commons.lang3.StringUtils;

import javax.validation.constraints.AssertTrue;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import java.time.LocalDateTime;
import java.util.List;

/**
 * DTO di input per la registrazione di un nuovo protocollo.
 * I: Interno, E: In entrata, U: In uscita
 * @author Perniola Giuseppe
 */

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProtocolRegistrationDTO implements HasID<Long>{
	
	private Long id;

	@Schema(description ="L'id del protocollo correlato come padre")
	private Long correlatedParentProtocolId;

	@Schema(description ="L'id del documento principale da protocollare se questo è stato già archiviato. Se il seguente campo è null allora bisogna caricare il documento principale in altro modo.")
	private Long mainDocumentId;

	@Schema(description ="Indica il valore sull'asse X per il posizionamento del watermark di segnatura sui documenti e allegati")
	private Long watermarkPositionX;

	@Schema(description ="Indica il valore sull'asse Y per il posizionamento del watermark di segnatura sui documenti e allegati")
	private Long watermarkPositionY;

	//IEU
	@NotNull private Long companyId;
	
	//IEU
	@NotNull private Long aooId;
	
	//IEU
	//@NotNull private Long uorId;
	
	//IEU
	@NotNull private ProtocolRegistrationType protocolRegistrationType;
	
	
	//---------------------------------- SCHEDA CORRISPONDENTI
	@NotEmpty List<CorrespondentRegistrationDTO> correspondents;
	
	
	//---------------------------------- SCHEDA DETTAGLI
	
	//IEU
	@NotNull private ProtocolConfidentialityLevel protocolConfidentialityLevel;

	//IEU
	@NotNull private String subject;
	
	//IEU
	@Schema(description="Document date", pattern="dd-MM-YYYY")
	private String documentDate;

	@Schema(description="Expire date for the protocol", pattern="dd-MM-YYYY")
	private String expireDate;

	//IEU
	private String documentSigner;
	
	//IEU
	private String physicalLocation;
	
	//IEU
	private String notes;
	
	//E
	private String senderProtocol;
	
	//EU
	private String senderProtocolDate;
	
	//EU
	private ProtocolCorrespondenceType protocolCorrespondenceType;
	
	
	//---------------------------------- CLASSIFICAZIONE E FASCICOLAZIONE
	
	//IEU
	@NotNull private Long classificationId;
	
	//IEU
	private Long dossierId;
	
	
	//---------------------------------- RESPONSABILITA
	
	//IEU
	private List<ProtocolRegistrationManagerDTO> managers;

	@NotEmpty private Long uorCompetenceManagerId;
	@NotEmpty private Integer uorCompetenceManagerRev;

	private String userCompetenceManagerId;
	private Integer userCompetenceManagerRev;

	
	@Schema(description ="TRUE se il protocollo (e il relativo documento associato) deve essere smistato")
	private Boolean assignProtocol;
	
	//IEU
	private String sortingNotes;
	
	
	//--------------------------------- PROTOCOLLO D'EMERGENZA
	
	@NotNull private boolean emergencyProtocolFlag = false;
	
	private String emergencyRegisterIdNumber;
	private String emergencyRegisterName;
	private String causeOfInterruption;
	
	@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
	private LocalDateTime interruptionStartingDate;
	
	@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
	private LocalDateTime interruptionEndDate;
	
	private String emergencyRegisterProtocolNumber;
	
	@JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
	private LocalDateTime emergencyRegistrationDate;
	
	

	@AssertTrue(message = "I campi del protocollo d'emergenza sono obbligatori se è stato abilitato il protocollo d'emergenza")
    private boolean isProtocolloEmegenzaValidation() {
        if(emergencyProtocolFlag) {
        	return 	StringUtils.isNotBlank(emergencyRegisterIdNumber) &&
        			StringUtils.isNotBlank(emergencyRegisterName) &&
        			StringUtils.isNotBlank(causeOfInterruption) &&
        			interruptionStartingDate != null &&
        			interruptionEndDate != null &&
        			StringUtils.isNotBlank(emergencyRegisterProtocolNumber) &&
        			emergencyRegistrationDate != null;
        }
        else return true;
    }
	
	@AssertTrue(message = "I campi del protocollo d'emergenza devono essere nulli se il protocollo non è di emergenza")
    private boolean isNotProtocolloEmegenzaValidation() {
        if(!emergencyProtocolFlag) {
        	return 	emergencyRegisterIdNumber == null &&
        			emergencyRegisterName == null &&
        			causeOfInterruption == null &&
        			interruptionStartingDate == null &&
        			interruptionEndDate == null &&
        			emergencyRegisterProtocolNumber == null &&
        			emergencyRegistrationDate == null;
        }
        else return true;
    }
	

}
